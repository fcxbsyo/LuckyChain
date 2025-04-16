import pygame
import random
from settings import symbols


class Symbol(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, index):
        super().__init__()
        self.index = index
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False
        self.x_val = self.rect.left
        self.sym_type = image_path.split('/')[-1].split('.')[0]

    def update(self):
        if self.fade_in and self.size_x < 320:
            self.size_x += 1
            self.size_y += 1
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

        elif not self.fade_in and self.fade_out and self.alpha > 115:
            self.alpha -= 7
            self.image.set_alpha(self.alpha)


class Reel:
    def __init__(self, pos, difficulty_state=0):
        self.symbol_list = pygame.sprite.Group()
        self.difficulty_state = difficulty_state

        # Easier-to-win weights (cherry and watermelon show up most)
        self.symbol_weights_by_state = {
            'cherry': 35,
            'watermelon': 30,
            'olive': 25,
            'bell': 12,
            'sevenn': 5
        }

        self.symbols = symbols

        self.reel_is_spinning = False
        self.delay_time = 0
        self.spin_time = 0

        self.spin_symbols = self.get_weighted_symbols(k=5)

        for idx, item in enumerate(self.spin_symbols):
            symbol_instance = Symbol(self.symbols[item], pos, idx)
            self.symbol_list.add(symbol_instance)
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def get_weighted_symbols(self, k=1):
        weights = self.symbol_weights_by_state
        return random.choices(
            population=list(weights.keys()),
            weights=list(weights.values()),
            k=k
        )

    def animate(self, delta_time):
        reel_is_stopping = False

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

                        new_symbol_type = random.choice(self.spin_symbols)
                        new_symbol_instance = Symbol(
                            self.symbols[new_symbol_type],
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
