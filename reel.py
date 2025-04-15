import pygame
import random
from settings import symbols


class Symbol(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, index):
        super().__init__()
        self.index = index
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Used for animation and identification
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False
        self.x_val = self.rect.left
        self.sym_type = image_path.split('/')[-1].split('.')[0]  # Extract symbol name

    def update(self):
        # Slightly increases size for winning symbols
        if self.fade_in and self.size_x < 320:
            self.size_x += 1
            self.size_y += 1
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

        # Fades out non-winning symbols
        elif not self.fade_in and self.fade_out and self.alpha > 115:
            self.alpha -= 7
            self.image.set_alpha(self.alpha)


class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]  # Use first 5 shuffled symbols

        self.reel_is_spinning = False
        self.delay_time = 0
        self.spin_time = 0

        for idx, item in enumerate(self.shuffled_keys):
            symbol_instance = Symbol(symbols[item], pos, idx)
            self.symbol_list.add(*[symbol_instance])
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        reel_is_stopping = False  # ✅ Declare at start

        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = self.spin_time < 0

            if self.delay_time <= 0:
                for symbol in list(self.symbol_list.sprites()):
                    symbol.rect.bottom += 100

                    if symbol.rect.top >= 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False

                        symbol_idx = symbol.index
                        symbol_x = symbol.x_val
                        symbol.kill()

                        new_symbol_instance = Symbol(
                            symbols[random.choice(self.shuffled_keys)],
                            (symbol_x, -300),
                            symbol_idx
                        )
                        self.symbol_list.add(*[new_symbol_instance])

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        return [symbol.sym_type for symbol in self.symbol_list.sprites()][::-1]
