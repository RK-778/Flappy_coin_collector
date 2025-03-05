import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 1
PIPE_GAP = 160
FONT_SIZE = 40
ANIMATION_SPEED = 2 # Speed of bird animation

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Coin Collector")

# Load and Scale Background
background = pygame.image.load("C:/Users/ragha/OneDrive/Desktop/RK_flappy/rk/assets/images/flapybirdbackground.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Bird Animation Frames
bird_frames = [
    pygame.image.load("rk/assets/images/bird.png"),
    pygame.image.load("rk/assets/images/bird2.png"),
    pygame.image.load("rk/assets/images/bird3.png")
]
bird_index = 0

pipe_image = pygame.image.load("rk/assets/images/pipe.png")
coin_image = pygame.image.load("rk/assets/images/coin.png")
coin_image = pygame.transform.scale(coin_image, (25, 25))
flappy_font = pygame.font.Font("rk/assets/fonts/flappy_font.ttf", FONT_SIZE)
restart_image = pygame.image.load("rk/assets/images/restart.png")
restart_rect = restart_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Load Sounds
bg_music = pygame.mixer.Sound("rk/assets/sounds/bg_music.mp3")
jump_sound = pygame.mixer.Sound("rk/assets/sounds/jump.wav")
coin_sound = pygame.mixer.Sound("rk/assets/sounds/coin.wav")
game_over_sound = pygame.mixer.Sound("rk/assets/sounds/game_over.wav")

# Game Variables
clock = pygame.time.Clock()
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
score = 0
coins_collected = 0
game_active = False
show_home_screen = True
pipes = []
score_timer = 0

# Background Scrolling Variables
bg_x = 0
bg_speed = 2

# Function to Draw Text with Black Border
def draw_text(text, font, color, center_x, center_y):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    for offset_x in [-0.3, 0.1]:
        for offset_y in [-0.1, -0.3]:
            screen.blit(font.render(text, True, BLACK), (text_rect.x + offset_x, text_rect.y + offset_y))
    screen.blit(font.render(text, True, color), text_rect)

# Function to Reset Game
def reset_game():
    global bird_y, bird_velocity, score, coins_collected, pipes, game_active, score_timer
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    score = 0
    coins_collected = 0
    pipes.clear()
    game_active = True
    score_timer = 0

# Function to Check Collisions
def check_collisions(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT

# Function to Generate Pipes and Coin
def generate_pipes():
    pipe_height = random.randint(100, 400)
    top_pipe = pipe_image.get_rect(midbottom=(SCREEN_WIDTH + 100, pipe_height - PIPE_GAP // 2))
    bottom_pipe = pipe_image.get_rect(midtop=(SCREEN_WIDTH + 100, pipe_height + PIPE_GAP // 2))
    coin_rect = coin_image.get_rect(center=(SCREEN_WIDTH + 100, pipe_height))
    return {"top": top_pipe, "bottom": bottom_pipe, "coin": coin_rect, "collected": False}

# Function to Move Pipes and Coin
def move_pipes(pipes):
    for pipe in pipes:
        pipe["top"].centerx -= 5
        pipe["bottom"].centerx -= 5
        pipe["coin"].centerx -= 5
    return pipes

# Function to Draw Pipes and Coin
def draw_pipes(pipes):
    for pipe in pipes:
        flipped_pipe = pygame.transform.flip(pipe_image, False, True)  # Rotate top pipe
        screen.blit(flipped_pipe, pipe["top"])  # Draw rotated top pipe
        screen.blit(pipe_image, pipe["bottom"])  # Draw normal bottom pipe
        if not pipe["collected"]:
            screen.blit(coin_image, pipe["coin"])

# Game Loop
running = True
bg_music.play(-1)
animation_counter = 0  # Animation control

while running:
    screen.fill(WHITE)

    # Scroll background
    bg_x -= bg_speed
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

    # Draw scrolling background
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + SCREEN_WIDTH, 0))

    # Event Handling
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
            elif event.key == pygame.K_SPACE and game_active:
                bird_velocity = -8
                jump_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_active and not show_home_screen:
            if restart_rect.collidepoint(event.pos):
                reset_game()

    # Show Home Screen
    if show_home_screen:
        draw_text("FLAPPY COIN COLLECTOR", flappy_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    
    # Game Logic
    if game_active:
        score_timer += 1
        if score_timer % 30 == 0:
            score += 1

        bird_velocity += GRAVITY
        bird_y += bird_velocity
        bird_rect = bird_frames[bird_index].get_rect(center=(100, bird_y))

        animation_counter += 1
        if animation_counter >= ANIMATION_SPEED:
            bird_index = (bird_index + 1) % len(bird_frames)
            animation_counter = 0

        if len(pipes) == 0 or pipes[-1]["top"].right < SCREEN_WIDTH - 200:
            pipes.append(generate_pipes())

        pipes = move_pipes(pipes)
        if pipes[0]["top"].right < 0:
            pipes.pop(0)

        draw_pipes(pipes)
        screen.blit(bird_frames[bird_index], bird_rect)

        if check_collisions(bird_rect, pipes):
            game_active = False
            game_over_sound.play()

        for pipe in pipes:
            if bird_rect.colliderect(pipe["coin"]) and not pipe["collected"]:
                coins_collected += 1
                score += 5
                coin_sound.play()
                pipe["collected"] = True

        draw_text(f"Score: {score}", flappy_font, WHITE, SCREEN_WIDTH // 2, 50)
        draw_text(f"Coins: {coins_collected}", flappy_font, WHITE, SCREEN_WIDTH // 2, 100)
    elif not show_home_screen:
        screen.blit(restart_image, restart_rect)

    pygame.display.update()
    clock.tick(30)
