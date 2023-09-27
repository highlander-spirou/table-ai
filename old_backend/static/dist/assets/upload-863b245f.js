import"./modulepreload-polyfill-3cfb730f.js";import{o as d,a as r}from"./oberver-418382cd.js";const c="/assets/csv-097ca35c.png",m="/assets/xlsx-7aa7ca3a.png";let o=!1,l=[],a=[],i=null;function p(e){return e.length!==new Set(e).size}const x=e=>e/(1024*1024)<.2?`${Math.round(e/1024)} KB`:`${Math.round(e/(1024*1024))} MB`,u=e=>e.substring(e.lastIndexOf(".")+1,e.length),g=e=>{o=!0;const n=Array.from(e),s=n.map(t=>t.name.substring(0,t.name.lastIndexOf("."))||t.name);p(s)?i=!0:n.forEach(t=>{t.size>5*10**8?a=[...a,{name:t.name}]:l=[...l,{name:t.name,size:x(t.size),ext:u(t.name),valid:!0}]})},f=e=>{e.length>0?(document.getElementById("room_name").classList.remove("hidden"),document.getElementById("upload-label").classList.add("hidden")):(document.getElementById("room_name").classList.add("hidden"),document.getElementById("upload-label").classList.remove("hidden"))},v=e=>{let n="";e.forEach(s=>{const t=`
      <div class="flex border-2 rounded-xl h-20 w-[350px]" >
            <img src="${s.ext==="csv"?`${c}`:`${m}`}" class="ml-5 h-[95%]" />
            <div class="flex flex-col mt-3 ml-5">
                <div class="tooltip text-left" data-tip="${s.name}">
                    <p class="text-slate-700 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">${s.name}</p>
                </div>
                <p class="text-base first-letter:text-slate-700">${s.size}</p>
            </div>
        </div>
      `;n+=t}),document.getElementById("file-list").innerHTML=n},h=e=>{let n="<p class='font-bold text-base text-center text-red-500'>File(s) size > 500MB</p>";e.forEach(s=>{const t=`
    <div class="flex border-2 rounded-xl h-20 w-[350px]" >
        <img src="/static/imgs/${s.ext==="csv"?"csv":"xlsx"}.png" class="ml-5 h-[95%]" />
        <div class="mt-3 ml-5">
            <div class="tooltip text-left" data-tip="${s.name}">
                <p class="text-red-500 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">
                    ${s.name}
                </p>
            </div>
        </div>
    </div>
    `;n+=t}),document.getElementById("error-files").innerHTML=n};document.getElementById("files").addEventListener("change",e=>{o&&(l=[],a=[],i=null),g(e.target.files),i?document.getElementById("error-section").innerHTML='<p class="flex justify-center text-red-500 text-lg font-bold">Duplicate filename</p>':(document.getElementById("error-section").innerHTML="",a.length>0?h(a):(v(l),f(l)))});d(document.getElementById("response"),r);
