import pygame as pg
from Constants.constants import *
from backend_handler import submit_guess, leave
import Rules.rules as rules
from math import ceil

start_time = 0 
prompt = None

prompt_surface = None
word_text = ""

sidebar_rect = pg.Rect(WIDTH-SIDEBAR_WIDTH,0,SIDEBAR_WIDTH,HEIGHT)
word_box = pg.Rect(250,190,250,40)


cursor_visible = None
cursor_time = None

prompt_card_rect = pg.Rect(20,80,WIDTH-SIDEBAR_WIDTH-40,80)
label_surface = INPUT_FONT.render("Enter a word: ", True, BLACK)

button_rect = pg.Rect((WIDTH - SIDEBAR_WIDTH - 160) // 2, 260, 160, 60)
button_text = INPUT_FONT.render("Enter", True, BLACK)
button_text_rect = button_text.get_rect(center=button_rect.center)

leave_button_rect = pg.Rect(10,10,100,50)
leave_button_text = BUTTON_FONT.render("Leave", True, BLACK)
leave_button_text_rect = leave_button_text.get_rect(center=leave_button_rect.center)

R_NUM_POS = (WIDTH/2,30)

SIDE_X = WIDTH - sidebar_rect.width + 10

time_label_surface = TIMER_FONT.render("Time left:", True, BLACK)
time_label_pos = SIDE_X,10
time_pos = SIDE_X,40

points_label_surface = TIMER_FONT.render("You have", True, BLACK)
points_label_pos = SIDE_X,100
points_surface = None
points_pos = SIDE_X,130

def make_guess(game):
    import Word_Check.word_check as wc
    guess = word_text.lower()
    game.last_score =  int(10 + wc.find_cat_similarity(word_text) * 100) if wc.check_word_valid(guess) and prompt.check_word(guess) else 0
    submit_guess(game.game.game_code,game.userid,game.game.round["num"],game.last_score,game.game)
    return "between"

def get_time_left(game):
    now = pg.time.get_ticks()
    elapsed = (now-start_time)/1000
    return max(game.game.round["length"] - elapsed,0)

def draw_sidebar(game, screen):
    pg.draw.rect(screen,WHITE,sidebar_rect)

    screen.blit(time_label_surface,time_label_pos)
    time_left = str(ceil(get_time_left(game)))
    if time_left=="1":
        time_left+=" second"
    else:
        time_left+=" seconds"
    time_surface = TIMER_FONT.render(time_left,True,BLACK)
    screen.blit(time_surface,time_pos)

    screen.blit(points_label_surface,points_label_pos)
    screen.blit(points_surface, points_pos)
    

def draw(game, screen):

    draw_sidebar(game, screen)
    
    button_color_to_use = WHITE if not leave_button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, button_color_to_use, leave_button_rect)
    screen.blit(leave_button_text, leave_button_text_rect)

    
    button_color_to_use = WHITE if not button_rect.collidepoint(
        pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, button_color_to_use, button_rect)
    screen.blit(button_text, button_text_rect)

    
    pg.draw.rect(screen,WHITE,prompt_card_rect,border_radius=20)

    screen.blit(prompt_surface,
                (prompt_card_rect.x + (prompt_card_rect.width-prompt_surface.get_width())//2,
                 prompt_card_rect.y + 20))
    
    pg.draw.rect(screen, HOVER, word_box)

    r_num = game.game.round["num"]
    r_num_surface = TITLE_FONT.render(f"Round {r_num}",True,BLACK)
    r_num_rect = r_num_surface.get_rect(center=R_NUM_POS)
    screen.blit(r_num_surface,r_num_rect)
    
    word_surface = INPUT_FONT.render(word_text, True, BLACK)
    screen.blit(word_surface,
                (word_box.x+5,
                 word_box.y + (word_box.height-word_surface.get_height())//2))
    
    screen.blit(label_surface,
                (word_box.x-label_surface.get_width() - 10,
                 word_box.y + (word_box.height-label_surface.get_height())//2))

    if cursor_visible:
        cursor_x = word_box.x + 5 + word_surface.get_width()
        pg.draw.line(screen, BLACK, (cursor_x, word_box.y + 5),
                     (cursor_x,word_box.y + word_box.height - 5), 2)
    
def update(game, events):
    global word_text
    global cursor_time
    global cursor_visible

    current_time = pg.time.get_ticks()
    if current_time-cursor_time>500:
        cursor_visible = not cursor_visible
        cursor_time = current_time

    
    time_left = get_time_left(game)
    if time_left<=0:
        return make_guess(game)
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if leave_button_rect.collidepoint(event.pos):
                leave(game.game, game.userid)
                return "main_menu"
            elif button_rect.collidepoint(event.pos):
                return make_guess(game)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                word_text = word_text[:-1]
            elif event.key == pg.K_RETURN:
                return make_guess(game)
            elif event.unicode and event.unicode.isprintable():
                letter = event.unicode.upper()
                if letter >= 'A' and letter <= 'Z':
                    word_text+=letter
    return "make_guess"

def init_time():
    global start_time
    start_time = pg.time.get_ticks()

def init_prompt(game):
    global prompt
    global prompt_surface
    r_text=game.game.round["rule"]
    r = rules.Rule()
    r.set(r_text[0],r_text[1],r_text[2],r_text[3])
    prompt = r
    prompt_text=str(prompt)
    prompt_surface = FONT.render(prompt_text, True, BLACK)
    
def init_word():
    global word_text
    word_text = ""

def init_cursor():
    global cursor_visible
    global cursor_time

    cursor_visible = False
    cursor_time = pg.time.get_ticks()

def init_points(game):
    global points_surface
    points = game.game.players[game.userid][0]
    points_surface = TIMER_FONT.render(str(points)+" points",True,BLACK)
    
def init(game):
    init_time()
    init_prompt(game)
    init_word()
    init_cursor()
    init_points(game)

functions = update,draw,init
