import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        self.show_map = False  # Variável para alternar a exibição do mapa 2D
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # Desenha o jogo em 3D
        self.object_renderer.draw()
        self.weapon.draw()

        # Exibe o mapa 2D, se ativado
        if self.show_map:
            self.draw_map()

    def draw_map(self):
        # Define o tamanho do minimapa
        map_scale = 10
        map_surface = pg.Surface((self.map.cols * map_scale, self.map.rows * map_scale))
        map_surface.fill((50, 50, 50))  # Cor de fundo do mapa

        # Desenha os blocos do mapa
        for j, row in enumerate(self.map.mini_map):
            for i, cell in enumerate(row):
                if cell:
                    color = (200, 200, 200)  # Cor para paredes e objetos
                    pg.draw.rect(
                        map_surface,
                        color,
                        (i * map_scale, j * map_scale, map_scale, map_scale)
                    )

        # Desenha o jogador no mapa
        player_x, player_y = self.player.pos
        pg.draw.circle(
            map_surface,
            (255, 0, 0),
            (int(player_x * map_scale), int(player_y * map_scale)),
            map_scale // 2
        )

        # Renderiza o minimapa no canto superior direito
        self.screen.blit(map_surface, (self.screen.get_width() - map_surface.get_width() - 10, 10))

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.show_map = not self.show_map  # Alterna o mapa 2D
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
