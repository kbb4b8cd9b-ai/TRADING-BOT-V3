class PaperEngine:
    def __init__(self, equity=50.0):
        self.equity = equity
        self.positions = {}
        self.orders = []

    def snapshot(self):
        return {
            "equity": round(self.equity, 2),
            "positions": self.positions,
            "orders": self.orders[-20:],
        }

    def market_order(self, symbol, side, quantity, price):
        value = abs(quantity * price)
        if value > self.equity:
            return {"status": "REJECTED", "reason": "insufficient paper equity"}
        signed = quantity if side == "BUY" else -quantity
        self.positions[symbol] = self.positions.get(symbol, 0) + signed
        order = {"symbol": symbol, "side": side, "quantity": quantity, "price": price, "status": "FILLED"}
        self.orders.append(order)
        return order
