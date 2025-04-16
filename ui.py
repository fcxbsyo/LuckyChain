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

        combined_text = f"Balance: ${player_data['balance']}   Wager: ${player_data['bet_size']}"
        combined_surf = self.font.render(combined_text, True, TEXT_COLOR, None)

        x, y = 20, self.display_surface.get_size()[1] - 30
        combined_rect = combined_surf.get_rect(bottomleft=(x, y))

        self.display_surface.blit(combined_surf, combined_rect)

        if self.player.last_payout:
            self.win_display_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.win_display_timer < 2000:
            self.display_win_banner(player_data['last_payout'])

    def display_win_banner(self, amount):
        win_surf = self.win_font.render(f"WIN! ${amount}", True, TEXT_COLOR, None)
        win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
        win_rect = win_surf.get_rect(center=(
            self.display_surface.get_width() // 2,
            self.display_surface.get_height() - 60))
        self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()
