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
        self.force_exit_game = False

        self.prev_result = {i: None for i in range(5)}
        self.spin_result = {i: None for i in range(5)}
        self.win_data = {}
        self.spin_time = 0

        self.markov_chain = MarkovChain()
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)
        self.statistics = Statistics()

    def spawn_reels(self):
        x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft += (300 + X_OFFSET)

            difficulty = self.markov_chain.get_next_state()

            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft), difficulty_state=difficulty)
            self.reel_index += 1

    def cooldowns(self):
        for reel in self.reel_list.values():
            if reel.reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and all(not reel.reel_is_spinning for reel in self.reel_list.values()):
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

                self.currPlayer.record_jackpot()
                self.statistics.record_spin(self.spin_result, win=True, jackpot=True)
            else:
                self.statistics.record_spin(self.spin_result, win=False, jackpot=False)

    def show_balance_empty_warning(self):
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Balance Depleted", "You’ve run out of balance. Please top up to continue.")
        root.destroy()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle:
            if self.currPlayer.balance >= self.currPlayer.bet_size:
                self.toggle_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.currPlayer.place_bet()
                self.machine_balance += self.currPlayer.bet_size
                self.currPlayer.last_payout = None
            else:
                self.show_balance_empty_warning()
                self.currPlayer.balance = 0
                self.force_exit_game = True

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

        middle_row = horizontal[1]
        unique_symbols = set(middle_row)

        if len(unique_symbols) == 1:
            sym = middle_row[0]
            hits[2] = [sym, [0, 1, 2, 3, 4]]
            self.can_animate = True
            return hits

        return None

    def pay_player(self, win_data, curr_player):
        multiplier = sum(len(v[1]) for v in win_data.values())
        spin_payout = multiplier * curr_player.bet_size * 2
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)

        for reel in self.reel_list.values():
            reel.symbol_list.draw(self.display_surface)
            reel.symbol_list.update()

        self.ui.update()
