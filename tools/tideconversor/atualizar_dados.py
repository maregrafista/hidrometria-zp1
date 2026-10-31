#!/usr/bin/env python3
"""Atualiza as páginas do TideConversor com dados novos do RLS (Fazendinha e Curuá).

Uso:  python3 atualizar_dados.py [fazendinha|curua ...]
Lê arquivos novos em entrada/<estacao>/ (Excel exportado do Hydromet Cloud ou CSV), junta com dados/serie_<estacao>.csv,
aplica o controle de qualidade, recalcula marés e série horária e reescreve o bloco TC_HARM da página.
As constantes harmônicas não mudam. Sai com código 0 se houve atualização e 3 se não havia dado novo.
"""
import sys, os, re, json, math, glob, shutil, datetime as dt
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import numpy as np, pandas as pd
from hourly import hourly
from events import predictor, swing, observed_extremes
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
GAP, WIN = 15, 5400
EST = {
  'fazendinha': dict(pagina='tideconversor/index.html', passo=5, filtro='residuo', desde='2026-08-01', recalcula_antigos=False),
  'curua':      dict(pagina='tideconversor/curua/index.html', passo=10, filtro='segdif', desde=None, recalcula_antigos=True),
}
VERSAO = '3.8'

def ler(path):
    cab = open(path, 'rb').read(8)
    if cab[:4] == b'\xd0\xcf\x11\xe0' or cab[:2] == b'PK':   # Excel de verdade (.xls binário ou .xlsx)
        x = pd.read_excel(path, header=None, engine='xlrd' if cab[:2] != b'PK' else 'openpyxl')
        d = None
        for i in range(min(len(x), 30)):   # acha a 1a linha cuja 1a coluna é data/hora
            if pd.notna(pd.to_datetime(x.iloc[i, 0], errors='coerce')): d = x.iloc[i:, :2].copy(); break
        assert d is not None, 'não achei linhas de data/hora no Excel'
        d.columns = ['t', 'v']; d['v'] = d.v.astype(str).str.replace(',', '.')
    else:
        txt = open(path, encoding='utf-8-sig', errors='replace').read()
        if '<table' in txt[:20000].lower() or '<html' in txt[:2000].lower():
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', txt, re.S)
            d = pd.DataFrame([re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S) for r in rows][1:]).iloc[:, :2]; d.columns = ['t', 'v']; d['v'] = d.v.astype(str).str.replace(',', '.')
        else:
            d = pd.read_csv(path, sep=';', decimal=',', encoding='utf-8-sig').iloc[:, :2]; d.columns = ['t', 'v']
    d['t'] = pd.to_datetime(d.t, errors='coerce'); d['v'] = pd.to_numeric(d.v, errors='coerce'); d = d.dropna().astype({'v': float})
    if len(d): print(f'  {os.path.basename(path)}: {len(d)} leituras, {d.t.min()} a {d.t.max()}, mediana {d.v.median():.2f}')
    if len(d) and d.v.median() > 20: d['v'] = d.v / 100   # série do app em metros; Hydromet pode exportar em cm
    return d

def bloco(s):
    m = [m for m in re.finditer(r'<script>window\.TC_HARM=(\{.*?\});?\s*</script>', s, re.S)]
    assert len(m) == 1, 'bloco TC_HARM não encontrado'; return m[0]

def rodape(s, ate):
    s = re.sub(r'(Atualizado em|Dados até) [\d/]+( \d\d:\d\d)? · v[\d.]+', f'Dados até {ate} · v{VERSAO}', s)
    if 'id="refreshData"' not in s:
        s = s.replace('<button class="textbutton" id="download">', '<button class="textbutton" id="refreshData" type="button">Atualizar</button><button class="textbutton" id="download">', 1)
        s = s.replace('</body>', '<script>document.getElementById("refreshData").onclick=function(){this.textContent="Atualizando…";location.replace(location.pathname+"?v="+Date.now());};</script></body>', 1)
    return s

def processa(nome, cfg):
    pag = os.path.join(RAIZ, cfg['pagina']); s = open(pag, encoding='utf-8').read(); m = bloco(s); H = json.loads(m.group(1))
    serie = os.path.join(AQUI, 'dados', f'serie_{nome}.csv'); base = pd.read_csv(serie, sep=';', decimal=',', encoding='utf-8-sig', parse_dates=['t'])
    arqs = sorted(f for f in glob.glob(os.path.join(AQUI, 'entrada', nome, '*')) if os.path.isfile(f) and not f.endswith('.md'))
    if not arqs: print(f'[{nome}] sem arquivo novo'); return False
    novos = [ler(a) for a in arqs]
    all_ = pd.concat([base] + novos).drop_duplicates('t', keep='last').sort_values('t').reset_index(drop=True)
    if len(all_) < len(base) or all_.t.max() < base.t.max(): print(f'[{nome}] série nova menor que a anterior; parei'); return False
    if len(all_) == len(base): print(f'[{nome}] nenhuma leitura nova'); [os.remove(a) for a in arqs]; return False
    print(f'[{nome}] {len(base)} -> {len(all_)} leituras; última {all_.t.max()}')
    NR = H['nr_cm']; S0 = H['S0_anual']; pr = predictor(H['comps'], S0); NRm = NR
    # picos espúrios
    rem = []
    if cfg['filtro'] == 'residuo':
        x = all_[all_.t >= cfg['desde']]
        for _ in range(2):
            xx = x[~x.t.isin(rem)]; r = pd.Series(xx.v.values * 100 - pr(xx.t.values.astype('datetime64[s]')), index=xx.t)
            med = r.rolling('3h', center=True, min_periods=3).median(); rem += list(r.index[(r - med).abs() > 30])
    else:
        v = all_.v.values; sd = np.abs(v[1:-1] - (v[:-2] + v[2:]) / 2); rem = list(all_.t.values[1:-1][sd > 0.30])
    clean = all_[~all_.t.isin(rem)].reset_index(drop=True); print(f'[{nome}] picos removidos: {len(rem)}')
    E0 = np.datetime64('2024-01-01T00:00:00').astype('datetime64[s]').astype(np.int64)
    oe = observed_extremes(clean); t = clean.t.values.astype('datetime64[s]').astype(np.int64)
    cut = np.where(np.diff(t) / 60 > 90)[0] + 1; st = np.r_[0, cut]; en = np.r_[cut, len(t)]; ev = []
    for a, b in zip(st, en):
        if b - a < 4: continue
        g = np.arange(math.ceil(t[a] / 300) * 300, t[b - 1] + 1, 300)
        if len(g) < 10: continue
        ep = swing(g, pr(g.astype('datetime64[s]')))
        for ta, va, ty, lr in [e for e in oe if g[0] <= e[0] <= g[-1]]:
            c_ = [e for e in ep if e[2] == ty]
            if not c_: continue
            k = min(c_, key=lambda e: abs(e[0] - ta)); d_ = (k[0] - ta) / 60
            if abs(d_) <= 180: ev.append([int(round((ta - E0) / 60)), 0 if ty == 'PM' else 1, int(round(va * 10 - NR * 10)), int(round(k[1] * 10 - NR * 10)), int(round(d_)), lr])
    ev.sort()
    if not cfg['recalcula_antigos']:
        lim = (np.datetime64(cfg['desde']) - np.datetime64('2024-01-01T00:00')) / np.timedelta64(1, 'm'); keys = {tuple(e[:2]) for e in ev}
        for e in H['ev']:
            if e[0] < lim and tuple(e[:2]) not in keys: ev.append(e[:5] + [0])
        ev.sort()
    def gapf(ta):
        i0 = np.searchsorted(t, ta - WIN); i1 = np.searchsorted(t, ta + WIN); xs = t[i0:i1]
        return np.diff(np.r_[ta - WIN, xs, ta + WIN]).max() / 60 if len(xs) else 9999
    evn = [e[:5] + [int(t[0] <= E0 + e[0] * 60 <= t[-1] and gapf(E0 + e[0] * 60) > GAP)] for e in ev]
    print(f'[{nome}] marés {len(evn)}; reprovadas {sum(e[5] for e in evn)}')
    d = pd.DataFrame(evn, columns=['m', 'ty', 'o', 'p', 'dt', 'lr']); d['mo'] = (pd.Timestamp('2024-01-01') + pd.to_timedelta(d.m, unit='m')).dt.strftime('%Y-%m'); d['eh'] = (d.p - d.o) / 10
    a = all_.copy(); a['mo'] = a.t.dt.strftime('%Y-%m'); a['slot'] = a.t.dt.floor(f"{cfg['passo']}min"); qc = []
    for mo, gp in a.groupby('mo'):
        p = pd.Period(mo); s0 = max(p.start_time, a.t.min()); s1 = min(p.end_time, a.t.max()); tot = int((s1 - s0).total_seconds() // (cfg['passo'] * 60)) + 1
        gg = (gp.t.diff().dt.total_seconds() / 3600).max(); sp = sum(1 for r in rem if pd.Timestamp(r).strftime('%Y-%m') == mo)
        dm = d[d.mo == mo]; vv = dm[dm.lr == 0]
        qc.append([mo, round(gp.slot.nunique() / tot * 100, 1), round(float(gg) if gg == gg else 0, 1), sp, len(dm), len(vv), round(float(vv.eh.mean()), 1) if len(vv) else None, round(float((vv.eh ** 2).mean() ** .5), 1) if len(vv) else None])
    H['obs'] = hourly(clean); H['ev'] = evn; H['qc'] = qc
    ini, fim = all_.t.min(), all_.t.max(); f = lambda x: x.strftime('%d/%m/%Y %H:%M')
    H['metodo']['dados'] = re.sub(r'de \d\d/\d\d/\d{4} \d\d:\d\d a \d\d/\d\d/\d{4} \d\d:\d\d|até \d\d/\d\d/\d{4}( \d\d:\d\d)?', lambda mm: (f'de {f(ini)} a {f(fim)}' if mm.group(0).startswith('de') else f'até {f(fim)}'), H['metodo']['dados'], count=1)
    H['ultimo'] = f(fim)
    s = s[:m.start()] + '<script>window.TC_HARM=' + json.dumps(H, ensure_ascii=False, separators=(',', ':')) + ';</script>' + s[m.end():]
    s = rodape(s, f(fim))
    open(pag, 'w', encoding='utf-8').write(s)
    all_.to_csv(serie, sep=';', decimal=',', index=False, date_format='%Y-%m-%d %H:%M:%S', encoding='utf-8-sig')
    os.makedirs(os.path.join(AQUI, 'entrada', nome, 'processados'), exist_ok=True)
    for a_ in arqs: shutil.move(a_, os.path.join(AQUI, 'entrada', nome, 'processados', os.path.basename(a_)))
    return True

if __name__ == '__main__':
    if '--so-pagina' in sys.argv:
        for n, cfg in EST.items():
            pag = os.path.join(RAIZ, cfg['pagina']); u = pd.read_csv(os.path.join(AQUI, 'dados', f'serie_{n}.csv'), sep=';', decimal=',', encoding='utf-8-sig', parse_dates=['t']).t.max()
            novo = rodape(open(pag, encoding='utf-8').read(), u.strftime('%d/%m/%Y %H:%M')); open(pag, 'w', encoding='utf-8').write(novo)
        sys.exit(0)
    nomes = sys.argv[1:] or list(EST); ok = [processa(n, EST[n]) for n in nomes]
    sys.exit(0 if any(ok) else 3)
