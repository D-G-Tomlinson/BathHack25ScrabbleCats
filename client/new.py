import pygame as pg
from pygame.mixer import music as music
from backend_handler import GameState
# init pygame
pg.init()
pg.mixer.init()

import sys
from Constants.constants import *

import States.main_menu as mm
import States.generate_game_code as ggc
import States.join_game as jg
class Game:
    def __init__(self):
        self.game = GameState()
        self.userid = ""

pg.display.set_icon(PROGRAM_ICON)
music.load(MUSIC_FILE)
music.set_volume(0.5)
music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

game = Game()

states = {"main_menu":(mm.update,mm.draw),
          "generate_game_code":(ggc.update,ggc.draw),
          "join_game":(jg.update,jg.draw)}
state = "main_menu"

def update():
    global state
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
    update_func = states[state][0]
    state = update_func(game, events)

def draw():
    screen.fill(BACKGROUND_COLOUR)    
    draw_func = states[state][1]
    draw_func(game, screen)
    pg.display.flip()

while True:
    update()
    draw()
