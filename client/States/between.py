import pygame as pg
from Constants.constants import *
from backend_handler import check_game_state, leave

class Response:
    def __init__(self, score):
        if score == 0:
            self.text = TIMER_FONT.render("Invalid word! No Points!",True,RED)
        else:
            self.text= TIMER_FONT.render(f"You earned {score} points.",True,(0,100,0))
            
        if score >= 50:
            self.encouragement_text = "Purrfection! You're the cat's meow!"
            self.cat_image = pygame.image.load("Resources/Images/Responses/happy_cat.png")
            self.cat_image = pygame.transform.scale(self.cat_image, (170, 170))
        elif score >= 10:
            self.encouragement_text = "Not bad! Keep going, paws-itively awesome!"
            self.cat_image = pygame.image.load("Resources/Images/Responses/neutral_cat.png")
            self.cat_image = pygame.transform.scale(self.cat_image, (192, 148))
        else:
            self.encouragement_text = "Don't give up! You can do it, little kitty!"
            self.cat_image = pygame.image.load("Resources/Images/Responses/sad_cat.png")
            self.cat_image = pygame.transform.scale(self.cat_image, (220, 150))


            
response = None
over_surface = TITLE_FONT.render("Game Complete",True,BLACK)
over_pos = WIDTH/2,HEIGHT-50
            
time = 0

sidebar_rect = pg.Rect(WIDTH-3*SIDEBAR_WIDTH,0,3*SIDEBAR_WIDTH,HEIGHT)
SIDE_X = WIDTH - sidebar_rect.width + 10
points_pos = SIDE_X//2,80
finished_surface = TIMER_FONT.render("Finished:",True,BLACK)
finished_pos = SIDE_X,10
FINISHED_Y = 40

wait_surface = TIMER_FONT.render("Waiting for:", True, BLACK)
wait_pos = SIDE_X,100
WAIT_Y = 130

leave_button_rect = pg.Rect(10,10,100,50)
leave_button_text = BUTTON_FONT.render("Leave", True, BLACK)
leave_button_text_rect = leave_button_text.get_rect(center=leave_button_rect.center)

is_game_over = False

def check_name(a,b):
    return f"You: {a}" if a==b else a

def draw_names(userid, players, screen):
    nr = players[userid][1]
    y1 = FINISHED_Y
    y2 = WAIT_Y
    details = [(players[id][0], players[id][1], check_name(id,userid)) for id in players.keys()]
    for score, round_num, name in details:
        if round_num==nr:
            pos = SIDE_X,y1
            y1+=25
        else:
            pos = SIDE_X,y2
            y2+=25
        text_surface = INPUT_FONT.render(f"{name} - {score} pts", True, BLACK)
        text_rect = text_surface.get_rect(midleft=pos)
        screen.blit(text_surface, text_rect)

# Text wrapping function
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def draw(game, screen):
    button_color_to_use = WHITE if not leave_button_rect.collidepoint(pg.mouse.get_pos()) else HOVER
    pg.draw.rect(screen, button_color_to_use, leave_button_rect)
    screen.blit(leave_button_text, leave_button_text_rect)

    pg.draw.rect(screen,WHITE,sidebar_rect)
    screen.blit(finished_surface,finished_pos)
    screen.blit(wait_surface,wait_pos)
    draw_names(game.userid,game.game.players,screen)

    if is_game_over:
        screen.blit(over_surface,over_pos)

    screen.blit(response.text,points_pos)
    # encouragement
    wrapped_text = wrap_text(response.encouragement_text, FONT, SIDE_X-30)
    y_offset = points_pos[1]+30
    for line in wrapped_text:
            encouragement_surface = FONT.render(line, True, BLACK)
            encouragement_rect = encouragement_surface.get_rect(center=(SIDE_X // 2, y_offset))
            screen.blit(encouragement_surface, encouragement_rect)
            y_offset += 50
    image_x = (SIDE_X-response.cat_image.get_width())//2
    screen.blit(response.cat_image,(image_x,y_offset))

    
def update(game, events):
    global is_game_over    
    if not is_game_over:
        global time
        current_time = pg.time.get_ticks()
        if current_time - time >1000:
            check_game_state(game.game.game_code,game.userid,game.game)
            time = current_time
            next_round = game.game.players[game.userid][1]
#            print(f"next round is {next_round}")
            current_r = game.game.round["num"]
 #           print(f"current round is {current_r}")
            if current_r==next_round:
                return "make_guess"
            elif current_r==None:
                is_game_over = True
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if leave_button_rect.collidepoint(event.pos):
                leave(game.game.game_code, game.userid)
                return "main_menu"
    return "between"
def init(game):
    global is_game_over
    is_game_over = False
    global response
    response = Response(game.last_score)
functions = (update,draw,init)
