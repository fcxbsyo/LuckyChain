class Statistics:
    def __init__(self):
        self.spin_data = []
        self.win_count = 0
        self.loss_count = 0
        self.jackpot_count = 0

    def record_spin(self, result, win, jackpot):
        self.spin_data.append(result)
        if win:
            self.win_count += 1
        else:
            self.loss_count += 1
        if jackpot:
            self.jackpot_count += 1

    def calculate_win_loss_rate(self):
        total = self.win_count + self.loss_count
        return self.win_count / total if total > 0 else 0

    def generate_report(self):
        return {
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'jackpot_count': self.jackpot_count
        }
