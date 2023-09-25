import"./modulepreload-polyfill-3cfb730f.js";const a=(e,n)=>{const t={childList:!0};new MutationObserver(n).observe(e,t)},r=(e,n)=>{for(const t of e)t.type==="childList"&&(t.target.querySelector("#response-status").getAttribute("status")==="True"?document.getElementById("submit").classList.remove("hidden"):document.getElementById("submit").classList.add("hidden"))},c="/assets/csv-097ca35c.png",m="/assets/xlsx-7aa7ca3a.png";let d=!1,l=[],o=[],i=null;function u(e){return e.length!==new Set(e).size}const p=e=>e/(1024*1024)<.2?`${Math.round(e/1024)} KB`:`${Math.round(e/(1024*1024))} MB`,x=e=>e.substring(e.lastIndexOf(".")+1,e.length),g=e=>{d=!0;const n=Array.from(e),t=n.map(s=>s.name.substring(0,s.name.lastIndexOf("."))||s.name);u(t)?i=!0:n.forEach(s=>{s.size>5*10**8?o=[...o,{name:s.name}]:l=[...l,{name:s.name,size:p(s.size),ext:x(s.name),valid:!0}]})},v=e=>{e.length>0?(document.getElementById("room_name").classList.remove("hidden"),document.getElementById("upload-label").classList.add("hidden")):(document.getElementById("room_name").classList.add("hidden"),document.getElementById("upload-label").classList.remove("hidden"))},f=e=>{let n="";e.forEach(t=>{const s=`
      <div class="flex border-2 rounded-xl h-20 w-[350px]" >
            <img src="${t.ext==="csv"?`${c}`:`${m}`}" class="ml-5 h-[95%]" />
            <div class="flex flex-col mt-3 ml-5">
                <div class="tooltip text-left" data-tip="${t.name}">
                    <p class="text-slate-700 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">${t.name}</p>
                </div>
                <p class="text-base first-letter:text-slate-700">${t.size}</p>
            </div>
        </div>
      `;n+=s}),document.getElementById("file-list").innerHTML=n},h=e=>{let n="<p class='font-bold text-base text-center text-red-500'>File(s) size > 500MB</p>";e.forEach(t=>{const s=`
    <div class="flex border-2 rounded-xl h-20 w-[350px]" >
        <img src="/static/imgs/${t.ext==="csv"?"csv":"xlsx"}.png" class="ml-5 h-[95%]" />
        <div class="mt-3 ml-5">
            <div class="tooltip text-left" data-tip="${t.name}">
                <p class="text-red-500 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">
                    ${t.name}
                </p>
            </div>
        </div>
    </div>
    `;n+=s}),document.getElementById("error-files").innerHTML=n};document.getElementById("files").addEventListener("change",e=>{d&&(l=[],o=[],i=null),g(e.target.files),i?document.getElementById("error-section").innerHTML='<p class="flex justify-center text-red-500 text-lg font-bold">Duplicate filename</p>':(document.getElementById("error-section").innerHTML="",o.length>0?h(o):(f(l),v(l)))});a(document.getElementById("response"),r);
