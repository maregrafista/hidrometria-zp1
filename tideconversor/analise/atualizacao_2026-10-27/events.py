import sys, json, math
sys.path.insert(0,'/Users/cooperativaunipilot/Mare_Fazendinha_PACMARE/pacmare/harmonica/scripts')
import numpy as np
from harm import astro, nodal
D2R=math.pi/180
def predictor(comps, S0):
    def pred(t_local):          # t_local: datetime64[s] array, hora local (UTC-3)
        t=np.asarray(t_local,dtype='datetime64[s]'); a=astro(t); f,u=nodal(a['N']); out=np.full(len(t),float(S0))
        for c in comps:
            F=np.ones(len(t)); U=np.zeros(len(t))
            for k,ab,sg in c['k']: F=F*f[k]**ab; U=U+sg*u[k]
            arg=c['c'][0]*a['T']+c['c'][1]*a['s']+c['c'][2]*a['h']+c['c'][3]*a['p']+c['c'][4]*a['p1']+c['o']+U/D2R
            out+=F*c['H']*np.cos((arg-c['g'])*D2R)
        return out
    return pred
def pchip(x,y,xi):
    h=np.diff(x); d=np.diff(y)/h; n=len(x); m=np.zeros(n)
    if n==2: m[:]=d[0]
    else:
        for i in range(1,n-1):
            if d[i-1]*d[i]>0:
                w1=2*h[i]+h[i-1]; w2=h[i]+2*h[i-1]; m[i]=(w1+w2)/(w1/d[i-1]+w2/d[i])
        def end(h0,h1,d0,d1):
            s=((2*h0+h1)*d0-h0*d1)/(h0+h1)
            if np.sign(s)!=np.sign(d0): s=0
            elif np.sign(d0)!=np.sign(d1) and abs(s)>3*abs(d0): s=3*d0
            return s
        m[0]=end(h[0],h[1],d[0],d[1]); m[-1]=end(h[-1],h[-2],d[-1],d[-2])
    k=np.clip(np.searchsorted(x,xi)-1,0,n-2); t=(xi-x[k])/h[k]
    h00=2*t**3-3*t**2+1; h10=t**3-2*t**2+t; h01=-2*t**3+3*t**2; h11=t**3-t**2
    return h00*y[k]+h10*h[k]*m[k]+h01*y[k+1]+h11*h[k]*m[k+1]
def swing(t,v,thr=40.0):
    out=[]; hi=lo=0; d=0
    for i in range(1,len(v)):
        if v[i]>v[hi]: hi=i
        if v[i]<v[lo]: lo=i
        if d>=0 and v[hi]-v[i]>=thr: out.append((hi,'PM')); d=-1; lo=i
        elif d<=0 and v[i]-v[lo]>=thr: out.append((lo,'BM')); d=1; hi=i
    return [(t[i],v[i],ty,i) for i,ty in out]
def observed_extremes(df, gap_max=90, lowres_min=20):
    """df: t (datetime64), v (m). Retorna lista (t_local_s, valor_cm, tipo, lowres)"""
    t=df.t.values.astype('datetime64[s]').astype(np.int64); v=df.v.values*100.0; out=[]
    cut=np.where(np.diff(t)/60>gap_max)[0]+1; st=np.r_[0,cut]; en=np.r_[cut,len(t)]
    for a,b in zip(st,en):
        if b-a<4: continue
        tt=t[a:b]; vv=v[a:b]; g=np.arange(math.ceil(tt[0]/300)*300, tt[-1]+1, 300)
        if len(g)<10: continue
        gap=np.diff(tt)/60; lin=np.interp(g,tt,vv)
        if gap.max()>lowres_min:
            cub=pchip(tt.astype(float),vv,g.astype(float)); k=np.clip(np.searchsorted(tt,g)-1,0,len(gap)-1); sp=gap[k]; vi=np.where(sp>lowres_min,cub,lin)
        else: sp=np.full(len(g),gap.max() if len(gap) else 0); vi=lin; k=np.clip(np.searchsorted(tt,g)-1,0,len(gap)-1); sp=gap[k]
        sw=swing(g,vi)
        for n_,(tg,val,ty,i) in enumerate(sw):
            spi=sp[min(i,len(sp)-1)]
            if n_==0 and len(sw)>1 and (g[0]+2700>tg or True): continue          # o primeiro "extremo" de um trecho pode ser só o início do trecho
            if tg<g[0]+2700 or tg>g[-1]-2700 or spi>65: continue
            out.append((int(tg),float(val),ty,int(spi>lowres_min)))
    return out
