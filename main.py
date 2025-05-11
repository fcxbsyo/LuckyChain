import os
import sys
import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image
import tkinter.font as tkFont
import game
from user_manager import UserManager, User


WIDTH, HEIGHT = 1400, 750
FONT_PATH = os.path.join("graphics", "font", "BebasNeue-Regular.ttf")
BG_GIF_PATH = os.path.join("graphics", "wallpaper.gif")


class WelcomeScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lucky Chain - Welcome")
        self.frames = self.load_gif(BG_GIF_PATH)
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_interval = 100

        self.title_font = pygame.font.Font(FONT_PATH, 100)
        self.start_font = pygame.font.Font(FONT_PATH, 40)

    def load_gif(self, path):
        pil_image = Image.open(path)
        frames = []
        try:
            while True:
                frame = pil_image.convert("RGBA")
                pygame_img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                pygame_img = pygame.transform.scale(pygame_img, (WIDTH, HEIGHT))
                frames.append(pygame_img)
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass
        return frames

    def show(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.handle_frame()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if self.confirm_exit():
                        pygame.quit()
                        sys.exit()
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    running = False
            clock.tick(60)

    def handle_frame(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = now

    def draw(self):
        self.screen.blit(self.frames[self.current_frame], (0, 0))
        title_text = self.title_font.render("LUCKY CHAIN", True, (255, 255, 255))
        start_text = self.start_font.render("Press any key or click to Start", True, (255, 255, 255))
        esc_text = self.start_font.render("ESC to exit", True, (200, 200, 200))

        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 320))
        self.screen.blit(esc_text, (WIDTH - esc_text.get_width() - 30, HEIGHT - 60))
        pygame.display.flip()

    def confirm_exit(self):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        root.destroy()
        return result


class LoginScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lucky Chain - Login")
        self.frames = WelcomeScreen().load_gif(BG_GIF_PATH)
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_interval = 100
        self.font = pygame.font.Font(FONT_PATH, 40)
        self.small_font = pygame.font.Font(FONT_PATH, 28)
        self.input_text = ""
        self.active = False
        self.message = ""
        self.user_manager = UserManager()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_frame()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if WelcomeScreen().confirm_exit():
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        user = self.handle_login()
                        if user:
                            return user
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        if WelcomeScreen().confirm_exit():
                            pygame.quit()
                            sys.exit()
                    else:
                        self.input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if WIDTH // 2 - 150 <= x <= WIDTH // 2 + 150 and 210 <= y <= 250:
                        user = self.handle_login()
                        if user:
                            return user
                    elif WIDTH // 2 - 150 <= x <= WIDTH // 2 + 150 and 270 <= y <= 310:
                        user = self.handle_register()
                        if user:
                            return user

            clock.tick(60)

    def handle_login(self):
        name = self.input_text.strip().lower()
        if not name:
            self.message = "Please enter your name."
            return None
        if name not in self.user_manager.users:
            self.message = "This name is not registered."
            return None
        user = self.user_manager.get_user(name)
        return user

    def handle_register(self):
        import tkinter as tk
        from tkinter import simpledialog, messagebox

        root = tk.Tk()
        root.withdraw()
        new_name = simpledialog.askstring("Register", "Enter a new username:")
        root.destroy()

        if not new_name:
            return None

        new_name = new_name.strip().lower()
        if new_name in self.user_manager.users:
            messagebox.showerror("Name Taken", "This name is already taken. Please choose another.")
            return None

        user = self.user_manager.get_user(new_name)
        return user

    def handle_frame(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = now

    def draw(self):
        self.screen.blit(self.frames[self.current_frame], (0, 0))
        input_box = pygame.Rect(WIDTH // 2 - 150, 120, 300, 50)  # way up
        pygame.draw.rect(self.screen, (0, 0, 0, 180), input_box.inflate(20, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)

        txt_surface = self.font.render(self.input_text or "Enter name...", True, (255, 255, 255))
        self.screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        login_btn = self.small_font.render("Login", True, (255, 255, 255))
        self.screen.blit(login_btn, (WIDTH // 2 - 150, 210))  # was 320

        register_txt = self.small_font.render("Don't have an account? Register", True, (200, 200, 255))
        self.screen.blit(register_txt, (WIDTH // 2 - 150, 270))  # was 390

        if self.message:
            msg_surface = self.small_font.render(self.message, True, (255, 150, 150))
            self.screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, 330))  # was 450

        pygame.display.flip()


class MenuScreen:
    def __init__(self, user):
        self.user = user
        self.user_manager = UserManager()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lucky Chain - Menu")
        self.frames = WelcomeScreen().load_gif(BG_GIF_PATH)
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_interval = 100
        self.font = pygame.font.Font(FONT_PATH, 40)
        self.small_font = pygame.font.Font(FONT_PATH, 28)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_frame()
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.confirm_exit():
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.confirm_exit():
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if WIDTH//2 - 150 <= x <= WIDTH//2 + 150 and 230 <= y <= 270:
                        if self.user.balance <= 0:
                            self.show_balance_empty_warning()
                        else:
                            return "play"
                    elif WIDTH//2 - 150 <= x <= WIDTH//2 + 150 and 300 <= y <= 340:
                        self.top_up()

            clock.tick(60)

    def show_balance_empty_warning(self):
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Insufficient Balance", "You don’t have enough balance to play. Please top up first.")
        root.destroy()

    def handle_frame(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = now

    def draw(self):
        self.screen.blit(self.frames[self.current_frame], (0, 0))

        name_text = self.font.render(f"Hello, {self.user.name.title()}", True, (255, 255, 255))
        bal_text = self.font.render(f"Balance: ${self.user.balance:.2f}", True, (255, 255, 255))
        self.screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, 100))  # was 180
        self.screen.blit(bal_text, (WIDTH // 2 - bal_text.get_width() // 2, 150))  # was 230

        start_btn = self.small_font.render("Start Game", True, (255, 255, 255))
        self.screen.blit(start_btn, (WIDTH // 2 - 150, 230))  # was 400

        topup_btn = self.small_font.render("Top Up", True, (255, 255, 255))
        self.screen.blit(topup_btn, (WIDTH // 2 - 150, 300))  # was 470

        esc_text = self.small_font.render("ESC to exit", True, (200, 200, 200))
        self.screen.blit(esc_text, (WIDTH - esc_text.get_width() - 30, HEIGHT - 60))

        pygame.display.flip()

    def top_up(self):
        import tkinter as tk
        from tkinter import simpledialog, messagebox

        root = tk.Tk()
        root.withdraw()
        amount = simpledialog.askinteger("Top Up", "Enter amount to top up:", minvalue=1)
        root.destroy()

        if amount:
            self.user.top_up(amount)
            self.user_manager.save_users()
            messagebox.showinfo("Success", f"Topped up ${amount} successfully!")

    def confirm_exit(self):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Exit Program", "Are you sure you want to exit?")
        root.destroy()
        return result


if __name__ == "__main__":
    WelcomeScreen().show()
    user = LoginScreen().run()
    while True:
        menu = MenuScreen(user)
        action = menu.run()
        if action == "play":
            while True:
                game = game.Game(user)
                game_result = game.run()

                if game_result == "topup":
                    user = UserManager().get_user(user.name)
                    break
                elif game_result == "exit":
                    pygame.quit()
                    sys.exit()
                else:
                    break
        elif action == "topup":
            user = UserManager().get_user(user.name)
            continue
        elif action == "exit":
            break
