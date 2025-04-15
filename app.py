import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import sys
import os
from user_manager import UserManager
from tkinter import PhotoImage
from PIL import Image, ImageTk
import tkinter.font as tkFont


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LuckyChain Launcher")

        window_width = 1350
        window_height = 900
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.resizable(False, False)

        self.user_manager = UserManager()
        self.current_user = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomePage, LoginPage, MenuPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

    def return_to_login(self, event=None):
        self.current_user = None
        self.show_frame(LoginPage)


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.bind("<Escape>", self.exit_program)
        self.focus_set()

        fixed_width = 1350
        fixed_height = 900

        # ✅ Load and resize wallpaper
        image_path = os.path.join(os.path.dirname(__file__), "graphics", "wallpaper.jpg")
        original_image = Image.open(image_path)
        resized_image = original_image.resize(
            (fixed_width, fixed_height),
            Image.Resampling.LANCZOS
        )
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # ✅ Background image fills frame
        self.bg_label = tk.Label(self, image=self.bg_image, borderwidth=0)
        self.bg_label.pack(fill="both", expand=True)

        # ✅ Load Bebas Neue font
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "BebasNeue-Regular.ttf")
        title_font = tkFont.Font(family="Bebas Neue", size=80)  # Big title
        button_font = tkFont.Font(family="Bebas Neue", size=32)

        # ✅ Create container frame (align left-center)
        content_frame = tk.Frame(self.bg_label, bg="", highlightthickness=0)
        content_frame.place(relx=0.2, rely=0.5, anchor="w")  # Left side align

        # ✅ Title text
        title_label = tk.Label(content_frame, text="LUCKY CHAIN", font=title_font, fg="white")
        title_label.pack(pady=(0, 20), anchor="w")  # Padding bottom 20

        # ✅ Optional: Subtitle
        subtitle_label = tk.Label(content_frame, text="Spin. Win. Enjoy the game.", font=button_font, fg="white")
        subtitle_label.pack(pady=(0, 40), anchor="w")

        # ✅ Start text (clean, no box)
        start_button = tk.Label(content_frame, text="Start", font=button_font, fg="white", cursor="hand2")
        start_button.pack(anchor="w")
        start_button.bind("<Button-1>", self.go_to_login)

        # ✅ Add hover effect for start button (Optional!)
        start_button.bind("<Enter>", lambda e: start_button.config(fg="gray"))
        start_button.bind("<Leave>", lambda e: start_button.config(fg="white"))

        # ✅ ESC label bottom right
        esc_label = tk.Label(self.bg_label, text="ESC", font=button_font, fg="white", padx=5, pady=2)
        esc_label.place(relx=0.98, rely=0.95, anchor="se")

    def go_to_login(self, event=None):
        self.controller.show_frame(LoginPage)

    def exit_program(self, event=None):
        confirm = messagebox.askyesno("Exit Program", "Are you sure you want to exit?")
        if confirm:
            self.controller.destroy()
            sys.exit()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.bind_all("<Escape>", self.exit_program)

        tk.Label(self, text="Enter your name:", font=("Helvetica", 18)).pack(pady=20)
        self.name_entry = tk.Entry(self, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        tk.Button(self, text="Login", font=("Helvetica", 14), command=self.login).pack(pady=20)

        # ESC Visual Bar
        esc_label = tk.Label(self, text="ESC  BACK", bg="black", fg="white", padx=5, pady=2)
        esc_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    def login(self):
        name = self.name_entry.get().strip()
        if name:
            self.controller.current_user = self.controller.user_manager.get_user(name)
            self.controller.show_frame(MenuPage)

    def exit_program(self, event=None):
        confirm = messagebox.askyesno("Exit Program", "Are you sure you want to exit?")
        if confirm:
            self.controller.destroy()
            sys.exit()


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.bind("<Escape>", self.logout)
        self.focus_set()

        self.balance_label = tk.Label(self, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=20)

        tk.Button(self, text="Play Game", font=("Helvetica", 14), command=self.play_game).pack(pady=10)
        tk.Button(self, text="Top Up", font=("Helvetica", 14), command=self.top_up).pack(pady=10)

        # ESC Visual Bar
        esc_label = tk.Label(self, text="ESC  BACK", bg="black", fg="white", padx=5, pady=2)
        esc_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    def refresh(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Hello, {user.name}! Your balance: {user.balance}")

    def play_game(self):
        self.controller.user_manager.save_users()

        user = self.controller.current_user
        username = user.name
        balance = user.balance

        python_exec = sys.executable
        main_path = os.path.abspath("main.py")

        # Use call() so app waits for game to finish
        subprocess.call([python_exec, main_path, username, str(balance)],
                        stdout=sys.stdout, stderr=sys.stderr)

        # After game ends, refresh balance and return to menu
        self.controller.user_manager = UserManager()  # Reload data from CSV
        self.controller.current_user = self.controller.user_manager.get_user(username)
        self.refresh()

    def top_up(self):
        amount = simpledialog.askinteger("Top Up", "Enter the amount you want to top up:", minvalue=1)

        if amount is not None:
            confirm = messagebox.askyesno("Confirm Top Up", f"Are you sure you want to top up {amount}?")

            if confirm:
                user = self.controller.current_user
                user.top_up(amount)
                self.controller.user_manager.save_users()
                messagebox.showinfo("Success", f"Topped up {amount} successfully!")
                self.refresh()

    def logout(self, event=None):
        self.controller.return_to_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()
