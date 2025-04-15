from machine import Machine
from settings import *
import ctypes
import pygame
import sys
from user_manager import UserManager

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()
print(">>> main.py is running!")
print(">>> Arguments:", sys.argv)


class Game:
    def __init__(self, user):
        pygame.init()
        print(">>> Game class initialized!")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('LuckyChain Slot Machine')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.machine.currPlayer.balance = user.balance
        self.machine.currPlayer.name = user.name
        self.delta_time = 0
        self.user = user

        main_sound = pygame.mixer.Sound('audio/track.mp3')
        main_sound.play(loops=-1)

    def draw_esc_bar(self):
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render("ESC  BACK", True, (255, 255, 255))
        text_bg = pygame.Surface((text_surf.get_width() + 20, text_surf.get_height() + 10))
        text_bg.fill((0, 0, 0))
        text_bg.blit(text_surf, (10, 5))
        self.screen.blit(text_bg, (WIDTH - text_bg.get_width() - 20, HEIGHT - text_bg.get_height() - 20))

    def confirm_exit(self):
        import tkinter as tk
        from tkinter import messagebox

        # Initialize hidden Tkinter window
        root = tk.Tk()
        root.withdraw()

        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit the game?")
        root.destroy()

        return result

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
            self.screen.blit(self.grid_image, (0, 0))
            self.draw_esc_bar()
            self.clock.tick(FPS)

        # ✅ When loop ends, exit game properly
        self.save_and_exit()

    def save_and_exit(self):
        manager = UserManager()
        self.user.balance = self.machine.currPlayer.balance
        manager.users[self.user.name] = self.user
        manager.save_users()

        print(f"Game saved. Goodbye, {self.user.name}!")
        pygame.quit()
        sys.exit()


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

    # ✅ Launch the game!
    game = Game(user)
    game.run()

