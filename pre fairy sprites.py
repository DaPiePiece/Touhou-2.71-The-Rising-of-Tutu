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
(reimu_width,reimu_height) = reimuImg.get_rect().size

def projectile(projx, projy, projw, projh, colour):
    pygame.draw.rect(gameDisplay, colour, [projx, projy, projw, projh])

def reimu(x,y):
    gameDisplay.blit(reimuImg,(x,y))

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

def crash():
    message_display('You crashed!')

def game_loop():
    x = (display_width * 0.45)
    y =  (display_height * 0.8)

    x_change = 0
    y_change = 0
    k_right = False
    k_left = False
    k_up = False
    k_down = False
    
    proj_startx = random.randrange(0, display_width)
    proj_starty = -600
    proj_speed = 7
    proj_width = 100
    proj_height = 100
    
    gameExit = False

    while not gameExit:

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

        if k_left:
            x_change = -5
        if k_right:
            x_change = 5
        if k_right and k_left:
            x_change = 0
        if k_up:
            y_change = -5
        if k_down:
            y_change = 5
        if k_up and k_down:
            y_change = 0
        
        x+= x_change
        y+= y_change
        
        gameDisplay.fill(black) 
        
        # projectile(projx, projy, projw, projh, colour):
        projectile(proj_startx, proj_starty, proj_width, proj_height, white)
        proj_starty += proj_speed
        reimu(x,y)

        if x > display_width-reimu_width or x<0:
            crash()        
        if y > display_height-reimu_height or y<0:
            crash()
            
        if proj_starty > display_height:
            proj_starty = 0 - proj_height
            proj_startx = random.randrange(0,display_width)
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
