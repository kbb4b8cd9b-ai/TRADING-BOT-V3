import os
from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.agents import AGENTS
from backend.engine.signal_engine import combine_signals
from backend.engine.risk_engine import RiskEngine
from backend.engine.paper_engine import PaperEngine

app = FastAPI(title="Trading AI v3", version="3.0.0")
paper = PaperEngine(float(os.getenv("STARTING_EQUITY", "50")))
risk = RiskEngine()
state = {"mode": "paper", "daily_pnl": 0.0, "open_positions": 0}

class MarketSnapshot(BaseModel):
    symbol: str = "DEMO"
    price: float = 100.0
    trend: float = 0.0
    momentum: float = 0.0
    volatility: float = 0.5
    volume: float = 0.5
    price_change: float = 0.0

@app.get("/api/status")
def status():
    snap = paper.snapshot()
    return {
        "mode": state["mode"],
        "equity": snap["equity"],
        "daily_pnl": state["daily_pnl"],
        "open_positions": state["open_positions"],
        "agents": AGENTS,
    }

@app.post("/api/start-paper")
def start_paper():
    state["mode"] = "paper"
    return status()

@app.post("/api/stop")
def stop():
    state["mode"] = "stopped"
    return status()

@app.post("/api/analyze")
def analyze(market: MarketSnapshot):
    signals = [
        {"agent":"TrendAgent","signal":"BUY" if market.trend>.2 else "SELL" if market.trend<-.2 else "HOLD","confidence":min(abs(market.trend),1)},
        {"agent":"MomentumAgent","signal":"BUY" if market.momentum>.2 else "SELL" if market.momentum<-.2 else "HOLD","confidence":min(abs(market.momentum),1)},
        {"agent":"ScalpingAgent","signal":"BUY" if market.price_change>.3 else "SELL" if market.price_change<-.3 else "HOLD","confidence":min(abs(market.price_change),1)},
        {"agent":"MeanReversionAgent","signal":"HOLD","confidence":.5},
        {"agent":"VolumeAgent","signal":"BUY" if market.volume>.7 else "HOLD","confidence":market.volume},
        {"agent":"VolatilityAgent","signal":"HOLD","confidence:.5},
        {"agent":"PriceActionAgent","signal":"BUY" if market.price_change>.2 else "SELL" if market.price_change<-.2 else "HOLD","confidence":min(abs(market.price_change),1)},
        {"agent":"MarketRegimeAgent","signal":"HOLD","confidence":.5},
        {"agent":"PortfolioAgent","signal":"HOLD","confidence":.5},
        {"agent":"RiskGuardianAgent","signal":"HOLD","confidence":1.0},
    ]
    decision = combine_signals(signals)
    return {"symbol":market.symbol, "decision":decision, "signals":signals}

@app.post("/api/paper-order")
def paper_order(market: MarketSnapshot, side: str, quantity: float):
    if state["mode"] != "paper":
        return {"status":"REJECTED","reason":"paper mode is not active"}
    value = abs(quantity * market.price)
    approved = risk.approve(
        paper.equity, state["daily_pnl"], value, state["open_positions"]
    )
    if not approved:
        return {"status":"REJECTED","reason":"risk engine"}
    result = paper.market_order(market.symbol, side.upper(), quantity, market.price)
    state["open_positions"] = sum(1 for q in paper.positions.values() if q != 0)
    return result
