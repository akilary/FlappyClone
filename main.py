# Автор ассетов: https://github.com/samuelcust/flappy-bird-assets.git
# Используется с разрешения автора

import sys, time
import pygame as pg
from random import randint

from core import Bird, Base, UpPipe, DownPipe
from utils import Configs, load_image


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()

        self.cfg = Configs()
        self.screen = pg.display.set_mode((self.cfg.width, self.cfg.height))
        pg.display.set_caption("Flappy Bird")
        self.background = self.cfg.load_background()

        self.bird_sprite = pg.sprite.GroupSingle()
        self.base_sprite = pg.sprite.GroupSingle()
        self.pipe_sprite = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()

        # self.all_sprites = pg.sprite.LayeredUpdates()
        # self.pipes = pg.sprite.Group()

        Base(self.screen, self.cfg, self.base_sprite, self.collision_sprites)
        self.bird = Bird(self.screen, self.cfg, self.bird_sprite)

        self.pipe_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.pipe_timer, 1000)

        self.last_passed_pipe = None
        self.score = 0

        self.game_state = "game_running"
        self.game_over_screen = load_image("assets/ui/gameover.png")

    def run(self) -> None:
        """"""
        last_time = time.time()
        while True:
            self.screen.blit(self.background, (0, 0))
            self._check_events()

            dt = time.time() - last_time
            last_time = time.time()

            self.bird_sprite.update(dt)
            self.pipe_sprite.update(dt)
            self.base_sprite.update(dt)
            self._collisions()

            pg.display.update()
            self.clock.tick(self.cfg.fps)

    def _check_events(self) -> None:
        """"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.bird.jump()
            if event.type == self.pipe_timer:
                offset = randint(-100, 100)
                UpPipe(self.screen, self.cfg, offset, self.pipe_sprite, self.collision_sprites)
                DownPipe(self.screen, self.cfg, offset, self.pipe_sprite, self.collision_sprites)

    def _collisions(self) -> None:
        """"""
        if pg.sprite.spritecollide(self.bird, self.collision_sprites, False): # type: ignore
            sys.exit()

        for pipe in filter(lambda p: isinstance(p, UpPipe) and p.rect.centerx < self.bird.rect.centerx,
                           self.pipe_sprite):
            if self.last_passed_pipe != pipe:
                self.score += 1
                self.last_passed_pipe = pipe
                print("Score: ", self.score)



if __name__ == '__main__':
    game = Game()
    game.run()

