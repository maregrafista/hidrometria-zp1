(function(root){'use strict';
const DAY=86400000,stamp=d=>Date.parse(d.slice(0,10)+'T00:00:00Z'),iso=t=>new Date(t).toISOString().slice(0,10),add=(d,n)=>iso(stamp(d)+n*DAY);
const round=x=>x==null?null:Math.round(x*10000)/10000;
const q=(a,p)=>{if(!a.length)return null;const v=[...a].sort((x,y)=>x-y),i=(v.length-1)*p,j=Math.floor(i);return v[j]+(v[Math.min(j+1,v.length-1)]-v[j])*(i-j)};
const doy=d=>{const y=d.slice(0,4);return Math.round((stamp(d)-stamp(y+'-01-01'))/DAY)+1};
const byMonthDay=(map,year,monthDay)=>{const target=stamp(year+'-'+monthDay);for(const k of [0,-1,1,-2,2]){const r=map.get(iso(target+k*DAY));if(r?.valid)return r.value}return null};
function calculate(meta,input){
 const raw=new Map();for(const [ts,v] of input){if(!/^\d{4}-\d\d-\d\dT\d\d:\d\d/.test(ts)||!Number.isFinite(+v))continue;raw.set(ts,Number(v))}
 const days=new Map();for(const [ts,value] of raw){const d=ts.slice(0,10),old=days.get(d);if(!old||ts>old.ts)days.set(d,{date:d,ts,value,valid:value>=-10&&value<=40,flags:value>=-10&&value<=40?[]:['faixa_atipica']});else if(ts===old.ts&&value!==old.value){old.valid=false;old.flags.push('conflito_mesmo_horario')}}
 const series=[...days.values()].sort((a,b)=>a.date.localeCompare(b.date));
 for(let i=1;i<series.length;i++){const r=series[i],p=series[i-1],gap=(stamp(r.date)-stamp(p.date))/DAY;if(r.valid&&p.valid&&gap<=2&&Math.abs(r.value-p.value)/gap>.8){r.valid=false;r.flags.push('salto_a_revisar')}}
 const map=new Map(series.map(r=>[r.date,r]));const last=[...series].reverse().find(r=>r.valid);if(!last)return {meta,series,forecast:[],rates:[],status:'Sem leitura válida'};
 const cut=last.date,monthly=cut.slice(5),rates=[1,7,15,30,182,365].map(n=>{const p=map.get(add(cut,-n)),delta=p?.valid?round(last.value-p.value):null;return {days:n,delta,cmDay:delta===null?null:round(delta*100/n)}});
 function slopeAt(day){const pts=[];for(let k=0;k<15;k++){const r=map.get(add(day,k-14));if(r?.valid)pts.push([k,r.value])}if(pts.length<10)return null;const xm=pts.reduce((s,r)=>s+r[0],0)/pts.length,ym=pts.reduce((s,r)=>s+r[1],0)/pts.length;const top=pts.reduce((s,r)=>s+(r[0]-xm)*(r[1]-ym),0),bot=pts.reduce((s,r)=>s+(r[0]-xm)**2,0);return top/bot}
 const slope=slopeAt(cut),analog=[];
 for(let y=2020;y<=2025;y++){const ref=byMonthDay(map,y,monthly);if(ref===null)continue;const back=byMonthDay(map,y,add(cut,-15).slice(5)),trend=back===null?null:(ref-back)/15;analog.push({year:y,ref,trend,weight:trend===null||slope===null?1:Math.exp(-Math.abs(trend-slope)/.055)})}
 const end='2026-12-31',forecast=[];let err=[];
 for(let y=2020;y<=2025;y++)for(let d=stamp(y+'-02-01');d<=stamp(y+'-11-30');d+=7*DAY){const origin=iso(d),h=map.get(origin),s=slopeAt(origin),future=map.get(iso(d+7*DAY));if(h?.valid&&future?.valid&&s!==null)err.push(future.value-(h.value+7*s))}
 const loErr=err.length>=25?q(err,.025):null,hiErr=err.length>=25?q(err,.975):null;
 for(let d=stamp(cut)+DAY;d<=stamp(end);d+=DAY){const date=iso(d),lead=(d-stamp(cut))/DAY,paths=[];for(const a of analog){const v=byMonthDay(map,a.year,date.slice(5));if(v!==null)paths.push({value:last.value+v-a.ref,weight:a.weight})}if(paths.length<3)continue;const sum=paths.reduce((s,p)=>s+p.weight,0),analogMean=paths.reduce((s,p)=>s+p.value*p.weight,0)/sum;
  const local=slope===null?analogMean:last.value+slope*lead,blend=lead<=7?Math.exp(-lead/8):Math.exp(-lead/4),value=blend*local+(1-blend)*analogMean;
  let low=null,high=null;if(lead<=7&&loErr!==null){low=value+loErr*Math.sqrt(lead/7);high=value+hiErr*Math.sqrt(lead/7)}else if(paths.length>=4){low=q(paths.map(p=>p.value),.025);high=q(paths.map(p=>p.value),.975)}
  forecast.push({date,value:round(value),lower:round(low),upper:round(high),n:paths.length,kind:lead<=7?'short':'analog'});
 }
 const historical=[];for(let y=2020;y<=2025;y++){const vals=[];for(let off=-7;off<=7;off++){const v=byMonthDay(map,y,add(cut,off).slice(5));if(v!==null)vals.push(v)}if(vals.length>=10)historical.push(vals.reduce((a,b)=>a+b)/vals.length)}
 let z=null;if(historical.length>=4){const m=historical.reduce((a,b)=>a+b)/historical.length,sd=Math.sqrt(historical.reduce((a,b)=>a+(b-m)**2,0)/(historical.length-1));if(sd>0)z=(last.value-m)/sd}
 const min2026=series.filter(r=>r.valid&&r.date.startsWith('2026')).reduce((a,r)=>!a||r.value<a.value?r:a,null);
 const annualPeak=forecast.reduce((a,r)=>!a||r.value>a.value?r:a,null);
 const sipamDelta=meta.sipam15,local15=rates[2].delta==null?null:round(rates[2].delta*100);
 return {meta,series,last,cut,rates,forecast,analogYears:analog.map(a=>a.year),slope:round(slope),z:round(z),historicalN:historical.length,min2026,annualPeak,bulletin:{deltaCm:sipamDelta,localCm:local15,agreement:local15===null||sipamDelta===null?null:Math.sign(local15)===Math.sign(sipamDelta)},quality:{input:input.length,dates:series.length,flagged:series.filter(r=>!r.valid).length},method:{hindcastErrors:err.length,analogs:analog.length}};
}
root.HydroAnalytics={calculate,add,stamp,iso,q,round};
})(typeof window!=='undefined'?window:globalThis);
