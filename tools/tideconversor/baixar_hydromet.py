#!/usr/bin/env python3
"""Baixa do Hydromet Cloud as leituras RLS de Fazendinha e Curuá e salva em entrada/<estacao>/.

Credenciais só no ambiente: HYDROMET_USER e HYDROMET_PASS (segredos do GitHub). Nada é gravado em arquivo.
Uso: python3 baixar_hydromet.py [--dias 4] [--inspecionar] [fazendinha] [curua]
Em caso de erro, salva tela e HTML em debug/ (sem a senha) para diagnóstico.
"""
import os, sys, argparse, datetime as dt
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__)); DEBUG = os.path.join(AQUI, '..', '..', 'debug')
URL = 'https://www.hydrometcloud.com/hydrometcloud/index.jsp?menu=index'
REL = 'https://www.hydrometcloud.com/hydrometcloud/jsp/CustomReport/CustomReports.jsp?menu=CustomReports'
ESTACOES = {  # nome no app -> (estação na árvore, sensor)
  'fazendinha': ('Atalaia_Fazendinha', 'RLS'),
  'curua': ('PONTA_DO_CÉU_I', os.environ.get('HYDROMET_SENSOR_CURUA', 'RADAR')),   # sensor do Curuá: confirmar na primeira execução
}
JS_NO = "(t)=>[...document.querySelectorAll('a.dynatree-title')].find(e=>e.textContent.trim()===t)"

def clica_no(pg, titulo, parte):
    ok = pg.evaluate(f"""(t)=>{{const a=({JS_NO})(t); if(!a) return false; const e=a.parentElement.querySelector('.dynatree-{parte}'); if(!e) return false; e.click(); return true}}""", titulo)
    if not ok: raise RuntimeError(f'nó não encontrado na árvore: {titulo}')
    pg.wait_for_timeout(600)

def existe(pg, titulo): return pg.evaluate(f"(t)=>!!({JS_NO})(t)", titulo)

def baixar(pg, nome, dias, saida):
    estacao, sensor = ESTACOES[nome]
    pg.goto(REL); pg.wait_for_load_state('networkidle'); pg.wait_for_selector('a.dynatree-title')
    if not existe(pg, estacao): clica_no(pg, 'UNIPLOT', 'expander')
    if not existe(pg, sensor): clica_no(pg, estacao, 'expander')
    clica_no(pg, sensor, 'checkbox')
    agora = dt.datetime.now(ZoneInfo('America/Belem')).replace(tzinfo=None)
    pg.locator('label[for=customTime]').click()
    pg.fill('#fromFld', (agora - dt.timedelta(days=dias)).strftime('%Y-%m-%d %H:%M')); pg.fill('#toFld', (agora + dt.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'))
    pg.select_option('#dataorder', 'ascending')
    with pg.expect_download(timeout=120000) as d: pg.locator('button.data-reports', has_text='Excel').click()
    os.makedirs(os.path.join(AQUI, 'entrada', nome), exist_ok=True)
    alvo = os.path.join(AQUI, 'entrada', nome, f'rls_{agora:%Y%m%d_%H%M}.xls'); d.value.save_as(alvo)
    print(f'[{nome}] baixado: {alvo} ({os.path.getsize(alvo)} bytes)')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dias', type=int, default=4); ap.add_argument('--inspecionar', action='store_true'); ap.add_argument('estacoes', nargs='*'); a = ap.parse_args()
    u, p = os.environ.get('HYDROMET_USER'), os.environ.get('HYDROMET_PASS')
    if not (u and p): sys.exit('Defina HYDROMET_USER e HYDROMET_PASS no ambiente.')
    os.makedirs(DEBUG, exist_ok=True); falhas = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=not a.inspecionar); ctx = br.new_context(accept_downloads=True, locale='pt-BR', timezone_id='America/Belem'); pg = ctx.new_page(); pg.set_default_timeout(30000)
        try:
            pg.goto(URL); pg.get_by_role('button', name='Login').first.click(); pg.fill('#userName', u); pg.fill('#password', p); pg.locator('#lgn button[type=submit]').click(); pg.wait_for_load_state('networkidle')
            if 'Guest' in pg.inner_text('body'): raise RuntimeError('login recusado')
        except Exception as e:
            pg.screenshot(path=os.path.join(DEBUG, 'login.png')); sys.exit(f'Falha no login: {type(e).__name__}')
        for n in (a.estacoes or ESTACOES):
            try: baixar(pg, n, a.dias, AQUI)
            except Exception as e:
                falhas.append(n); print(f'[{n}] FALHOU: {type(e).__name__}: {str(e)[:200]}')
                pg.screenshot(path=os.path.join(DEBUG, f'{n}.png'), full_page=True); open(os.path.join(DEBUG, f'{n}.html'), 'w', encoding='utf-8').write(pg.content())
        br.close()
    sys.exit(1 if len(falhas) == len(a.estacoes or ESTACOES) else 0)
if __name__ == '__main__': main()
