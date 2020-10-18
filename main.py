import pygame
import random
import time
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
mixer.music.load("background.wav")
mixer.music.play(-1)

screen_width = 500
screen_height = 500
display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dragon Game")
icon = pygame.image.load("dragon.png")
pygame.display.set_icon(icon)
boomimg = pygame.image.load("boom.png")
# player
playerimg = pygame.image.load("dragon.png")
playerx = 10
playery = screen_height - 60
yChange = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyyChange = []
enemyxChange = []

numofenemies = 7

speed = 60

for i in range(numofenemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(330, 450))
    enemyy.append(random.randint(150, 440))
    enemyyChange.append(5)
    enemyxChange.append(20)

# fire
fireimg = pygame.image.load("fire2.png")
firex = 20
firey = screen_height - 60
fireyChange = 0
firexChange = 10
fire_state = "ready"

# scoreformat

scorevalue = 0
font = pygame.font.Font("freesansbold.ttf", 18)
textX = 10
texty = 10

gameover = pygame.font.Font("freesansbold.ttf", 32)


def player(x, y):
    display.blit(playerimg, (x, y))


def enemy(x, y, i):
    display.blit(enemyimg[i], (x, y))


def fire(x, y):
    global fire_state
    fire_state = "fire"
    display.blit(fireimg, (x + 25, y + 20))


def iscollision(enemyy, enemyx, firey, firex):
    distance = math.sqrt((math.pow(enemyx - firex, 2)) + (math.pow(enemyy - firey, 2)))
    if distance < 18:
        return True
    else:
        return False


def showScore(x, y):
    score = font.render("score: " + str(scorevalue), True, (255, 255, 255))
    display.blit(score, (x, y))


def gameovershow():
    display.fill((0, 100, 200))
    over_text = gameover.render("GAME OVER", True, (255, 0, 0))
    display.blit(over_text, (150, 150))
    over_text = gameover.render("Your Final Score is " + str(scorevalue), True, (255, 0, 0))
    display.blit(over_text, (90, 190))

game = False
while not game:
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                yChange = -5
            if event.key == pygame.K_DOWN:
                yChange = 5
            if event.key == pygame.K_SPACE:
                if fire_state == "ready":
                    firesound = mixer.Sound("laser.wav")
                    firesound.play()
                    firey = playery
                    fire(firex, firey)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                yChange = 0
    if playery <= 0:
        playery = 0
    elif playery >= 440:
        playery = 440
    playery += yChange
    for i in range(numofenemies):
        if enemyx[i] < 64:
            for j in range(numofenemies):
                enemyy[j] = 2000
            gameovershow()
            playery += 10

        if enemyy[i] <= 0:
            enemyyChange[i] = 5
            enemyx[i] -= enemyxChange[i]
        elif enemyy[i] >= 440:
            enemyyChange[i] = -5
            enemyx[i] -= enemyxChange[i]
        enemyy[i] += enemyyChange[i]

        collision = iscollision(enemyy[i], enemyx[i], firey, firex)
        if collision:
            collisionsound = mixer.Sound("Explosion3.wav")
            collisionsound.play()
            display.blit(boomimg,(enemyy[i], enemyy[i]))
            firex = 30
            fire_state = "ready"
            scorevalue += 1
            if scorevalue == 30 or scorevalue == 60:
                speed += 20
            elif scorevalue == 100:
                speed += 20
            enemyx[i] = random.randint(330, 450)
            enemyy[i] = random.randint(150, 440)

        enemy(enemyx[i], enemyy[i], i)
    if firex >= 500:
        firex = 30
        fire_state = "ready"
    if fire_state == "fire":
        fire(firex, firey)
        firex += firexChange

    player(playerx, playery)
    showScore(textX, texty)
    clock.tick(speed)
    pygame.display.update()
