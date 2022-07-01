import random
import sys
import math
import pygame
from pygame import mixer
import time


pygame.init()

screen = pygame.display.set_mode((289,511))

background = pygame.image.load("background.png")
base = pygame.image.load("base.png")

pygame.display.set_caption("FLAPPY BIRD")
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)


playerImg = pygame.image.load("bird.png")
playerX = 50
playerY = 250
playerY_change = 0.6

die=mixer.Sound("die.wav")
point=mixer.Sound("point.wav")
hit=mixer.Sound("hit.wav")
wing=mixer.Sound("wing.wav")

def player(x, y):
    screen.blit(playerImg, (x, y))

pipe_image=pygame.image.load("pipe.png")
flip_pipe=pygame.transform.flip(pipe_image,False,True)

p1x=300
p1y=random.randint(200,300)

p2x=450
p2y=random.randint(200,300)

p3x=300
p3y=p1y-420

p4x=450
p4y=p2y-420
pc=-1

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 32)

def pipe(x,y):
    screen.blit(pipe_image,(x,y))

def pipe2(x,y):
    screen.blit(flip_pipe,(x,y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
   

def game_over_text():
    die.play()
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (30, 250))
    time.sleep(3)
    pygame.quit()
    sys.exit()

h= pipe_image.get_height()
w=flip_pipe.get_width()
hp=playerImg.get_height()


def collide(playerX, playerY, p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y):

    if(playerY<h+p3y and abs(playerX-p3x)<w):
         game_over_text()
         
         
         
    elif(playerY<h+p4y and abs(playerX-p4x)<w):
         game_over_text()
         
         
         
    elif(playerY+hp>p1y and abs(playerX-p1x)<w):
         game_over_text()
         
         
    elif(playerY+hp>p2y and abs(playerX-p2x)<w):
         game_over_text()
         
run=True        
while run:
    
    screen.blit(background, (0, 0))

    pipe(p1x,p1y)
    pipe(p2x,p2y)
    pipe2(p3x,p3y)
    pipe2(p4x,p4y)
    
    screen.blit(base, (0,400))
    
    playerY_change = 0.6
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerY_change = -45
                wing.play()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                playerY_change = 0

    playerY+=playerY_change
    
    collide(playerX, playerY, p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y)
    
    if playerY>=390 or playerY<=0:
       die.play()
       game_over_text()
    
    pc=-1
    p1x+=pc
    p2x+=pc
    p3x+=pc
    p4x+=pc


    if p1x<=-40:
        p1x=300
        p1y=random.randint(200,350)

    if p2x<=-40:
         p2x=300
         p2y=random.randint(200,350)

    if p3x<=-40:
         p3x=300
         p3y=p1y-450
         
    if p4x<=-40:
         p4x=300
         p4y=p2y-450

    if p1x==50 or p2x==50:
        score_value+=1
        point.play()
        
    player(playerX, playerY)
    show_score(textX, testY)
   
    
    pygame.display.update()
    

