from machine import Machine
from settings import *
import ctypes
import pygame
import sys
from user_manager import UserManager
from settings import WIDTH, HEIGHT

ctypes.windll.user32.SetProcessDPIAware()
print(">>> main.py is running!")
print(">>> Arguments:", sys.argv)


class Game:
    def __init__(self, user):
        pygame.init()
        print(">>> Game class initialized!")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        pygame.display.set_caption('LuckyChain Slot Machine')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.machine.currPlayer.balance = user.balance
        self.machine.currPlayer.name = user.name
        self.delta_time = 0
        self.user = user
        self.should_return_to_topup = False
        main_sound = pygame.mixer.Sound('audio/track.mp3')
        main_sound.play(loops=-1)

    def draw_esc_bar(self):
        font = pygame.font.SysFont(None, 32)
        text = "ESC  BACK"

        text_surf = font.render(text, True, (255, 255, 255))
        padding = 10

        bg_rect = pygame.Rect(
            self.screen_width - text_surf.get_width() - 2 * padding - 20,
            self.screen_height - text_surf.get_height() - 2 * padding - 20,
            text_surf.get_width() + 2 * padding,
            text_surf.get_height() + 2 * padding
        )

        overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (bg_rect.x, bg_rect.y))

        self.screen.blit(text_surf, (bg_rect.x + padding, bg_rect.y + padding))

    def confirm_exit(self):
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()

        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit the game?")
        root.destroy()

        return result

    def show_balance_empty_warning(self):
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Balance Depleted", "You’ve run out of balance. Please top up to continue.")
        root.destroy()

    def run(self):
        self.start_time = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.confirm_exit():
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.confirm_exit():
                            running = False

            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)

            if self.machine.force_exit_game:
                self.should_return_to_topup = True
                running = False
                break

            self.screen.blit(self.grid_image, (0, 0))
            self.draw_esc_bar()
            self.clock.tick(FPS)

        self.save_and_exit()
        return "topup" if self.should_return_to_topup else "done"

    def save_and_exit(self):
        manager = UserManager()
        self.user.balance = self.machine.currPlayer.balance
        self.user.jackpot_count = self.machine.currPlayer.jackpot_count
        manager.users[self.user.name] = self.user
        manager.save_users()


if __name__ == '__main__':
    manager = UserManager()

    if len(sys.argv) >= 3:
        player_name = sys.argv[1]
        balance = float(sys.argv[2])
        user = manager.get_user(player_name)
        user.balance = balance
        print(f"Welcome back, {player_name}! Your balance is {balance}")
    else:
        player_name = input("Enter your name: ").strip()
        user = manager.get_user(player_name)
        manager.top_up_user(user)

    game = Game(user)
    game.run()

