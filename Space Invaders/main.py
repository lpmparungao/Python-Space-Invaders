import pygame
import random
import math

# initialize pygame
pygame.init()

# create the screen
# any variable
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('bg.jpg')

# title
pygame.display.set_caption("Sample")
# icon
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# character
player_img = pygame.image.load('space-invaders.png')
playerX = 375
playerY = 510
playerX_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('shannen.png'))
    enemyX.append(random.randint(10, 735))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.4)
    enemyY_change.append(45)

# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

#score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

#game over
gameover_font = pygame.font.Font('freesansbold.ttf', 64)

#moving state
move_state = "steady"


# adding character
def Player(x, y):
    screen.blit(player_img, (x, y))


# adding enemy
def Enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 20, y + 5))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 32:
        return True
def show_score(x,y):
    score = score_font.render("Score : " + str(score_value), True, (152, 255, 152))
    screen.blit(score, (x,y))

def game_over_text():
    gameover_text = gameover_font.render("GAME OVER", True, (152, 255, 152))
    score_text = score_font.render("Score: " + str(score_value), True, (152, 255, 152))
    screen.blit(gameover_text, (200, 250))
    screen.blit(score_text, (350, 310))


# loop for windows
run = True
while run:
    # color only
    screen.fill((152, 255, 152))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # key stroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_a:
                playerX_change = -0.5
                move_state = "movingLeft"
            if event.key == pygame.K_d:
                playerX_change = 0.5
                move_state = "movingRight"
        if event.type == pygame.KEYUP:
            if move_state == "movingLeft":
                if event.key == pygame.K_a:
                    playerX_change = 0
                    move_state = "steady"
            if move_state == "movingRight":
                if event.key == pygame.K_d:
                    playerX_change = 0
                    move_state = "steady"

    playerX += playerX_change
    if playerX >= 736:
        playerX_change = 0
    if playerX <= 0:
        playerX_change = 0

    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 100)
            score_value += 1

        Enemy(enemyX[i], enemyY[i], i)

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


    Player(playerX, playerY)
    show_score(scoreX,scoreY)

    pygame.display.update()
