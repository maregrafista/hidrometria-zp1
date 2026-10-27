import sys, json, math
sys.path.insert(0,'/Users/cooperativaunipilot/Mare_Fazendinha_PACMARE/pacmare')
import numpy as np, pandas as pd, blocos
def hourly(df):
    t=df.t.values.astype('datetime64[s]').astype(np.int64); v=df.v.values*100.0
    h0=np.datetime64('2024-01-01T00:00:00').astype(np.int64)
    hs=np.arange(math.ceil((t[0]-h0)/3600),math.floor((t[-1]-h0)/3600)+1)
    sec=h0+hs*3600; j=np.searchsorted(t,sec); ok=(j>0)&(j<len(t)); val=np.full(len(hs),np.nan)
    for i in np.where(ok)[0]:
        a,b=j[i]-1,j[i]
        if t[b]==sec[i]: val[i]=v[b]
        elif (t[b]-t[a])<=3600: val[i]=v[a]+(v[b]-v[a])*(sec[i]-t[a])/(t[b]-t[a])
    idx=np.where(~np.isnan(val))[0]; runs=[]; prev=None; cur=[]; start=None
    for i in idx:
        if prev is not None and i==prev+1: cur.append(int(round(val[i])))
        else:
            if cur: runs.append([int(hs[start]),cur])
            start=i; cur=[int(round(val[i]))]
        prev=i
    if cur: runs.append([int(hs[start]),cur])
    return runs
def load_csv(p):
    c=pd.read_csv(p,sep=';',decimal=',',encoding='utf-8-sig'); c.columns=['t','v']; c['t']=pd.to_datetime(c.t); c['v']=pd.to_numeric(c.v,errors='coerce'); return c.dropna()
