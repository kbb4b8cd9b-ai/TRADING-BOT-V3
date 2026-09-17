def combine_signals(signals):
    buy = sum(s["confidence"] for s in signals if s["signal"] == "BUY")
    sell = sum(s["confidence"] for s in signals if s["signal"] == "SELL")
    if buy >= 2.0 and buy > sell:
        return "BUY"
    if sell >= 2.0 and sell > buy:
        return "SELL"
    return "HOLD"
