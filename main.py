import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
WHITE = (255, 255, 255)
GRAVITY = 0.5
STARTING_PIPE_GAP = 160
PIPE_GAP = STARTING_PIPE_GAP
FONT_SIZE = 40

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Coin Collector")

# Load Assets
background = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/flapybirdbackground.png")
bird1_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/bird.png")
bird2_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/bird2.png")
bird3_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/bird3.png")
pipe_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/pipe.png")
coin_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/coin.png")
coin_image = pygame.transform.scale(coin_image, (25, 25))
flappy_font = pygame.font.Font("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/fonts/flappy_font.ttf", FONT_SIZE)
restart_image = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/restart.png")

# Load Sounds
bg_music = pygame.mixer.Sound("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/sounds/bg_music.mp3")
jump_sound = pygame.mixer.Sound("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/sounds/jump.wav")
coin_sound = pygame.mixer.Sound("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/sounds/coin.wav")
game_over_sound = pygame.mixer.Sound("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/sounds/game_over.wav")

# Game Variables
clock = pygame.time.Clock()
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
score = 0
coins_collected = 0
paused = False
high_score = 0
game_active = False
show_home_screen = True
show_game_over_screen = False
show_high_score_screen = False

# Pipe and Coin Management
pipes = []
pipe_speed = 3
pipe_spawn_timer = 0
coins = []

# Bird animation
bird_frame = 0
bird_frame_timer = 0
bird_frames = [bird1_image, bird2_image, bird3_image]

# Restart button properties
restart_button_x = SCREEN_WIDTH // 2 - restart_image.get_width() // 2
restart_button_y = SCREEN_HEIGHT // 2 + 150
restart_button_rect = pygame.Rect(restart_button_x, restart_button_y, restart_image.get_width(), restart_image.get_height())

# Draw text function
def draw_text(text, font, color, center_x, center_y):
    # Render with black outline
    stroke_color = (0, 0, 0)  # Black
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Thin border offsets
    for dx, dy in offsets:
        text_surface = font.render(text, True, stroke_color)
        text_rect = text_surface.get_rect(center=(center_x + dx, center_y + dy))
        screen.blit(text_surface, text_rect)
    # Render main text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

# Reset game state function
def reset_game():
    global bird_y, bird_velocity, score, coins_collected, pipes, coins, pipe_spawn_timer, pipe_speed, PIPE_GAP, bird_frame, bird_frame_timer
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    score = 0
    coins_collected = 0
    pipes.clear()
    coins.clear()
    pipe_spawn_timer = 0
    pipe_speed = 3
    PIPE_GAP = STARTING_PIPE_GAP
    bird_frame = 0
    bird_frame_timer = 0

# Generate pipe with coin
def generate_pipe_with_coin(pipe_image, screen_width, gap):
    pipe_height = pipe_image.get_height()
    top_pipe_y = random.randint(-pipe_height + 100, -100)
    bottom_pipe_y = top_pipe_y + pipe_height + gap
    coin_x = screen_width + 50
    coin_y = top_pipe_y + pipe_height + (gap // 2) - (coin_image.get_height() // 2)
    return {
        "top": {"x": screen_width, "y": top_pipe_y, "image": pygame.transform.flip(pipe_image, False, True)},
        "bottom": {"x": screen_width, "y": bottom_pipe_y, "image": pipe_image},
        "coin": {"x": coin_x, "y": coin_y}
    }

# Check for collisions
def check_collisions(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]["x"], pipe["top"]["y"], pipe_image.get_width(), pipe_image.get_height()):
            return True
        if bird_rect.colliderect(pipe["bottom"]["x"], pipe["bottom"]["y"], pipe_image.get_width(), pipe_image.get_height()):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

# Main Game Loop
running = True
bg_music.play(-1)

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if show_home_screen:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    show_home_screen = False
                    reset_game()
                elif event.key == pygame.K_h:
                    show_high_score_screen = True
                    show_home_screen = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif show_game_over_screen:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif show_high_score_screen and event.key == pygame.K_RETURN:
                show_high_score_screen = False
                show_home_screen = True
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    bg_music.stop()
                else:
                    bg_music.play(-1)
            elif event.key == pygame.K_SPACE and game_active and not paused:
                bird_velocity = -8
                jump_sound.play()

        if show_game_over_screen and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(mouse_pos):
                reset_game()
                show_game_over_screen = False
                show_home_screen = True

    if show_home_screen:
        draw_text("FLAPPY COIN COLLECTOR", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text("PRESS ENTER TO PLAY", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("PRESS H FOR HIGH SCORE", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text("PRESS ESC FOR EXIT", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    elif show_high_score_screen:
        draw_text("HIGH SCORE", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(str(high_score), flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("PRESS ENTER TO RETURN", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    elif game_active:
        if not paused:
            bird_velocity += GRAVITY
            bird_y += bird_velocity
            bird_frame_timer += 1
            if bird_frame_timer > 5:
                bird_frame = (bird_frame + 1) % 3
                bird_frame_timer = 0

            pipe_spawn_timer += 1
            if pipe_spawn_timer > 90:
                new_pipe = generate_pipe_with_coin(pipe_image, SCREEN_WIDTH, PIPE_GAP)
                pipes.append(new_pipe)
                coins.append(new_pipe["coin"])
                pipe_spawn_timer = 0

                if PIPE_GAP > 120:
                    PIPE_GAP -= 2
                if pipe_speed < 6:
                    pipe_speed += 0.1

            pipes = [{"top": {"x": p["top"]["x"] - pipe_speed, "y": p["top"]["y"], "image": p["top"]["image"]},
                      "bottom": {"x": p["bottom"]["x"] - pipe_speed, "y": p["bottom"]["y"], "image": p["bottom"]["image"]},
                      "coin": {"x": p["coin"]["x"] - pipe_speed, "y": p["coin"]["y"]}} for p in pipes if p["top"]["x"] + pipe_image.get_width() > 0]

            coins = [{"x": c["x"] - pipe_speed, "y": c["y"]} for c in coins if c["x"] > 0]

            bird_rect = pygame.Rect(SCREEN_WIDTH // 4, bird_y, bird1_image.get_width(), bird1_image.get_height())

            if check_collisions(bird_rect, pipes):
                game_over_sound.play()
                game_active = False
                show_game_over_screen = True
                if score > high_score:
                    high_score = score

            for coin in coins[:]:
                coin_rect = pygame.Rect(coin["x"], coin["y"], coin_image.get_width(), coin_image.get_height())
                if bird_rect.colliderect(coin_rect):
                    coins_collected += 1
                    coin_sound.play()
                    coins.remove(coin)

            for pipe in pipes:
                screen.blit(pipe["top"]["image"], (pipe["top"]["x"], pipe["top"]["y"]))
                screen.blit(pipe["bottom"]["image"], (pipe["bottom"]["x"], pipe["bottom"]["y"]))

    # **New Code: Update score when bird passes the pipe**
                if pipe["top"]["x"] + pipe_image.get_width() < SCREEN_WIDTH // 4 and not pipe.get("scored", False):
                    score += 1
                    pipe["scored"] = True  # Mark this pipe as scored to prevent double counting

            for coin in coins:
                screen.blit(coin_image, (coin["x"], coin["y"]))

            screen.blit(bird_frames[bird_frame], (SCREEN_WIDTH // 4, bird_y))
            draw_text(f"Score: {score}", flappy_font, WHITE, SCREEN_WIDTH // 2, 30)
            draw_text(f"Coins: {coins_collected}", flappy_font, WHITE, SCREEN_WIDTH // 2, 70)

    elif show_game_over_screen:
        draw_text("GAME OVER", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(f"Score: {score}", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(f"High Score: {high_score}", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(restart_image, (restart_button_x, restart_button_y))

    pygame.display.update()
    clock.tick(60)
 