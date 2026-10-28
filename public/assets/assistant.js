(function conciergeClient() {
  'use strict';
  if (document.querySelector('[data-ef-concierge]')) return;
  const svg = (name, size=18) => {
    const shapes = {
      close:'<path d="M5 5 19 19M19 5 5 19"/>',
      send:'<path d="m21 3-9 18-3.3-7.7L1 10l20-7Z"/><path d="M9 13.3 21 3"/>',
      arrow:'<path d="M5 12h14m-7-7 7 7-7 7"/>',
      shield:'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
      check:'<path d="m5 12 4.5 4.5L19 7"/>'
    };
    return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${shapes[name]}</svg>`;
  };
  const root = document.createElement('div');
  root.className='ef-concierge';
  root.dataset.efConcierge='';
  root.innerHTML=`
    <div class="efc-tip" data-ef-tip hidden>
      <button class="efc-tip-main" data-ef-tip-open type="button"><strong>¿Necesitás ayuda con tu auto?</strong><span>Estoy acá para orientarte.</span></button>
      <button class="efc-tip-close" data-ef-tip-dismiss type="button" aria-label="Cerrar sugerencia">${svg('close',14)}</button>
    </div>
    <section class="efc-panel" data-ef-panel hidden role="dialog" aria-modal="false" aria-label="Asistente virtual de Euro Factory">
      <header class="efc-head">
        <div class="efc-avatar"><img src="/assets/eurofactory-icon.webp" alt="" width="44" height="44"></div>
        <div class="efc-identity"><span>EURO FACTORY</span><strong>Asistente virtual</strong><small><i></i> Servicios · Dudas · Citas</small></div>
        <button class="efc-close" data-ef-close aria-label="Cerrar asistente" type="button">${svg('close',20)}</button>
      </header>
      <div class="efc-log" data-ef-log role="log" aria-live="polite" aria-relevant="additions">
        <div class="efc-message efc-message--assistant"><span>¡Hola! Soy el asistente virtual de Euro Factory. Te puedo orientar con nuestros servicios o ayudarte a solicitar una cita en Maracay o Valencia. ¿En qué te ayudo?</span></div>
        <div class="efc-chips" data-ef-chips>
          <button type="button" data-ef-prompt="Quiero solicitar una cita para mi vehículo">Quiero una cita ${svg('arrow',14)}</button>
          <button type="button" data-ef-prompt="¿Qué servicios ofrecen?">Ver servicios ${svg('arrow',14)}</button>
          <button type="button" data-ef-prompt="¿Dónde están ubicadas las dos sedes?">Sedes y horarios ${svg('arrow',14)}</button>
        </div>
      </div>
      <div class="efc-ready" data-ef-ready hidden>
        <div class="efc-ready-header"><span class="efc-ready-icon">${svg('check',18)}</span><span><strong>Tu solicitud está lista</strong><small data-ef-ready-caption>Para enviar al taller</small></span></div>
        <a data-ef-wa class="efc-whatsapp" href="#" target="_blank" rel="noopener noreferrer">Enviar solicitud por WhatsApp ${svg('arrow',17)}</a>
        <p>El equipo confirmará disponibilidad. No es una reserva automática.</p>
      </div>
      <form class="efc-form" data-ef-form>
        <label for="ef-chat-input" class="efc-sr">Escribí tu consulta</label>
        <textarea id="ef-chat-input" data-ef-input rows="1" maxlength="1000" placeholder="Contame qué necesitás..." enterkeyhint="send" required></textarea>
        <button class="efc-send" data-ef-send type="submit" aria-label="Enviar mensaje">${svg('send',19)}</button>
      </form>
      <div class="efc-privacy">${svg('shield',13)} Asistente con IA · Tus datos se usan para responder y preparar tu consulta.</div>
    </section>
    <button class="efc-fab" data-ef-fab aria-label="Abrir asistente virtual de Euro Factory" aria-expanded="false" type="button">
      <span class="efc-halo"></span>
      <img src="/assets/eurofactory-icon.webp" alt="Euro Factory" width="53" height="53">
      <span class="efc-dot"></span>
    </button>`;
  document.body.appendChild(root);
  document.body.classList.add('has-ef-assistant');
  const $ = name => root.querySelector('[data-ef-'+name+']');
  const panel=$('panel'),fab=$('fab'),tip=$('tip'),log=$('log'),form=$('form'),input=$('input'),
        send=$('send'),chips=$('chips'),ready=$('ready'),wa=$('wa');
  let isOpen=false,interacted=false,loading=false,history=[],
      lead={branch:'',name:'',vehicle:'',service:'',date:'',phone:''},wantsAppointment=false;
  function open(){
    interacted=true;tip.hidden=true;panel.hidden=false;isOpen=true;
    fab.setAttribute('aria-expanded','true');fab.setAttribute('aria-label','Cerrar asistente');
    root.classList.add('efc-open');
    requestAnimationFrame(()=>{log.scrollTop=log.scrollHeight;input.focus({preventScroll:true});});
  }
  function close(){
    panel.hidden=true;isOpen=false;root.classList.remove('efc-open');
    fab.setAttribute('aria-expanded','false');fab.setAttribute('aria-label','Abrir asistente virtual de Euro Factory');
    fab.focus({preventScroll:true});
  }
  fab.addEventListener('click',()=>isOpen?close():open());
  $('close').addEventListener('click',close);
  $('tip-open').addEventListener('click',open);
  $('tip-dismiss').addEventListener('click',()=>{interacted=true;tip.hidden=true;});
  document.addEventListener('keydown',e=>{if(isOpen&&e.key==='Escape'){e.preventDefault();close();}});
  window.setTimeout(()=>{if(!interacted&&!isOpen&&document.visibilityState==='visible')tip.hidden=false;},45000);

  function bubble(text,kind){
    const d=document.createElement('div'),t=document.createElement('span');
    d.className='efc-message efc-message--'+kind;t.textContent=text;d.append(t);log.append(d);
    log.scrollTop=log.scrollHeight;
  }
  async function submit(text){
    text=(text||'').trim();
    if(!text||loading)return;
    chips.hidden=true;ready.hidden=true;loading=true;send.disabled=input.disabled=true;
    bubble(text,'user');input.value='';input.style.height='';
    const typing=document.createElement('div');typing.className='efc-typing';typing.setAttribute('role','status');
    typing.setAttribute('aria-label','El asistente está escribiendo');
    typing.innerHTML='<i></i><i></i><i></i>';log.append(typing);log.scrollTop=log.scrollHeight;
    try{
      const abort=new AbortController(),timer=setTimeout(()=>abort.abort(),28000);
      let response;
      try {
        response=await fetch('/api/assistant',{
          method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({message:text,history:history.slice(-12),lead,wantsAppointment}),
          signal:abort.signal
        });
      }finally{clearTimeout(timer);}
      const data=await response.json().catch(()=>({}));
      if(!response.ok||typeof data.reply!=='string')throw Error(data.error||'No pude responder en este momento.');
      history=[...history,{role:'user',content:text},{role:'assistant',content:data.reply}].slice(-12);
      if(data.lead&&typeof data.lead==='object')for(const k of Object.keys(lead))if(typeof data.lead[k]==='string')lead[k]=data.lead[k];
      wantsAppointment=data.wantsAppointment===true;
      typing.remove();bubble(data.reply,'assistant');
      if(data.ready&&data.whatsapp&&typeof data.whatsapp.url==='string'&&
         /^https:\/\/wa\.me\/(?:584243103283|584144630453)\?text=/.test(data.whatsapp.url)){
        wa.href=data.whatsapp.url;
        $('ready-caption').textContent='Euro Factory '+(data.whatsapp.branch==='Valencia'?'Valencia':'Maracay');
        ready.hidden=false;
        ready.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'nearest'});
      }
    }catch(e){
      typing.remove();bubble(e.message||'Ocurrió un error de conexión.','error');
      const fallback=document.createElement('p');fallback.className='efc-fallback';
      fallback.append(document.createTextNode('También podés escribirnos: '));
      for(const [name,number] of [['Maracay','584243103283'],['Valencia','584144630453']]){
        const a=document.createElement('a');a.href='https://wa.me/'+number;a.target='_blank';a.rel='noopener noreferrer';a.textContent=name;
        fallback.append(a);
      }
      log.append(fallback);
    }finally{
      loading=false;send.disabled=input.disabled=false;
      if(isOpen)input.focus({preventScroll:true});
      log.scrollTop=log.scrollHeight;
    }
  }
  form.addEventListener('submit',e=>{e.preventDefault();submit(input.value);});
  input.addEventListener('keydown',e=>{
    if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();form.requestSubmit();}
  });
  input.addEventListener('input',()=>{
    input.style.height='auto';input.style.height=Math.min(input.scrollHeight,110)+'px';
  });
  chips.querySelectorAll('[data-ef-prompt]').forEach(button=>button.addEventListener('click',()=>submit(button.dataset.efPrompt)));
})();