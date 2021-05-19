# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:44:15 2019

@author: SPORYKHIN
"""

import pygame
import time
import random
pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Touhou 2.71: The Rising of Tutu')
clock = pygame.time.Clock()

reimuImg=pygame.image.load('Reimu small.png')
bfairyImg=pygame.image.load('bfairy.png')
gfairyImg=pygame.image.load('gfairy.png')
rfairyImg=pygame.image.load('rfairy.png')
danmakul = []
(reimu_width,reimu_height) = reimuImg.get_rect().size
(fairy_width,fairy_height) = bfairyImg.get_rect().size

def fairy(x,y):
    fairyobject = gameDisplay.blit(bfairyImg,(x,y))    
    return fairyobject

def reimu(x,y):
    reimuobject = gameDisplay.blit(reimuImg,(x,y))
    return reimuobject

def text_objects(text, font):
    textSurface= font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

    game_loop()

def death():
    message_display('You died!')

def game_loop():
    x = (display_width * 0.45)
    y =  (display_height * 0.8)

    x_change = 0
    y_change = 0
    k_right = False
    k_left = False
    k_up = False
    k_down = False
    z_down = False
    
    fairy_startx = random.randrange(0, display_width)
    fairy_starty = -600
    fairy_speed = 3
    
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    k_left = True
                if event.key == pygame.K_RIGHT:
                    k_right = True
                if event.key == pygame.K_UP:
                    k_up = True
                if event.key == pygame.K_DOWN:
                    k_down = True
                if event.key == pygame.K_z:
                    z_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    k_left = False
                    x_change = 0
                if event.key == pygame.K_RIGHT:
                    k_right = False
                    x_change = 0
                if event.key == pygame.K_UP:
                    k_up = False
                    y_change = 0
                if event.key == pygame.K_DOWN:
                    k_down = False
                    y_change = 0
                if event.key == pygame.K_z:
                    z_down = False

        if k_left:
            x_change = -5
            if x<0:
                x_change = 0
        if k_right:
            x_change = 5
            if x > display_width-reimu_width:
                x_change = 0
        if k_right and k_left:
            x_change = 0
        if k_up:
            y_change = -5
            if y<0:
                y_change=0
        if k_down:
            y_change = 5
            if y > display_height-reimu_height:
                y_change=0
        if k_up and k_down:
            y_change = 0
        
        
        x+= x_change
        y+= y_change
        
        gameDisplay.fill(black)
        
        fairypos = fairy(fairy_startx, fairy_starty)
        fairy_starty += fairy_speed
        reimupos = reimu(x,y)
        pygame.draw.circle(gameDisplay, white, (50, 50), 100)
        if fairy_starty > display_height:
            fairy_starty = 0 - fairy_height
            fairy_startx = random.randrange(0,display_width)
            
        colliding = reimupos.colliderect(fairypos)
        
        if colliding:
            pygame.draw.rect(gameDisplay, red, reimupos.clip(fairypos))
            death()
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
