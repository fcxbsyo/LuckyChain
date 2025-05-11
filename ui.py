from player import Player
from settings import *
import pygame
import random


class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        try:
            self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            print("Error loading font!")
            quit()
        self.win_display_timer = 0
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()

        balance_text = f"BALANCE: ${player_data['balance']}"
        wager_text = f"WAGER: ${player_data['bet_size']}"

        balance_surf = self.font.render(balance_text, True, TEXT_COLOR, None)
        wager_surf = self.font.render(wager_text, True, TEXT_COLOR, None)

        x = WIDTH - 190
        y = 40
        self.display_surface.blit(balance_surf, (x, y))
        self.display_surface.blit(wager_surf, (x, y + 40))

        if player_data['last_payout'] != "N/A" and float(player_data['last_payout']) > 0:
            self.win_display_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.win_display_timer < 2000 and \
                player_data['last_payout'] != "N/A" and float(player_data['last_payout']) > 0:
            self.display_win_banner(player_data['last_payout'])

    def display_win_banner(self, amount):
        win_surf = self.win_font.render(f"WIN! ${amount}", True, TEXT_COLOR, None)
        win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
        win_rect = win_surf.get_rect(center=(
            self.display_surface.get_width() // 2,
            self.display_surface.get_height() - 60))
        self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(WIDTH - 200, 0, 200, HEIGHT))
        self.display_info()
