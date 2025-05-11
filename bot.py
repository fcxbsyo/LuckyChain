import pygame
from machine import Machine
from user_manager import log_gameplay_data
from settings import FPS
from user_manager import generate_player_summary


class Bot:
    def __init__(self, player_name="BotPlayer", stop_after_losses=10, stop_after_jackpot=True, max_spins=None):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)
        self.machine = Machine()
        self.machine.currPlayer.name = player_name
        self.losses = 0
        self.wins = 0
        self.jackpots = 0
        self.spins = 0
        self.stop_after_losses = stop_after_losses
        self.stop_after_jackpot = stop_after_jackpot
        self.max_spins = max_spins
        self.clock = pygame.time.Clock()

    def simulate(self):
        print(f"[BOT] Starting simulation as {self.machine.currPlayer.name}")
        running = True
        while running:
            if self.machine.can_toggle:
                if self.machine.currPlayer.balance < self.machine.currPlayer.bet_size:
                    print("[BOT] Ran out of balance.")
                    break

                self.machine.toggle_spinning()
                self.machine.currPlayer.place_bet()
                self.spins += 1

            self.machine.update(1 / FPS)

            if self.machine.can_toggle:  # Spin complete
                payout = self.machine.currPlayer.last_payout
                win = payout > 0
                jackpot = payout >= 50

                if win:
                    self.wins += 1
                    self.losses = 0
                else:
                    self.losses += 1
                    self.machine.currPlayer.record_loss()

                if jackpot:
                    self.jackpots += 1
                    self.machine.currPlayer.record_jackpot()

                # Log gameplay
                log_gameplay_data(
                    player_name=self.machine.currPlayer.name,
                    bet_amount=self.machine.currPlayer.bet_size,
                    spin_result=str(self.machine.spin_result),
                    coin_balance=self.machine.currPlayer.balance,
                    session_winnings=payout,
                    session_spins=self.spins,
                    streak_length=self.wins,
                    difficulty_state=self.machine.markov_chain.current_state
                )

                if self.should_stop():
                    print(f"[BOT] Stopping {self.machine.currPlayer.name}")
                    running = False

            self.clock.tick(FPS)

        print(f"[BOT] Done — Spins: {self.spins}, Wins: {self.wins}, Losses: {self.losses}, Jackpots: {self.jackpots}")

    def should_stop(self):
        if self.max_spins and self.spins >= self.max_spins:
            return True
        if self.stop_after_losses and self.losses >= self.stop_after_losses:
            return True
        if self.stop_after_jackpot and self.jackpots >= 1:
            return True
        return False


def simulate_multiple_bots(bot_configs, runs_per_bot=50):
    for config in bot_configs:
        for i in range(runs_per_bot):
            name = f"{config['player_name']}_Run{i+1}"
            print(f"\n=== Running bot: {name} ===")
            bot = Bot(
                player_name=name,
                stop_after_losses=config.get('stop_after_losses'),
                stop_after_jackpot=config.get('stop_after_jackpot'),
                max_spins=config.get('max_spins')
            )
            bot.simulate()
    print("\n=== All bots finished. Data written to gameplay_log.csv ===")


if __name__ == "__main__":
    bot_configs = [
        {
            "player_name": "CautiousBot",
            "stop_after_losses": 5,
            "stop_after_jackpot": True,
            "max_spins": 30
        },
        {
            "player_name": "GreedyBot",
            "stop_after_losses": None,
            "stop_after_jackpot": False,
            "max_spins": 30
        },
        {
            "player_name": "LuckyBot",
            "stop_after_losses": 10,
            "stop_after_jackpot": True,
            "max_spins": 30
        }
    ]

    simulate_multiple_bots(bot_configs, runs_per_bot=20)
    generate_player_summary()
