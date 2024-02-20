import pygame
import random
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 515
PLAYER_SPEED = 5
COIN_SPEED = 3
BOMB_SPEED = 4
COIN_SCORE = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GoGoRun!")

background_img = pygame.image.load("bg.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

menu_img = pygame.image.load("bg2.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load("player4.png")
player_img = pygame.transform.scale(player_img, (100, 100))

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (60, 60))

bomb_img = pygame.image.load("bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (90, 90))

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 95

# Основной игровой цикл
running = True
score = 0
lives = 3
coins = []
bombs = []

def create_objects():
    if random.randint(1, 100) <= 3:
        coins.append(pygame.Rect(random.randint(0, SCREEN_WIDTH-30), 0, 60, 60))
    elif random.randint(1, 100) <= 2:
        bombs.append(pygame.Rect(random.randint(0, SCREEN_WIDTH-30), 0, 90, 90))

def show_text(text, x, y, color):
    font = pygame.font.SysFont('Century Gothic', 30)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def show_menu():
    menu_running = True
    while menu_running:
        screen.blit(menu_img, (0, 0))
        show_text("GoGoRun!", 430, 100, (253, 255, 237))
        show_text("Нажмите 'S' чтобы начать игру", 330, 240, (253, 255, 237))
        show_text("Нажмите 'Q' чтобы выйти", 330, 300, (253, 255, 237))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_running = False
                if event.key == pygame.K_q:
                    menu_running = False

def restart_game():
    global score, lives, coins, bombs
    score = 0
    lives = 3
    coins = []
    bombs = []
    show_menu()

show_menu()
while running:
    screen.blit(background_img, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH-30:
        player_x += PLAYER_SPEED

    # Движение монеток и бомб
    for coin in coins:
        coin.y += COIN_SPEED
        if coin.colliderect(pygame.Rect(player_x, player_y, 100, 100)):
            coins.remove(coin)
            score += COIN_SCORE
    for bomb in bombs:
        bomb.y += BOMB_SPEED
        if bomb.colliderect(pygame.Rect(player_x, player_y, 100, 100)):
            bombs.remove(bomb)
            lives -= 1

    create_objects()

    # Отображение игрока и объектов
    screen.blit(player_img, (player_x, player_y))
    for coin in coins:
        screen.blit(coin_img, coin)
    for bomb in bombs:
        screen.blit(bomb_img, bomb)

    show_text(f"Счет: {score}", 10, 10, (253, 255, 237))
    show_text(f"Жизни: {lives}", 10, 50, (253, 255, 237))

    if lives <= 0:
        screen.blit(menu_img, (0, 0))
        show_text("Game Over", 400, 190, (253, 255, 237))
        show_text(f"Ваш счет: {score}", 395, 240, (253, 255, 237))
        show_text(f"Нажмите 'R' чтобы начать сначала", 280, 290, (253, 255, 237))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                if event.key == pygame.K_q:
                    running = False

    pygame.display.flip()

with open("results.txt", "a") as file:
    file.write(str(score) + "\n")

pygame.quit()
