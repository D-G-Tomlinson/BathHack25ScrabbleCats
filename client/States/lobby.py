import pygame as pg
from Constants.constants import *
from backend_handler import check_game_state, leave, start_game

leave_button_rect = pg.Rect(10,10,100,50)
leave_button_text = BUTTON_FONT.render("Leave", True, BLACK)
leave_button_text_rect = leave_button_text.get_rect(center=leave_button_rect.center)

button_rect = pg.Rect((WIDTH-300)//2,HEIGHT-110,300,60)
button_text = BUTTON_FONT.render("Start Game", True, BLACK)
button_text_rect = button_text.get_rect(center=button_rect.center)

time = 0

def draw_names(userid, names, screen):
    y = 70
    for name in names:
        if name == userid:
            name = "You: " + userid
        name_surface = INPUT_FONT.render(name, True, BLACK)
        x = (WIDTH - name_surface.get_width())//2
        name_rect = name_surface.get_rect(center=(x,y))
        screen.blit(name_surface, name_rect)
        y = y + 25

def draw(game, screen):
    button_color_to_use = WHITE if not button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, button_color_to_use, button_rect)
    screen.blit(button_text, button_text_rect)
    # back button
    button_color_to_use = WHITE if not leave_button_rect.collidepoint(pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, button_color_to_use, leave_button_rect)
    screen.blit(leave_button_text, leave_button_text_rect)

    # draw game code
    title = "Game Code: " + str(game.game.game_code)
    title_surface = TITLE_FONT.render(title, True, BLACK)
    title_rect = title_surface.get_rect(midtop=(WIDTH//2,10))
    screen.blit(title_surface,title_rect)

    names = game.game.players.keys()
    draw_names(game.userid, names, screen)
    
def update(game, events):
    global time
    current_time = pg.time.get_ticks()
    if current_time - time >1000:
        check_game_state(game.game.game_code,game.userid,game.game)
        time = current_time
        if game.game.round != None:
            return "make_guess"
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if leave_button_rect.collidepoint(event.pos):
                leave(game.game.game_code, game.userid)
                return "main_menu"
            elif button_rect.collidepoint(event.pos):
                start_game(game.game.game_code,game.game)
                return "make_guess"
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            start_game(game.game.game_code,game.game)
            return "make_guess"
    return "lobby"
def init(game):
    pass
functions = (update,draw,init)
