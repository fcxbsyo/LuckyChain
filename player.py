class Player:
    def __init__(self):
        self.balance = 1000.00
        self.bet_size = 10.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00
        self.win_count = 0
        self.loss_count = 0
        self.jackpot_count = 0

    def get_data(self):
        return {
            'balance': f"{self.balance:.2f}",
            'bet_size': f"{self.bet_size:.2f}",
            'last_payout': f"{self.last_payout:.2f}" if self.last_payout else "N/A",
            'total_won': f"{self.total_won:.2f}",
            'total_wager': f"{self.total_wager:.2f}",
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'jackpot_count': self.jackpot_count
        }

    def place_bet(self):
        self.balance -= self.bet_size
        self.total_wager += self.bet_size

    def record_win(self, payout):
        self.balance += payout
        self.last_payout = payout
        self.total_won += payout
        self.win_count += 1

    def record_loss(self):
        self.last_payout = 0.00
        self.loss_count += 1

    def record_jackpot(self):
        self.jackpot_count += 1
