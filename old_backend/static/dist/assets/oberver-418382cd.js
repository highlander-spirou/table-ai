const r=(t,s)=>{const e={childList:!0};new MutationObserver(s).observe(t,e)},i=(t,s)=>{for(const e of t)e.type==="childList"&&(console.log("active"),e.target.querySelector("#response-status").getAttribute("status")==="True"?document.getElementById("submit").classList.remove("hidden"):document.getElementById("submit").classList.add("hidden"))};export{i as a,r as o};