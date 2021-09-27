import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Hunters")
icon = pygame.image.load("images/launch.png")
pygame.display.set_icon(icon)

background = pygame.image.load("images/space.jpg")
mixer.music.load("music/background.wav")
mixer.music.play(-1)

playerimg = pygame.image.load("images/space-invaders.png")
playerX= 370
playerY= 480
playerX_change=0

special_enemy_img = pygame.image.load("images/asteroid.png")
special_enemyX=random.randint(0,300)
special_enemyY=random.randint(-2000,-1999)

aestroidX=random.randint(400,736)
aestroidY=random.randint(-1000,-999)


enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

for i in range(6):
    enemyimg.append(pygame.image.load("images/ufo.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append( random.randint(50,150))
    enemyX_change.append(0.6)
    enemyY_change.append(40)


bulletimg = pygame.image.load("images/bullet.png")
bulletX=0
bulletY= 480
bulletX_change=0
bulletY_change=1
bullet_state="ready"


score_value=0
font=pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10

over_font=pygame.font.Font("freesansbold.ttf",64)

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def is_collision(x1,x2,y1,y2):
    distance = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
    if distance<27:
        return True

def special_enemy(x,y):
    screen.blit(special_enemy_img, (x, y))


def show_score(x,y):
    score=font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    score = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(score, (200, 250))



running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-1.2
            if event.key==pygame.K_RIGHT:
                playerX_change=1.2
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("music/laser.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change=0

    playerX +=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    for i in range(6):
        if enemyY[i]>440 or is_collision(special_enemyX, playerX, special_enemyY, playerY) or is_collision(aestroidX, playerX, aestroidY, playerY):
            for j in range(6):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            if score_value>20:
                enemyX_change[i]=1
            else:
                enemyX_change[i] = 0.65
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            if score_value>20:
                enemyX_change[i]=-1
            else:
                enemyX_change[i] = -0.65
            enemyY[i] += enemyY_change[i]

        special_enemyY += 0.12
        special_enemyX+=0.03
        if special_enemyY >= 600:
            special_enemyY = random.randint(-2000, -1999)
            special_enemyX = random.randint(0, 300)

        aestroidY += 0.1
        aestroidX -= 0.03
        if aestroidY >= 600:
            aestroidY = random.randint(-1000, -999)
            aestroidX = random.randint(400, 736)

        collision = is_collision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision is True :
            collision_sound = mixer.Sound("music/explosion.wav")
            collision_sound.play()
            score_value+=1
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)
        collision = is_collision(special_enemyX, bulletX, special_enemyY, bulletY)
        if collision is True and bullet_state is not "ready":
            bulletY = 480
            bullet_state = "ready"
        special_enemy(special_enemyX, special_enemyY)

        collision = is_collision(aestroidX, bulletX, aestroidY, bulletY)
        if collision is True and bullet_state is not "ready":
            bulletY = 480
            bullet_state = "ready"
        special_enemy(aestroidX, aestroidY)

    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()



