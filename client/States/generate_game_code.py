import pygame as pg
from Constants.constants import *
from backend_handler import create_game

username_box_width = 280
username_box_x = (WIDTH//2)-(username_box_width//2)
username_box = pg.Rect(username_box_x, 120, username_box_width, 40)

username_active = True

cursor_visible = True
cursor_time = 0

username_label_text = INPUT_FONT.render("Enter Username:", True, BLACK)
username_label_rect = username_label_text.get_rect(midright=(username_box.x-10,username_box.y+20))

title_text = TITLE_FONT.render("Create New Game",True,BLACK)
title_text_rect = title_text.get_rect(center=(WIDTH//2,60))

button_rect = pg.Rect((WIDTH-300)//2,200,300,60)
button_text = BUTTON_FONT.render("Generate Join Code", True, BLACK)
button_text_rect = button_text.get_rect(center=button_rect.center)

def draw(game, screen):
    screen.fill(BACKGROUND_COLOUR)
    screen.blit(title_text, title_text_rect)

    screen.blit(username_label_text, username_label_rect)
    pg.draw.rect(screen, WHITE, username_box,0)

    username_surface = INPUT_FONT.render(game.userid, True, BLACK)
    screen.blit(username_surface,
                    (username_box.x + 5, username_box.y + (username_box.height - username_surface.get_height()) // 2))

    # Draw the cursor if it's active
    if username_active and cursor_visible:
        cursor_x = username_box.x + 5 + username_surface.get_width()  # Position the cursor after the text
        pygame.draw.line(screen, BLACK, (cursor_x, username_box.y + 5),
                        (cursor_x, username_box.y + username_box.height - 5), 2)

    # Draw the "Generate Join Code" button
    button_color_to_use = WHITE if not button_rect.collidepoint(
        pygame.mouse.get_pos()) else HOVER
    pygame.draw.rect(screen, button_color_to_use, button_rect)
    screen.blit(button_text, button_text_rect)

def update(game, events):
    global cursor_time
    global cursor_visible
    global username_active
    
    current_time = pg.time.get_ticks()
    if current_time-cursor_time>500:
        cursor_visible = not cursor_visible
        cursor_time = current_time

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            username_active = username_box.collidepoint(event.pos)
            if button_rect.collidepoint(event.pos) and game.userid.strip():
                create_game(game.userid, game.game)
                return "lobby"
        elif event.type == pg.KEYDOWN and username_active:
            if event.key == pg.K_BACKSPACE:
                game.userid = game.userid[:-1]
            elif event.key == pg.K_RETURN:
                create_game(game.userid, game.game)
                return "lobby"
            elif event.unicode and event.unicode.isprintable():
                game.userid += event.unicode                    
    return "generate_game_code"
