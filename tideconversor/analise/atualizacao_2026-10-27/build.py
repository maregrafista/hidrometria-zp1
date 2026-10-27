import sys,json,pickle,collections
U='/private/tmp/claude-501/-Users-cooperativaunipilot-Mare-Fazendinha-PACMARE/4e3db02b-a924-4939-8e24-c594f1ccf739/scratchpad/upd'
sys.path.insert(0,U)
from hourly import *; from events import *
P='/Users/cooperativaunipilot/Mare_Fazendinha_PACMARE/tideconversorv2/data/harm.js'
s=open(P,encoding='utf-8').read(); H=json.loads(s[s.index('=')+1:].rstrip(';\n'))
all_,_=pickle.load(open(U+'/new.pkl','rb')); pr=predictor(H['comps'],H['S0_anual']); NR=H['nr_cm']
# --- remoção de picos espúrios no trecho de registro irregular (a partir de 01/08/2026)
x=all_[all_.t>='2026-08-01']; rem=[]
for it in range(2):
    xx=x[~x.t.isin(rem)]; r=pd.Series(xx.v.values*100-pr(xx.t.values.astype('datetime64[s]')),index=xx.t)
    med=r.rolling('3h',center=True,min_periods=3).median(); bad=(r-med).abs()>30; rem+=list(r.index[bad])
print('picos removidos',len(rem))
clean=all_[~all_.t.isin(rem)].reset_index(drop=True)
E0=np.datetime64('2024-01-01T00:00:00').astype('datetime64[s]').astype(np.int64)
oe=observed_extremes(clean)
t=clean.t.values.astype('datetime64[s]').astype(np.int64); cut=np.where(np.diff(t)/60>90)[0]+1; st=np.r_[0,cut]; en=np.r_[cut,len(t)]
ev=[]
for a,b in zip(st,en):
    if b-a<4: continue
    g=np.arange(math.ceil(t[a]/300)*300,t[b-1]+1,300)
    if len(g)<10: continue
    ep=swing(g,pr(g.astype('datetime64[s]')))
    for ta,va,ty,lr in [e for e in oe if g[0]<=e[0]<=g[-1]]:
        c_=[x_ for x_ in ep if x_[2]==ty]
        if not c_: continue
        k=min(c_,key=lambda x_:abs(x_[0]-ta)); dt=(k[0]-ta)/60
        if abs(dt)<=180: ev.append([int(round((ta-E0)/60)),0 if ty=='PM' else 1,int(round(va*10-NR*10)),int(round(k[1]*10-NR*10)),int(round(dt)),lr])
ev.sort()
Em=np.datetime64('2024-01-01T00:00'); lim=(np.datetime64('2026-08-01')-Em)/np.timedelta64(1,'m')
keys={tuple(e[:2]) for e in ev}
for e in H['ev']:
    if e[0]<lim and tuple(e[:2]) not in keys: ev.append(e[:5]+[0])
ev.sort()
g=collections.defaultdict(list)
for e in ev: g[str(Em+np.timedelta64(e[0],'m'))[:7]].append(e)
rm=lambda l:(sum(((e[3]-e[2])/10)**2 for e in l)/len(l))**.5
for k in ['2024-12','2025-01','2026-01','2026-07','2026-08','2026-09','2026-10']: print(k,len(g[k]),round(rm(g[k]),1),'lr',sum(e[5] for e in g[k]),'viés',round(np.mean([(e[3]-e[2])/10 for e in g[k]]),1))
print(len(ev),'total; lowres',sum(e[5] for e in ev))
pickle.dump((clean,ev,rem),open(U+'/new3.pkl','wb'))
