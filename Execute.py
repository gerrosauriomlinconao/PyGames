import pygame,os
import random
import math
from pygame import mixer
#centra la ventana:
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('images/background.png')
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

running = True
#Title and icon
pygame.display.set_caption("Titulo")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('images/spaceship.png')
playerX = 340
playerY = 465
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change  = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy1.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(15)
    enemyY_change.append(15)

#bullet:
#ready you can't see the bullet on the screen
#fire is currently moving
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 15
bulletY_change = 25
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textx = 10
texty = 10

#game over text
gover_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = gover_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))

def show_Score(x,y):
    score = font.render("Puntos: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 75, y +10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance < 60:
       return True
    else:
        return False

#GameLoop
while running:
    # RGB values
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its tight or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #cheking for boundaries of spaceship
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 650:
        playerX = 650

    # Enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 420:
            for J in range(num_of_enemies):
                enemyY[J] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 20 #velocidad de movimiento
        elif enemyX[i] >= 720:
            enemyX_change[i] = -20 #velocidad de movimiento
            enemyY[i] += enemyY_change[i]
        # Collision
        colision = isCollision(enemyY[i], enemyY[i], bulletX, bulletY)
        if colision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,100)

        enemy(enemyX[i], enemyY[i],i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change




    player(playerX,playerY)
    show_Score(textx,texty)
    pygame.display.update()

