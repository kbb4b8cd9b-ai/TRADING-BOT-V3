const API="http://127.0.0.1:8000";
async function refresh(){const r=await fetch(API+"/api/status");const s=await r.json();mode.textContent=s.mode.toUpperCase();equity.textContent=`€${s.equity.toFixed(2)}`;pnl.textContent=`€${s.daily_pnl.toFixed(2)}`;agents.innerHTML=s.agents.map(x=>`<div>🟢 ${x}</div>`).join("")}
async function startPaper(){await fetch(API+"/api/start-paper",{method:"POST"});refresh()}
async function stopBot(){await fetch(API+"/api/stop",{method:"POST"});refresh()}
async function analyze(){const body={symbol:"DEMO",price:100,trend:.65,momentum:.55,volatility:.5,volume:.8,price_change:.35};const r=await fetch(API+"/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});result.textContent=JSON.stringify(await r.json(),null,2)}
refresh()
