import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Global variable to track if music has started
background_music_started = False

# Screen setup
programIcon = pygame.image.load('scrabble_cat_tile.png')
pygame.display.set_icon(programIcon)
width, height = 640, 360
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Scrabble Cats™ Banter')
background_colour = (50, 205, 50)

# Fonts
font = pygame.font.SysFont("centurygothic", 48)
button_font = pygame.font.SysFont("centurygothic", 28)
input_font = pygame.font.SysFont("centurygothic", 32)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Global variables
game_code = ''
username_text = ''
game_code_text = ''
message = ''
message_color = black
player_points = {}  # Dictionary to store player points
player_usernames = {}  # Dictionary to store player usernames

# States
MAIN_MENU = 0
JOIN_GAME = 1
GAME_CODE_GENERATED = 2

current_state = MAIN_MENU


def play_background_music(music_file='kevin-macleod-hall-of-the-mountain-king.mp3'):
    """
    Play background music in a loop

    Parameters:
    music_file (str): Path to the music file to play
    """
    global background_music_started

    # Only start the music if it's not already playing
    if not background_music_started:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            background_music_started = True
            print("Music started successfully")  # Debug message
        except pygame.error as e:
            print(f"Cannot load music file: {music_file}")
            print(f"Error: {e}")


# Functions for each screen
def draw_main_menu():
    play_background_music()
    # Load the title image
    title_image = pygame.image.load("Logo.png")  # Replace "title.png" with your file name
    title_image = pygame.transform.scale(title_image, (400, 400))  # Optional: scale the image
    title_rect = title_image.get_rect(midtop=(430, -40))  # Position the image

    button_width = 420
    button_height = 60
    button_color = white
    button_hover_color = (200, 200, 255)

    # Buttons
    generate_button_rect = pygame.Rect(30, 200, button_width, button_height)
    generate_button_text = button_font.render("Generate Game Code", True, black)
    generate_button_text_rect = generate_button_text.get_rect(center=generate_button_rect.center)

    join_button_rect = pygame.Rect(30, 280, button_width, button_height)
    join_button_text = button_font.render("Join with Existing Game Code", True, black)
    join_button_text_rect = join_button_text.get_rect(center=join_button_rect.center)

    # Draw the screen
    screen.fill(background_colour)
    screen.blit(title_image, title_rect)
    pygame.draw.rect(screen, button_color, generate_button_rect)
    screen.blit(generate_button_text, generate_button_text_rect)
    pygame.draw.rect(screen, button_color, join_button_rect)
    screen.blit(join_button_text, join_button_text_rect)

    pygame.display.flip()


def draw_join_game_screen():
    global screen, username_text, game_code_text
    global username_active, game_code_active
    global cursor_visible, cursor_timer
    global message, message_color

    # Screen setup
    width, height = 640, 360
    screen = pygame.display.set_mode((width, height))
    background_colour = (50, 205, 50)

    # Fonts
    font = pygame.font.SysFont("centurygothic", 48)
    input_font = pygame.font.SysFont("centurygothic", 32)
    invalid_font = pygame.font.SysFont("centurygothic", 24)

    # Title text
    title_text = font.render("Join Game!", True, (0, 0, 0))
    title_rect = title_text.get_rect(midtop=(width // 2, 20))

    # Input boxes
    username_box = pygame.Rect(250, 100, 300, 40)
    game_code_box = pygame.Rect(250, 170, 300, 40)
    username_text = ''
    game_code_text = ''
    username_active = True
    game_code_active = False

    # Labels
    username_label_text = input_font.render("Username:", True, (0, 0, 0))
    username_label_rect = username_label_text.get_rect(midright=(240, 120))
    game_code_label_text = input_font.render("Game code:", True, (0, 0, 0))
    game_code_label_rect = game_code_label_text.get_rect(midright=(240, 190))

    # Join button
    button_rect = pygame.Rect(240, 240, 160, 60)
    button_color = (255, 255, 255)
    button_hover_color = (200, 200, 255)
    button_text = input_font.render("Join", True, (0, 0, 0))
    button_text_rect = button_text.get_rect(center=button_rect.center)

    # Message
    message = ''
    message_color = (0, 0, 0)
    error_message_y = height - 40

    # Cursor
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()
    cursor_x_offset = 5
    cursor_y_offset = 5
    cursor_rect = pygame.Rect(0, 0, 2, 32)
    max_characters = 10

    def scramble_username(username):
        username_list = list(username)
        random.shuffle(username_list)
        return ''.join(username_list)

    running = True
    joined = False

    while running:
        screen.fill(background_colour)

        if joined:
            lobby_screen()

        screen.blit(title_text, title_rect)

        screen.blit(username_label_text, username_label_rect)
        pygame.draw.rect(screen, (255, 255, 255), username_box)
        txt_surface = input_font.render(username_text, True, (0, 0, 0))
        if txt_surface.get_width() > username_box.width - 10:
            txt_surface = input_font.render(username_text[:max_characters], True, (0, 0, 0))
        input_text_rect = txt_surface.get_rect(
            topleft=(username_box.x + 5, username_box.y + (username_box.height - txt_surface.get_height()) // 2))
        screen.blit(txt_surface, input_text_rect)

        if username_active:
            if pygame.time.get_ticks() - cursor_timer >= 500:
                cursor_visible = not cursor_visible
                cursor_timer = pygame.time.get_ticks()
            if cursor_visible:
                cursor_rect.x = input_text_rect.x + txt_surface.get_width() + cursor_x_offset
                cursor_rect.y = input_text_rect.y + cursor_y_offset
                pygame.draw.rect(screen, (0, 0, 0), cursor_rect)

        screen.blit(game_code_label_text, game_code_label_rect)
        pygame.draw.rect(screen, (255, 255, 255), game_code_box)
        txt_surface = input_font.render(game_code_text, True, (0, 0, 0))
        if txt_surface.get_width() > game_code_box.width - 10:
            txt_surface = input_font.render(game_code_text[:max_characters], True, (0, 0, 0))
        input_text_rect = txt_surface.get_rect(
            topleft=(game_code_box.x + 5, game_code_box.y + (game_code_box.height - txt_surface.get_height()) // 2))
        screen.blit(txt_surface, input_text_rect)

        if game_code_active:
            if pygame.time.get_ticks() - cursor_timer >= 500:
                cursor_visible = not cursor_visible
                cursor_timer = pygame.time.get_ticks()
            if cursor_visible:
                cursor_rect.x = input_text_rect.x + txt_surface.get_width() + cursor_x_offset
                cursor_rect.y = input_text_rect.y + cursor_y_offset
                pygame.draw.rect(screen, (0, 0, 0), cursor_rect)

        color = button_color if not button_rect.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(button_text, button_text_rect)

        if message:
            font_to_use = input_font if message_color == (0, 128, 0) else invalid_font
            msg_surface = font_to_use.render(message, True, message_color)
            msg_rect = msg_surface.get_rect(center=(width // 2, error_message_y))
            screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    username_active = True
                    game_code_active = False
                elif game_code_box.collidepoint(event.pos):
                    game_code_active = True
                    username_active = False
                else:
                    username_active = False
                    game_code_active = False

                if button_rect.collidepoint(event.pos):
                    if game_code_text.strip().lower() == "cats" and username_text.strip():
                        scrambled_username = scramble_username(username_text.strip())
                        message = f"Welcome, {scrambled_username}!"
                        message_color = (0, 128, 0)
                        joined = True
                    else:
                        message = "You cannot join."
                        message_color = (255, 0, 0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_code_text.strip().lower() == "cats" and username_text.strip():
                        scrambled_username = scramble_username(username_text.strip())
                        message = f"Welcome, {scrambled_username}!"
                        message_color = (0, 128, 0)
                        joined = True
                    else:
                        message = "You cannot join."
                        message_color = (255, 0, 0)

                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.key == pygame.K_DOWN:
                        username_active = False
                        game_code_active = True
                    elif len(username_text) < max_characters and event.unicode.isprintable():
                        username_text += event.unicode

                elif game_code_active:
                    if event.key == pygame.K_BACKSPACE:
                        game_code_text = game_code_text[:-1]
                    elif event.key == pygame.K_UP:
                        game_code_active = False
                        username_active = True
                    elif len(game_code_text) < max_characters and event.unicode.isprintable():
                        game_code_text += event.unicode


def draw_game_code_generated_screen():
    # Fonts
    font = pygame.font.SysFont("centurygothic", 48)
    input_font = pygame.font.SysFont("centurygothic", 32)
    button_font = pygame.font.SysFont("centurygothic", 28)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # User input box for username
    username_box_x = 180
    username_box_y = 120
    username_box_width = 280
    username_box_height = 40
    username_box = pygame.Rect(username_box_x, username_box_y, username_box_width, username_box_height)
    username_text = ''
    username_active = True  # Make active from the start
    cursor_visible = True
    cursor_time = 0

    # "Enter Username" label
    username_label_text = input_font.render("Enter Username:", True, black)
    username_label_rect = username_label_text.get_rect(midright=(username_box_x - 10, username_box_y + 20))

    # Title at the top in big writing
    title_font = pygame.font.SysFont("centurygothic", 72)  # Increased font size for the title
    title_text = title_font.render("Join Game", True, black)
    title_text_rect = title_text.get_rect(center=(width // 2, 60))  # Centered at the top

    # Button to generate join code
    button_width = 300
    button_height = 60
    button_color = white
    button_hover_color = (200, 200, 255)
    generate_button_rect = pygame.Rect((width - button_width) // 2, 200, button_width, button_height)
    generate_button_text = button_font.render("Generate Join Code", True, black)
    generate_button_text_rect = generate_button_text.get_rect(center=generate_button_rect.center)

    # Share join code button
    share_button_rect = pygame.Rect((width - button_width) // 2, 280, button_width, button_height)
    share_button_text = button_font.render("Share Join Code", True, black)
    share_button_text_rect = share_button_text.get_rect(center=share_button_rect.center)

    # Join code display
    join_code = ''
    show_share_button = False

    # Main loop
    running = True
    while running:
        screen.fill(background_colour)

        # Draw the title at the top
        screen.blit(title_text, title_text_rect)

        # Draw the "Enter Username" label and input box
        screen.blit(username_label_text, username_label_rect)
        pygame.draw.rect(screen, white, username_box, 0)  # White background for the username box
        username_surface = input_font.render(username_text, True, black)
        screen.blit(username_surface,
                    (username_box.x + 5, username_box.y + (username_box.height - username_surface.get_height()) // 2))

        # Draw the cursor if it's active
        if username_active and cursor_visible:
            cursor_x = username_box.x + 5 + username_surface.get_width()  # Position the cursor after the text
            pygame.draw.line(screen, black, (cursor_x, username_box.y + 5),
                             (cursor_x, username_box.y + username_box.height - 5), 2)

        # Draw the "Generate Join Code" button
        button_color_to_use = button_color if not generate_button_rect.collidepoint(
            pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(screen, button_color_to_use, generate_button_rect)
        screen.blit(generate_button_text, generate_button_text_rect)

        # If the join code is generated, show it and the "Share Join Code" button on the same line, below the generate button
        if join_code:
            # Adjust the position for the join code and share button, centering them together
            code_surface = button_font.render(f"Join Code: {join_code}", True, black)

            # Position the join code and share button horizontally aligned, below the generate button
            join_code_x = (
                                  width - code_surface.get_width() - share_button_rect.width - 10) // 2  # Center the join code with button
            join_code_y = generate_button_rect.bottom + 30  # Adjusted downward for more space

            # Draw the join code
            screen.blit(code_surface, (join_code_x, join_code_y))

            # Adjust the position of the "Share Join Code" button to line up perfectly with the join code
            share_button_rect.x = join_code_x + code_surface.get_width() + 10  # Place button directly after the code
            share_button_text_rect.center = share_button_rect.center  # Ensure text is centered inside the button

            # Draw the "Share Join Code" button
            button_color_to_use = button_color if not share_button_rect.collidepoint(
                pygame.mouse.get_pos()) else button_hover_color
            pygame.draw.rect(screen, button_color_to_use, share_button_rect)
            screen.blit(share_button_text, share_button_text_rect)

        pygame.display.flip()

        # Toggle the cursor every half a second to make it blink
        current_time = pygame.time.get_ticks()
        if current_time - cursor_time > 500:
            cursor_visible = not cursor_visible
            cursor_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    username_active = True
                else:
                    username_active = False

                if generate_button_rect.collidepoint(event.pos) and username_text.strip():
                    # Generate a random join code if username is provided
                    join_code = 72415  # Generate a 4-digit join code
                    show_share_button = True  # Enable share button

                if share_button_rect.collidepoint(event.pos) and join_code:
                    lobby_screen()

            elif event.type == pygame.KEYDOWN:
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.key == pygame.K_RETURN:  # Handle Enter key
                        username_active = False  # Deselect the text box
                    else:
                        username_text += event.unicode


def lobby_screen():
    global screen, players, player_points, player_usernames

    # Screen setup
    background_colour = (50, 205, 50)

    # Fonts
    font = pygame.font.SysFont("centurygothic", 48)
    input_font = pygame.font.SysFont("centurygothic", 32)
    button_font = pygame.font.SysFont("centurygothic", 28)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Join code
    join_code = 72415

    # Players
    players = []

    # Start button
    button_width = 300
    button_height = 60
    start_button_rect = pygame.Rect((width - button_width) // 2, height - 100, button_width, button_height)
    start_button_text = button_font.render("Start Game", True, black)
    start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)

    game_started = False
    running = True

    while running:
        screen.fill(background_colour)

        join_code_font = pygame.font.SysFont("centurygothic", 72)
        join_code_text = join_code_font.render(f"Join Code: {join_code}", True, black)
        join_code_text_rect = join_code_text.get_rect(center=(width // 2, 80))
        screen.blit(join_code_text, join_code_text_rect)

        if game_started:
            play_rounds()
        else:
            if len(players) == 0:
                waiting_message = input_font.render("Waiting for people to join...", True, black)
                waiting_message_rect = waiting_message.get_rect(center=(width // 2, height // 2 - 40))
                screen.blit(waiting_message, waiting_message_rect)
            else:
                for i, player in enumerate(players):
                    row = i // 2
                    col = i % 2
                    player_text = input_font.render(player, True, black)
                    player_text_rect = player_text.get_rect(
                        center=(width // 2 + col * 200 - 100, height // 2 + row * 60 - 40))
                    screen.blit(player_text, player_text_rect)

            pygame.draw.rect(screen, white, start_button_rect)
            screen.blit(start_button_text, start_button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    if len(players) > 0:
                        player_points = {player: 0 for player in players}  # Initialize player points
                        play_rounds()

                # Simulate players joining
                if len(players) < 4:
                    player = f"Player {len(players) + 1}"
                    players.append(player)
                    player_usernames[player] = f"User {len(players) + 1}"  # simulate usernames


def play_rounds():
    rounds = 10
    total_points = 0  # Initialize total points

    for round_num in range(1, rounds + 1):
        round_points = play_round(round_num, total_points)  # Pass total points to play_round
        total_points += round_points  # Add round points to total
    show_leaderboard()


def play_round(round, total_points=0):  # Add parameter for total points with default 0
    import rules
    import word_check
    import word_check
    import pygame
    import time

    pygame.init()

    prompt = rules.generate_rule(round)
    prompt_text = str(prompt)

    font = pygame.font.SysFont("centurygothic", 32)
    input_font = pygame.font.SysFont("centurygothic", 28)
    timer_font = pygame.font.SysFont("centurygothic", 24)

    # Game variables
    word_text = ''
    points = 0
    start_time = time.time()
    time_limit = 15
    sidebar_width = 100
    sidebar_rect = pygame.Rect(width - sidebar_width, 0, sidebar_width, height)

    # Define text box and cursor
    word_box = pygame.Rect(250, 150, 250, 40)
    active = True
    button_active = True
    cursor_visible = True
    cursor_timer = time.time()
    entered_text = ""
    valid_word = True
    last_word = ""

    # Enter button
    button_rect = pygame.Rect((width - sidebar_width - 160) // 2, 220, 160, 60)
    button_text = input_font.render("Enter", True, black)

    # Main game loop
    running = True
    while running:
        screen.fill((50, 205, 50))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and active == True:
                if word_box.collidepoint(event.pos):
                    active = True
                if button_rect.collidepoint(event.pos) and word_text.strip():
                    last_word = word_text
                    if word_check.check_word_valid(word_text.lower()) and prompt.check_word(word_text.lower()):
                        points = int(points + 10 + word_check.find_cat_similarity(word_text) * 100)
                        valid_word = True
                        entered_text = f"{points}"
                    else:
                        valid_word = False
                        entered_text = f"Invalid word! Points: {points}"
                    word_text = ''
                    active = False

            if event.type == pygame.KEYDOWN and active == True:
                if event.key == pygame.K_RETURN and word_text.strip():
                    last_word = word_text
                    if word_check.check_word_valid(word_text.lower()) and prompt.check_word(word_text.lower()):
                        points = int(points + 10 + word_check.find_cat_similarity(word_text) * 100)
                        valid_word = True
                        entered_text = f"{points}"
                    else:
                        valid_word = False
                        entered_text = f"Invalid word! Points: {points}"
                    word_text = ''
                    active = False
                elif active:
                    if event.key == pygame.K_BACKSPACE:
                        word_text = word_text[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        word_text += event.unicode

        # Draw the white card for the prompt with rounded corners
        prompt_card_rect = pygame.Rect(20, 40, width - sidebar_width - 40, 80)
        pygame.draw.rect(screen, (255, 255, 255), prompt_card_rect, border_radius=20)

        # Display prompt text
        prompt_surface = font.render(prompt_text, True, (0, 0, 0))
        text_width = prompt_surface.get_width()

        if text_width > prompt_card_rect.width - 20:
            prompt_text = "Must have 'EA' and ends with 'R'"
            prompt_surface = font.render(prompt_text, True, (0, 0, 0))

        screen.blit(prompt_surface,
                    (prompt_card_rect.x + (prompt_card_rect.width - text_width) // 2, prompt_card_rect.y + 20))

        # Set the text box color
        word_box_color = (255, 255, 255) if active else (200, 200, 200)
        pygame.draw.rect(screen, word_box_color, word_box)

        # Render the entered text in the input box
        word_surface = input_font.render(word_text, True, (0, 0, 0))
        screen.blit(word_surface, (word_box.x + 5, word_box.y + (word_box.height - word_surface.get_height()) // 2))

        # Display label "Enter a word" next to the input box
        label_text = "Enter a word:"
        label_surface = input_font.render(label_text, True, (0, 0, 0))
        screen.blit(label_surface, (
            word_box.x - label_surface.get_width() - 10,
            word_box.y + (word_box.height - label_surface.get_height()) // 2))

        # Draw the enter button
        mouse_pos = pygame.mouse.get_pos()
        button_color = (220, 220, 220) if button_rect.collidepoint(mouse_pos) else (255, 255, 255)
        pygame.draw.rect(screen, button_color, button_rect)
        button_text_width = button_text.get_width()
        button_text_height = button_text.get_height()
        screen.blit(button_text, (button_rect.x + (button_rect.width - button_text_width) // 2,
                                  button_rect.y + (button_rect.height - button_text_height) // 2))

        # Display feedback text below the Enter button
        if entered_text:
            feedback_color = (0, 100, 0) if valid_word else (200, 0, 0)
            enter_text_surface = input_font.render(entered_text, True, feedback_color)
            screen.blit(enter_text_surface,
                        (button_rect.x + (button_rect.width - enter_text_surface.get_width()) // 2,
                         button_rect.y + button_rect.height + 10))

        # Sidebar: Timer and Points
        pygame.draw.rect(screen, (255, 255, 255), sidebar_rect)

        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))
        timer_text = f"Time:"
        timer_value_text = f"{remaining_time}s"
        timer_text_surface = timer_font.render(timer_text, True, (0, 0, 0))
        timer_value_surface = timer_font.render(timer_value_text, True, (0, 0, 0))

        points_text = f"Points:"
        points_value_text = f"{total_points + points}"
        points_text_surface = timer_font.render(points_text, True, (0, 0, 0))
        points_value_surface = timer_font.render(points_value_text, True, (0, 0, 0))

        screen.blit(timer_text_surface, (width - sidebar_width + 10, 10))
        screen.blit(timer_value_surface, (width - sidebar_width + 10, 40))
        screen.blit(points_text_surface, (width - sidebar_width + 10, 100))
        screen.blit(points_value_surface, (width - sidebar_width + 10, 130))

        if active:
            if time.time() - cursor_timer > 0.5:
                cursor_visible = not cursor_visible
                cursor_timer = time.time()
            if cursor_visible:
                cursor_x = word_box.x + 5 + word_surface.get_width()
                cursor_y = word_box.y + (word_box.height - word_surface.get_height()) // 2
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y),
                                 (cursor_x, cursor_y + word_surface.get_height()), 2)

        pygame.display.flip()

        if time.time() - start_time > time_limit:
            give_encouragement(points, total_points + points)
            running = False
            for player in players:
                player_points[player] += points
            return points  # Return points earned in this round


def give_encouragement(points, player_score):
    pygame.init()

    # Set up screen
    # background_colour = (200, 255, 200)  # A soft green, playful background

    # Fonts
    font = pygame.font.SysFont("centurygothic", 48)
    small_font = pygame.font.SysFont("centurygothic", 32)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Simulated scores
    other_player_score = 250
    last_round_points = 50

    # Encouragement message
    if points >= 50:
        encouragement_text = "Purrfection! You're the cat's meow!"
        cat_image = pygame.image.load("happy_cat.png")
        cat_image = pygame.transform.scale(cat_image, (170, 170))
    elif points >= 10:
        encouragement_text = "Not bad! Keep going, paws-itively awesome!"
        cat_image = pygame.image.load("neutral_cat.png")
        cat_image = pygame.transform.scale(cat_image, (192, 148))
    else:
        encouragement_text = "Don't give up! You can do it, little kitty!"
        cat_image = pygame.image.load("sad_cat.png")
        cat_image = pygame.transform.scale(cat_image, (220, 150))

    # Scale image if needed

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

    # Timer setup
    counter = 5
    counter_start_time = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        screen.fill(background_colour)

        # Draw encouragement text
        wrapped_text = wrap_text(encouragement_text, font, width - 50)
        y_offset = 20
        for line in wrapped_text:
            encouragement_surface = font.render(line, True, black)
            encouragement_rect = encouragement_surface.get_rect(center=(width // 2, y_offset))
            screen.blit(encouragement_surface, encouragement_rect)
            y_offset += 50

        # Draw scores
        comparison_text = f"Your Score: {player_score} | Opponent's Score: {other_player_score}"
        comparison_surface = small_font.render(comparison_text, True, black)
        comparison_rect = comparison_surface.get_rect(center=(width // 2, y_offset + 20))
        screen.blit(comparison_surface, comparison_rect)


        # Draw image
        image_x = (width - cat_image.get_width()) // 2
        screen.blit(cat_image, (image_x, y_offset + 40))

        # Countdown timer
        time_left = counter - ((pygame.time.get_ticks() - counter_start_time) // 1000)
        timer_text = small_font.render(f"{time_left} seconds", True, black)
        timer_rect = timer_text.get_rect(center=(width // 2, height - 40))
        screen.blit(timer_text, timer_rect)

        if time_left <= 0:
            running = False

        pygame.display.flip()


def show_leaderboard():
    # Fonts
    font = pygame.font.SysFont("centurygothic", 48)  # Large font for "Leaderboard" title and player names
    input_font = pygame.font.SysFont("centurygothic", 32)  # Medium font for player scores
    button_font = pygame.font.SysFont("centurygothic", 28)  # Smaller font for button

    # Bold font for current player's name
    bold_font = pygame.font.SysFont("centurygothic", 32, bold=True)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    button_color = white  # Default button color
    button_hover_color = (200, 200, 255)  # Light blue hover color

    # Player data (for example purposes, this can be fetched from a database or passed dynamically)
    players_data = [{"name": player_usernames[player], "score": score} for player, score in player_points.items()]

    # Sort players by score in descending order to display the leaderboard
    players_data = sorted(players_data, key=lambda x: x['score'], reverse=True)

    # Simulate "current player" index (for highlighting the player in leaderboard)
    current_player_index = 0  # Let's assume the first player in the sorted list is the current player

    # Button setup
    button_width = 150
    button_height = 60
    button_spacing = 20  # Spacing between buttons
    play_again_button_rect = pygame.Rect((width - button_width * 2 - button_spacing) // 2, height - 70, button_width,
                                         button_height)
    exit_button_rect = pygame.Rect((width + button_width + button_spacing) // 2, height - 70, button_width,
                                   button_height)

    # Button text
    play_again_text = button_font.render("Play Again", True, black)
    exit_button_text = button_font.render("Exit", True, black)

    # Title for the leaderboard
    leaderboard_title = font.render("Leaderboard", True, black)
    leaderboard_title_rect = leaderboard_title.get_rect(center=(width // 2, 40))  # Moved further up to 40

    # Function to draw buttons with hover effect
    def draw_button(button_rect, button_text, is_hovering):
        button_color_to_use = button_hover_color if is_hovering else button_color
        pygame.draw.rect(screen, button_color_to_use, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    # Main loop
    running = True
    while running:
        screen.fill(background_colour)

        # Draw the Leaderboard Title at the top
        screen.blit(leaderboard_title, leaderboard_title_rect)

        # Display player names and scores
        y_offset = 120  # Start position for the first player entry
        for i, player in enumerate(players_data):
            player_name_surface = bold_font.render(player['name'], True,
                                                   black) if i == current_player_index else input_font.render(
                player['name'], True, black)
            player_score_surface = input_font.render(str(player['score']), True, black)

            # Center the player name and score horizontally
            player_name_rect = player_name_surface.get_rect(center=(width // 2 - 50, y_offset))
            player_score_rect = player_score_surface.get_rect(center=(width // 2 + 100, y_offset))

            screen.blit(player_name_surface, player_name_rect)
            screen.blit(player_score_surface, player_score_rect)

            y_offset += 40  # Increase vertical offset for the next player

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        draw_button(play_again_button_rect, play_again_text, play_again_button_rect.collidepoint(mouse_pos))
        draw_button(exit_button_rect, exit_button_text, exit_button_rect.collidepoint(mouse_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    lobby_screen()
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()


# Main loop
running = True
while running:
    if current_state == MAIN_MENU:
        draw_main_menu()
    elif current_state == JOIN_GAME:
        draw_join_game_screen()
    elif current_state == GAME_CODE_GENERATED:
        draw_game_code_generated_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_state == MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(30, 200, 420, 60).collidepoint(event.pos):
                    current_state = GAME_CODE_GENERATED
                elif pygame.Rect(30, 280, 420, 60).collidepoint(event.pos):
                    current_state = JOIN_GAME

pygame.quit()
sys.exit()