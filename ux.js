(()=>{'use strict';
const root=document.documentElement,viewport=document.querySelector('meta[name="viewport"]');
const mobileButton=document.getElementById('view-mobile'),desktopButton=document.getElementById('view-desktop');
const installButton=document.getElementById('install-app'),dialog=document.getElementById('install-dialog');
let preference='auto',deferredInstall=null;
try{preference=localStorage.getItem('rios-zp1-layout')||'auto'}catch{}
if(!['auto','mobile','desktop'].includes(preference))preference='auto';
const physicalPhone=()=>matchMedia('(pointer: coarse)').matches&&screen.width<=800;
const effective=()=>preference==='auto'?(matchMedia('(max-width: 800px)').matches?'mobile':'desktop'):preference;
function renderLayout(){const mode=effective();root.dataset.layout=preference==='auto'?'auto':mode;viewport.content=mode==='desktop'&&physicalPhone()?'width=1024,initial-scale=1,viewport-fit=cover':'width=device-width,initial-scale=1,viewport-fit=cover';mobileButton.setAttribute('aria-pressed',String(mode==='mobile'));desktopButton.setAttribute('aria-pressed',String(mode==='desktop'));mobileButton.title=mode==='mobile'?'Visualização celular ativa':'Usar visualização celular';desktopButton.title=mode==='desktop'?'Visualização computador ativa':'Usar visualização computador'}
function setLayout(mode){preference=mode;try{localStorage.setItem('rios-zp1-layout',mode)}catch{}renderLayout()}
mobileButton.addEventListener('click',()=>setLayout('mobile'));
desktopButton.addEventListener('click',()=>setLayout('desktop'));
matchMedia('(max-width: 800px)').addEventListener('change',()=>{if(preference==='auto')renderLayout()});
renderLayout();
const standalone=()=>matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
function instructions(){const ua=navigator.userAgent,inApp=/WhatsApp|Instagram|FBAN|FBAV/i.test(ua);if(inApp)return 'Abra este link no navegador do telefone. No Android, use o Chrome; no iPhone, use o Safari. Depois toque em “Instalar app” novamente.';if(/iPhone|iPad|iPod/i.test(ua))return 'No Safari, toque em Compartilhar e escolha “Adicionar à Tela de Início”. Se aparecer, ative “Abrir como App” e toque em Adicionar.';if(/Android/i.test(ua))return 'No Chrome, abra o menu ⋮ e escolha “Instalar app” ou “Adicionar à tela inicial”. Confirme a instalação.';return 'Use o menu do navegador e escolha “Instalar Rios ZP-1” ou “Criar atalho”. No celular, abra este link no Chrome (Android) ou Safari (iPhone).'}
function showInstructions(){document.getElementById('install-instructions').textContent=instructions();if(!dialog.open)dialog.showModal()}
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();deferredInstall=event});
window.addEventListener('appinstalled',()=>{deferredInstall=null;installButton.hidden=true});
if(standalone())installButton.hidden=true;
installButton.addEventListener('click',async()=>{if(deferredInstall){const prompt=deferredInstall;deferredInstall=null;await prompt.prompt();return}showInstructions()});
document.getElementById('install-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
if(new URLSearchParams(location.search).has('instalar')&&!standalone())window.addEventListener('load',showInstructions,{once:true});
})();
