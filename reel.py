import pygame
import random
from settings import symbols


class Symbol(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, index):
        super().__init__()
        self.index = index
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (200, 200))

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]+20, pos[1]+260)

        self.size_x = 240
        self.size_y = 240
        self.alpha = 105
        self.fade_out = False
        self.fade_in = False
        self.x_val = pos[0]
        self.sym_type = image_path.split('/')[-1].split('.')[0]

    def update(self):
        if self.fade_in and self.size_x < 220:
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

        self.symbol_weights_by_state = [
            {  # state 0 - slightly hard (used to be easy)
                'cherry': 20,
                'watermelon': 15,
                'grape': 25,
                'lemon': 30,
                'seven': 10
            },
            {  # state 1 - medium-hard
                'cherry': 15,
                'watermelon': 15,
                'grape': 25,
                'lemon': 30,
                'seven': 15
            },
            {  # state 2 - hard
                'cherry': 10,
                'watermelon': 10,
                'grape': 25,
                'lemon': 35,
                'seven': 20
            },
            {  # state 3 - very hard (jackpot state punishment)
                'cherry': 5,
                'watermelon': 5,
                'grape': 20,
                'lemon': 40,
                'seven': 30
            }
        ]

        self.symbols = symbols
        self.reel_is_spinning = False
        self.delay_time = 0
        self.spin_time = 0

        self.spin_symbols = self.get_weighted_symbols(k=3)

        for idx, item in enumerate(self.spin_symbols):
            symbol_instance = Symbol(self.symbols[item], pos, idx)
            self.symbol_list.add(symbol_instance)
            pos = list(pos)
            pos[1] += 240
            pos = tuple(pos)

    def get_weighted_symbols(self, k=1):
        weights = self.symbol_weights_by_state[self.difficulty_state]
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
                    symbol.rect.bottom += int(240 * delta_time * 20)

                    if symbol.rect.top >= 720:
                        if reel_is_stopping:
                            self.reel_is_spinning = False

                        symbol_idx = symbol.index
                        symbol_x = symbol.x_val
                        symbol.kill()

                        new_symbol_type = random.choice(self.spin_symbols)
                        new_symbol_instance = Symbol(
                            self.symbols[new_symbol_type],
                            (symbol_x, -240),
                            symbol_idx
                        )
                        self.symbol_list.add(*[new_symbol_instance])

            if not self.reel_is_spinning:
                sorted_symbols = sorted(self.symbol_list.sprites(), key=lambda s: s.index)
                for i, symbol in enumerate(sorted_symbols):
                    symbol.rect.center = (symbol.x_val + 120, i * 240 + 120)

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        return [symbol.sym_type for symbol in self.symbol_list.sprites()][::-1]
