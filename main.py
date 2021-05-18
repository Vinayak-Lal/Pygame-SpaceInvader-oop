import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, (800, 600))


class Position_Parameters:
    def __init__(self, x, y, xchange, ychange):
        self.x = x
        self.y = y
        self.xchange = xchange
        self.ychange = ychange


class Enemy(Position_Parameters):

    def draw(self, x, y):
        self.image = pygame.image.load('alien.png')
        screen.blit(self.image, (x, y))


class Player(Position_Parameters):

    def draw(self, x, y):
        self.image = pygame.image.load('astronomy.png')
        screen.blit(self.image, (x, y))


class Bullet(Position_Parameters):

    def draw(self, x, y):
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        screen.blit(self.image, (x + 16, y + 10))


class button:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        font4 = pygame.font.Font('Crowd Pleaser DEMO.otf', 60)
        again_text = font4.render("Play Again", True, (255, 255, 255))
        screen.blit(again_text, (self.x + (self.width / 2) - (again_text.get_width()) / 2,
                                 self.y + (self.height / 2) - (again_text.get_height()) / 2))

    def click(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height)


##Creating player
player = Player(370, 480, 0, 0)
# Creating Enemy
enemy = []
numenemies = 6
for i in range(numenemies):
    enemy.append(Enemy(random.randint(0, 735), random.randint(0, 100), 2, 30))

# bullet
bullet = Bullet(player.x, player.y, 0, 3)
bullet_state = "rest"

gamestate = "active"

count = 0
font = pygame.font.Font('Crowd Pleaser DEMO.otf', 32)
score = 0
font2 = pygame.font.Font('Crowd Pleaser DEMO.otf', 100)
font3 = pygame.font.Font('Crowd Pleaser DEMO.otf', 60)
mixer.music.load('background.wav')
mixer.music.play(-1)

game_over_button = button(320, 300, 200, 70, (0, 0, 255))


def show_score(x, y):
    score_text = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def game_over_text(x, y):
    game = font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game, (x, y))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2))
    return distance < 27


running = True
while (running):
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.xchange = -1
            if event.key == pygame.K_RIGHT:
                player.xchange = 1
            # firing bullets
            if event.key == pygame.K_SPACE and bullet_state == "rest":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bullet.x = player.x
                bullet.draw(bullet.x, bullet.y)
                bullet.y += bullet.ychange
                bullet_state = "motion"

        if event.type == pygame.KEYUP:
            player.xchange = 0
        # option to play again
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gamestate == "over":
                pos = pygame.mouse.get_pos()
                if game_over_button.click(pos):
                    gamestate = "active"
                    for j in range(numenemies):
                        enemy[j].x = random.randint(0, 735)
                        enemy[j].y = random.randint(0, 100)
                    score = 0
                    count = 0

    for i in range(numenemies):
        ##How the game ends
        if ((player.y - enemy[i].y) <= 40 ):

            for j in range(numenemies):
                enemy[j].y = 3000
            game_over_text(250, 100)

            gamestate = "over"
            game_over_button.draw(screen)

            if count == 0:
                oversound = mixer.Sound('giddylaugh.wav')
                oversound.play()
                count = 1
            break
        ##enemy movement
        if enemy[i].xchange + enemy[i].x >= 736 or enemy[i].xchange + enemy[i].x <= 0:

            enemy[i].y += enemy[i].ychange

            if enemy[i].x + enemy[i].xchange >= 736:
                enemy[i].x = 736
            else:
                enemy[i].x = 0
            enemy[i].y += enemy[i].ychange
            enemy[i].xchange = -enemy[i].xchange
        enemy[i].x += enemy[i].xchange

        ##coliision
        if iscollision(enemy[i].x, enemy[i].y, bullet.x, bullet.y):
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            score += 1
            enemy[i].x = random.randint(0, 735)
            enemy[i].y = random.randint(0, 100)
            bullet_state = "rest"
            bullet.y = player.y
        enemy[i].draw(enemy[i].x, enemy[i].y)

    ##player movement
    if 0 <= (player.x + player.xchange) <= 736:
        player.x += player.xchange

    ##bullet movement
    if bullet_state == "motion":
        bullet.draw(bullet.x, bullet.y)
        bullet.y -= bullet.ychange
    if bullet.y <= 0:
        bullet_state = "rest"
        bullet.y = player.y

    player.draw(player.x, player.y)
    show_score(10, 10)
    pygame.display.update()
