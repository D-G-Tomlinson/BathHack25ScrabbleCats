import pygame as pg
from Constants.constants import *

title_image = pg.image.load("Resources/Images/logo.png")  # Replace "title.png" with your file name
title_image = pg.transform.scale(title_image, (400, 400))  # Optional: scale the image
title_rect = title_image.get_rect(midtop=(430, -40))  # Position the image

button_width = 420
button_height = 60

# Buttons
generate_button_rect = pg.Rect(30, 200, button_width, button_height)
generate_button_text = BUTTON_FONT.render("Generate Game Code", True, BLACK)
generate_button_text_rect = generate_button_text.get_rect(center=generate_button_rect.center)

join_button_rect = pg.Rect(30, 280, button_width, button_height)
join_button_text = BUTTON_FONT.render("Join with Existing Game Code", True, BLACK)
join_button_text_rect = join_button_text.get_rect(center=join_button_rect.center)


leave_button_rect = pg.Rect(10,10,100,50)
leave_button_text = BUTTON_FONT.render("Exit", True, BLACK)
leave_button_text_rect = leave_button_text.get_rect(center=leave_button_rect.center)


def draw(game, screen):
    screen.blit(title_image, title_rect)

    col_to_use = WHITE if not leave_button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, col_to_use, leave_button_rect)
    screen.blit(leave_button_text, leave_button_text_rect)

    
    col_to_use = WHITE if not generate_button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, col_to_use, generate_button_rect)
    screen.blit(generate_button_text, generate_button_text_rect)

    col_to_use = WHITE if not join_button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, col_to_use, join_button_rect)
    screen.blit(join_button_text, join_button_text_rect)

def update(game, events):
    for event in events:
        if event.type==pg.MOUSEBUTTONDOWN:
            if generate_button_rect.collidepoint(event.pos):
                return "generate_game_code"
            elif join_button_rect.collidepoint(event.pos):
                return "join_game"
            elif leave_button_rect.collidepoint(event.pos):
                pg.quit()
                import sys
                sys.exit()
    return "main_menu"

def init(game):
    pass
functions = (update,draw,init)
