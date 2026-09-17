class RiskEngine:
    def __init__(self, max_daily_loss=0.03, max_position_size=0.20, max_open_positions=2):
        self.max_daily_loss = max_daily_loss
        self.max_position_size = max_position_size
        self.max_open_positions = max_open_positions

    def approve(self, equity, daily_pnl, position_value, open_positions):
        if equity <= 0:
            return False
        if daily_pnl <= -(equity * self.max_daily_loss):
            return False
        if position_value > equity * self.max_position_size:
            return False
        if open_positions >= self.max_open_positions:
            return False
        return True
