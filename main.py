from typing import Text
import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# Initialize window
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Variables
FPS = 60
VEL = 6
BULLET_VEL = 6  
ENEMY_VEL = 3
SHIP_WIDTH = 40
SHIP_HEIGHT = 40
ENEMY_WIDTH = 33
ENEMY_HEIGHT = 24
MAX_BULLETS = 3
ENEMY_DIR = 1
BORDER = pygame.Rect(0, HEIGHT//3-3, WIDTH, 6)

# Hit events
ENEMY_HIT = pygame.USEREVENT+1
SHIP_HIT = pygame.USEREVENT+2

# Load assets
SHIP_IMAGE = pygame.image.load(os.path.join("assets", "ship.png"))
ENEMY_IMAGE = pygame.image.load(os.path.join("assets", "enemy.png"))
BG_IMAGE = pygame.image.load(os.path.join("assets", "stars.jpg"))
BLASTER = pygame.mixer.Sound(os.path.join("assets", "sf_laser_15.mp3"))
ENEMY_EXPLODE = pygame.mixer.Sound(os.path.join("assets", "Explosion+1.mp3"))
BGM = os.path.join("assets", "bgm.mp3")

# Scale assets
SHIP = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
BG = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

# Fonts 
INFO_FONT = pygame.font.SysFont('ubuntumono', 30) # Define font

# Play music
pygame.mixer.music.load(BGM)
pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.

# Draws elements to be displayed on WIN
def draw_display(ship, enemies, bullets):
    WIN.fill(BLACK)
    WIN.blit(BG, (0, 0))
    WIN.blit(SHIP, (ship.x, ship.y))

    # Draw bullet inside bullets list
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # Draw enemy from enemies list
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))

    pygame.display.update()

# Shows text containing player stats
def draw_text(lives, hits, level):
    lives_text = INFO_FONT.render(f"LIVES: {str(lives)}", 1, WHITE)
    hits_text = INFO_FONT.render(f'HITS: {str(hits)}', 1, WHITE)
    level_text = INFO_FONT.render(f"LEVEL: {str(level)}", 1, WHITE)
    WIN.blit(level_text, (2, 2))
    WIN.blit(hits_text, (2, 2+level_text.get_height()))
    WIN.blit(lives_text, (WIDTH-2-lives_text.get_width(), 2))
    pygame.display.update()

# Moves player ship depending on the keys pressed
def move_ship(ship):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship.y-VEL > BORDER.y:
        ship.y -= VEL
    if keys[pygame.K_DOWN] and ship.y+VEL < HEIGHT-SHIP_HEIGHT:
        ship.y += VEL
    if keys[pygame.K_LEFT] and ship.x-VEL > 0:
        ship.x -= VEL
    if keys[pygame.K_RIGHT] and ship.x+VEL < WIDTH-SHIP_WIDTH:
        ship.x += VEL

# Automatically moves enemy based on a certain pattern
def move_enemy(enemies, ship, speed=ENEMY_VEL):
    for enemy in enemies:
        if enemy.x+speed > WIDTH-enemy.width:
            enemy.x = 0
            enemy.y += 30
        elif enemy.colliderect(ship):
            pygame.event.post(pygame.event.Event(SHIP_HIT))
            enemies.remove(enemy)
        else: enemy.x += speed

# Function storing bullet movements code
def move_bullets(bullets):
    for bullet in bullets:
        bullet.y -= BULLET_VEL

# Checks if enemy was hit or if the player was hit by an enemy
def collide_check(ship, bullets, enemies):
    for bullet in bullets:
        if bullet.y < -10:
            bullets.remove(bullet)
        for enemy in enemies:
            if bullet.colliderect(enemy):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                enemies.remove(enemy)
                bullets.remove(bullet)
            elif enemy.colliderect(ship):
                pygame.event.post(pygame.event.Event(SHIP_HIT))
                enemies.remove(enemy)
            
def main():
    enemy = pygame.Rect(WIDTH//2-ENEMY_WIDTH//2, 90, ENEMY_WIDTH, ENEMY_HEIGHT)
    ship = pygame.Rect(WIDTH//2-SHIP_WIDTH//2, 500, SHIP_WIDTH, SHIP_HEIGHT)
    clock = pygame.time.Clock()
    level = 0
    wave = 0
    lives = 5
    hits = 0
    enemy_vel = 3
    
    bullets = []
    enemies = []

    run = True

    # Run game
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Shoot bullet if player hasn't used a full round of bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(ship.x+ship.width//2-2, ship.y-ship.height+5, 3, 10)
                    bullets.append(bullet)
                    BLASTER.play()
            
            # Activated depending on event type
            if event.type == ENEMY_HIT:
                hits += 1
                ENEMY_EXPLODE.play()
            
            if event.type == SHIP_HIT:
                lives -= 1

        # Create enemy waves 
        if len(enemies) == 0:
            level += 1
            if wave <= 9:
                wave += 2
            else: enemy_vel += 1
             
            for i in range(0, wave):
                enemy = pygame.Rect((40*i)+5, 40, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy)

        draw_display(ship, enemies, bullets)
        draw_text(lives, hits, level)
        move_enemy(enemies, ship, enemy_vel)
        move_bullets(bullets)
        collide_check(ship, bullets, enemies)
        move_ship(ship)

if __name__ == "__main__":
    main()
                






