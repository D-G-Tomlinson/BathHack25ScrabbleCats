import pygame as pg
from pygame.mixer import music as music
from backend_handler import GameState, leave

import traceback

# init pygame
pg.init()
pg.mixer.init()

import sys
from Constants.constants import *

import States.main_menu as mm
import States.generate_game_code as ggc
import States.join_game as jg
import States.lobby as lb
import States.make_guess as mg
import States.between as bt

class Game:
    def __init__(self):
        self.game = GameState()
        self.userid = ""
        self.last_score = None

pg.display.set_icon(PROGRAM_ICON)
music.load(MUSIC_FILE)
music.set_volume(0.5)
music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

game = Game()

states = {"main_menu":mm.functions,
          "generate_game_code":ggc.functions,
          "join_game":jg.functions,
          "lobby":lb.functions,
          "make_guess":mg.functions,
          "between":bt.functions
          }
state = "main_menu"

def update(state):
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            if game.game.in_game:
                leave(game.game,game.userid)
            pg.quit()
            sys.exit()
    update_func = states[state][0]
    new_state = update_func(game, events)
    if new_state != state:
        states[new_state][2](game)
    return new_state

def draw(state):
    screen.fill(BACKGROUND_COLOUR)    
    draw_func = states[state][1]
    draw_func(game, screen)
    pg.display.flip()

while True:
    try:
        state = update(state)
        draw(state)
    except Exception:
        traceback.print_exc()
        pg.quit()
        sys.exit()
