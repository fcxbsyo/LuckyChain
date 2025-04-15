from player import Player
from reel import Reel
from markovchain import MarkovChain
from statistics import Statistics
from ui import UI
from wins import flip_horizontal, longest_seq
from settings import X_OFFSET
import random
import pygame


class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # Results and data tracking
        self.prev_result = {i: None for i in range(5)}
        self.spin_result = {i: None for i in range(5)}
        self.win_data = {}
        self.spin_time = 0

        # Instantiate classes
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)
        self.markov_chain = MarkovChain()
        self.statistics = Statistics()

    def spawn_reels(self):
        x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft += (300 + X_OFFSET)
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))
            self.reel_index += 1

    def cooldowns(self):
        for reel in self.reel_list.values():
            if reel.reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        # If all reels have stopped spinning
        if not self.can_toggle and all(not reel.reel_is_spinning for reel in self.reel_list.values()):
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

                # Record win in statistics
                self.statistics.record_spin(self.spin_result, win=True, jackpot=False)
            else:
                # Record loss in statistics
                self.statistics.record_spin(self.spin_result, win=False, jackpot=False)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list.values():
            reel.animate(delta_time)

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            for reel_number, reel in self.reel_list.items():
                reel.start_spin(int(reel_number) * 200)
            self.win_animation_ongoing = False

    def get_result(self):
        return {reel_number: reel.reel_spin_result() for reel_number, reel in self.reel_list.items()}

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits
        return None

    def pay_player(self, win_data, curr_player):
        multiplier = sum(len(v[1]) for v in win_data.values())
        spin_payout = multiplier * curr_player.bet_size
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def win_animation(self):
        # You can add animations here later if you want!
        pass

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)

        for reel in self.reel_list.values():
            reel.symbol_list.draw(self.display_surface)
            reel.symbol_list.update()

        self.ui.update()
        self.win_animation()
