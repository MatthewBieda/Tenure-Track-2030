"""
Python Tkinter Splash Screen

This script holds the class SplashScreen, which is simply a window without
the top bar/borders of a normal window.

The window width/height can be a factor based on the total screen dimensions
or it can be actual dimensions in pixels. (Just edit the useFactor property)

Very simple to set up, just create an instance of SplashScreen, and use it as
the parent to other widgets inside it.
"""

from tkinter import *


class SplashScreen(Frame):
    def __init__(self, master=None, width=0.8, height=0.6, useFactor=True):
        Frame.__init__(self, master)
        self.pack(side=TOP, fill=BOTH, expand=YES)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 800
        h = 600
        # calculate position x, y
        x = 800
        y = 600
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.master.overrideredirect(True)
        self.lift()


if __name__ == '__main__':
    root = Tk()

    sp = SplashScreen(root)
    sp.config(bg="#3366ff")

    m = Label(sp, text="TENURE TRACK 2030\n\n\nStop Chris!\n\nArrow keys to move\nSpace to shoot Karel bullets!")
    m.pack(side=TOP, expand=YES)
    m.config(bg="#3366ff", justify=CENTER, font=("calibri", 29))

    Button(sp, text="Press this button to start!", bg='yellow', command=root.destroy).pack(side=BOTTOM, fill=X)
    root.mainloop()




import random
import math

import pygame
from pygame import mixer


# Initialize pygamep
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("dusk.jpg")

# Background sound
bgm = pygame.mixer.Sound("background.wav")
pygame.mixer.Channel(1).play(bgm, -1)

# Caption and Icon
pygame.display.set_caption("Tenure Track 2030")
icon = pygame.image.load("UFO.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("Mehran.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Chris.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("Karel.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
lose_font = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x, y):
    score = font.render("Score: " + str(score_value) + "/50", True, (0, 0, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = lose_font.render("CHRIS STOLE YOUR TENURE! ", True, (0, 255, 0))
    screen.blit(over_text, (25, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:


    # RGB values
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            play_again = font.render("Play again?: y/n ", True, (0, 255, 0))
            screen.blit(play_again, (275, 425))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    pygame.quit()
                elif event.key == pygame.K_y:
                    score_value = 0
                    for j in range(num_of_enemies):
                        enemyY[j] = 100


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            mehran_party = mixer.Sound("party time.wav")
            if random.randint(0, 5) == 3:
                mehran_party.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if score_value >= 50:
        you_win = over_font.render("YOU STOPPED CHRIS! ", True, (0, 255, 0))
        screen.blit(you_win, (50, 250))
        for i in range(num_of_enemies):
            enemyY[i] = -2000
        play_again = font.render("Play again?: y/n ", True, (0, 255, 0))
        screen.blit(play_again, (275, 425))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                pygame.quit()
            elif event.key == pygame.K_y:
                score_value = 0
                for j in range(num_of_enemies):
                    enemyY[j] = 100


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()