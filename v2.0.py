# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:44:15 2019

@author: SPORYKHIN
"""

import pygame
import random
pygame.init()

display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
numbers = '0123456789'

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Touhou 2.71: The Rising of Tutu')

reimuImg=pygame.image.load('Reimu_small.png')
bg=pygame.image.load('background.png')
bfairyImg=pygame.image.load('bfairy.png')
gfairyImg=pygame.image.load('gfairy.png')
rfairyImg=pygame.image.load('rfairy.png')
sansImg=pygame.image.load('sans.png')
(reimu_width,reimu_height) = reimuImg.get_rect().size
(bfairy_width,bfairy_height) = bfairyImg.get_rect().size
(gfairy_width,gfairy_height) = gfairyImg.get_rect().size
(rfairy_width,rfairy_height) = rfairyImg.get_rect().size
(sans_width, sans_height) = sansImg.get_rect().size


clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
bulletSound.set_volume(0.3)
hitSound.set_volume(0.3)

pygame.mixer.music.load('stagemusic.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

class reimu(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x+10, self.y+10, self.width-20, self.height-20)
        
    
    def draw(self,gameDisplay):
        gameDisplay.blit(reimuImg,(self.x,self.y))
        self.hitbox = (self.x+10, self.y+10, self.width-20, self.height-20)
        pygame.draw.rect(gameDisplay, red, self.hitbox, 2)
        
    def hit(self):
        self.x = display_width * 0.5
        self.y = display_height * 0.8
        font1 = pygame.font.SysFont('arial', 100)
        text = font1.render('You died!', 1, white)
        gameDisplay.blit(text, (display_width * 0.5 - text.get_width() * 0.5, display_height * 0.5 - text.get_height() * 0.5))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        
class projectile(object):
    def __init__(self,x,y,radius,colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel = 20
        
    def draw(self,gameDisplay):
        pygame.draw.circle(gameDisplay, self.colour, (self.x,self.y), self.radius)
    
class enemyprojectile(object):
    def __init__(self,x,y,radius,colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel = 2
        
    def draw(self,gameDisplay):
        pygame.draw.circle(gameDisplay, self.colour, (self.x,self.y), self.radius)
        
class sans(object):
    def __init__(self, x, y, width, height, endx, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.endx = endx
        self.pathx = [self.x, self.endx]
        self.velx = 2
        self.sprite = sprite
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 4999
        self.visible = False
        
    def draw(self, gameDisplay):
        self.movesans()
        self.hitbox = (self.x, self.y, self.width, self.height)
        if enemies[0].visible or enemies[1].visible or enemies[2].visible:
            self.visible = False
        else:
            if self.health > 0:
                self.visible = True
        if self.visible:
            pygame.draw.rect(gameDisplay, red, (self.hitbox[0], self.hitbox[1] + self.height + 20 , self.width, 10))
            pygame.draw.rect(gameDisplay, green, (self.hitbox[0], self.hitbox[1] + self.height + 20 , self.width * (self.health/4999), 10))
            gameDisplay.blit(self.sprite,(self.x,self.y))
    
    def movesans(self):
        if self.velx > 0:
            if self.x + self.velx < self.pathx[1]:
                self.x += self.velx
            else:
                self.velx = self.velx * -1
        else:
            if self.x - self.velx > self.pathx[0]:
                self.x += self.velx
            else:
                self.velx = self.velx * -1
                
    def hit(self):
        if self.health > 0:
            self.health -= 1
            print(self.health)
        else:
            self.visible = False
            font1 = pygame.font.SysFont('arial', 100)
            font1 = pygame.font.SysFont('arial', 50)
            text = font1.render('You win!', 1, white)
            finalscore = font1.render('Final score: '+str(highscore+graze), 1, white)
            file = open('playerdata.txt','w')
            file.write('Highscore: '+str(score+graze+1))
            file.close()
            gameDisplay.fill(black)
            gameDisplay.blit(text, (display_width * 0.5 - text.get_width() * 0.5, display_height * 0.5 - text.get_height() * 0.5))
            gameDisplay.blit(finalscore, (display_width * 0.5 - text.get_width() * 0.5, display_height * 0.2 - text.get_height() * 0.5))
            pygame.display.update()
            pygame.mixer.music.fadeout(3000)
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()

class enemy(object):
    def __init__(self, x, y, width, height, endx, endy, spriteNum):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.endx = endx
        self.endy = endy
        self.pathx = [self.x, self.endx]
        self.pathy = [self.y, self.endy]
        self.velx = 2
        self.vely = 3
        self.sprite = [bfairyImg, gfairyImg, rfairyImg, sansImg]
        self.spriteNum = spriteNum
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 499
        self.visible = True
         
    def draw(self, gameDisplay):
        if self.spriteNum == 0:
            self.moveleft()
            self.hitbox = (self.x, self.y, self.width, self.height)
            if self.visible:
                pygame.draw.rect(gameDisplay, red, (self.hitbox[0], self.hitbox[1] - 20 , self.width, 10))
                pygame.draw.rect(gameDisplay, green, (self.hitbox[0], self.hitbox[1] - 20 , self.width * (self.health/499), 10))
                gameDisplay.blit(self.sprite[self.spriteNum],(self.x,self.y))
        if self.spriteNum == 1:
            self.movecenter()
            self.hitbox = (self.x, self.y, self.width, self.height)
            if self.visible:
                pygame.draw.rect(gameDisplay, red, (self.hitbox[0], self.hitbox[1] - 20 , self.width, 10))
                pygame.draw.rect(gameDisplay, green, (self.hitbox[0], self.hitbox[1] - 20 , self.width * (self.health/499), 10))
                gameDisplay.blit(self.sprite[self.spriteNum],(self.x,self.y))
        if self.spriteNum == 2:
            self.moveright()
            self.hitbox = (self.x, self.y, self.width, self.height)
            if self.visible:
                pygame.draw.rect(gameDisplay, red, (self.hitbox[0], self.hitbox[1] - 20 , self.width, 10))
                pygame.draw.rect(gameDisplay, green, (self.hitbox[0], self.hitbox[1] - 20 , self.width * (self.health/499), 10))
                gameDisplay.blit(self.sprite[self.spriteNum],(self.x,self.y))

    def moveleft(self):
        if self.velx > 0:
            if self.x - self.velx > self.pathx[1]:
                self.x -= self.velx
            else:
                self.velx = 0
        if self.vely > 0:
            if self.y + self.vely < self.pathy[1]:
                self.y += self.vely
            else:
                self.vely = 0
    
    def movecenter(self):
        if self.velx > 0:
            if self.x - self.velx > self.pathx[1]:
                self.x -= self.velx
            else:
                self.velx = 0
        if self.vely > 0:
            if self.y + self.vely < self.pathy[1]:
                self.y += self.vely
            else:
                self.vely = 0
    
    def moveright(self):
        if self.velx > 0:
            if self.x + self.velx < self.pathx[1]:
                self.x += self.velx
            else:
                self.velx = 0
        if self.vely > 0:
            if self.y + self.vely < self.pathy[1]:
                self.y += self.vely
            else:
                self.vely = 0
                
    def hit(self):
        if self.health > 0:
            self.health -= 1
            print(self.health)
        else:
            self.visible = False
        print('hit')

def redrawGameWindow():
    gameDisplay.blit(bg,(0,0))
    text = font.render('Score: '+ str(score), 1, white)
    hightext = font.render('High Score: '+ str(highscore), 1, white)
    grazetext = font.render('Graze: '+ str(graze), 1, white)
    reimu.draw(gameDisplay)
    sans.draw(gameDisplay)
    for fairy in enemies:
        fairy.draw(gameDisplay)
    for bullet in bullets:
        bullet.draw(gameDisplay)
    for cbullet in center_bullets:
        cbullet.draw(gameDisplay)
    for lbullet in left_bullets:
        lbullet.draw(gameDisplay)
    for rbullet in right_bullets:
        rbullet.draw(gameDisplay)
    gameDisplay.blit(hightext, (display_width * 0.65, display_height * 0.00001))
    gameDisplay.blit(text, (display_width * 0.7, display_height * 0.05))
    gameDisplay.blit(grazetext, (display_width * 0.7, display_height * 0.1))
    pygame.display.update()

#mainloop
file = open("playerdata.txt",'r')
c = file.read()
highscoretext = ''
for k in c:
    if k in numbers:
        highscoretext += k
highscore = int(highscoretext)
file.close()
font = pygame.font.SysFont('arial', 30, True)
reimu = reimu(display_width * 0.5, display_height * 0.8, reimu_width, reimu_height)
enemies = [enemy(display_width * 0.5, display_height * -0.2, bfairy_width, bfairy_height, display_width * 0.2, display_height * 0.2, 0), enemy(display_width * 0.5, display_height * -0.2, gfairy_width, gfairy_height, display_width * 0.5, display_height * 0.2, 1), enemy(display_width * 0.5, display_height * -0.2, rfairy_width, rfairy_height, display_width * 0.8, display_height * 0.2, 2)]
sans = sans(display_width * 0.1, display_height * 0.00001, sans_width, sans_height, display_width * 0.9 - sans_width, sansImg)
bullets = []
right_bullets = []
center_bullets = []
left_bullets = []
score = 0
graze = 0
m=0
run = True

while run:
    clock.tick(60)
    r=random.randint(1,3)
    rd=random.randint(1,3)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for fairy in enemies:
        if fairy.visible:
            if reimu.hitbox[1] < fairy.hitbox[1] + fairy.hitbox[3] and reimu.hitbox[1] + reimu.hitbox[3] > fairy.hitbox[1]:
                if reimu.hitbox[0] + reimu.hitbox[2] > fairy.hitbox[0] and reimu.hitbox[0] < fairy.hitbox[0] + fairy.hitbox[2]: 
                    reimu.hit()
                    center_bullets.clear()
                    left_bullets.clear()
                    right_bullets.clear()
                    score -= 100
                    if score > highscore:
                        highscore = score
            if reimu.y < fairy.y + fairy.height and reimu.y + reimu.height > fairy.y:
                if reimu.x + reimu.width > fairy.x and reimu.x < fairy.x + fairy.width:
                    graze += 1
    
    if sans.visible:
        if reimu.hitbox[1] < sans.hitbox[1] + sans.hitbox[3] and reimu.hitbox[1] + reimu.hitbox[3] > sans.hitbox[1]:
            if reimu.hitbox[0] + reimu.hitbox[2] > sans.hitbox[0] and reimu.hitbox[0] < sans.hitbox[0] + sans.hitbox[2]: 
                reimu.hit()
                center_bullets.clear()
                left_bullets.clear()
                right_bullets.clear()
                score -= 100
                if score > highscore:
                        highscore = score
        if reimu.y < sans.y + sans.height and reimu.y + reimu.height > sans.y:
                if reimu.x + reimu.width > sans.x and reimu.x < sans.x + sans.width:
                    graze += 1
        if r == 1:
            if len(center_bullets) < 200:
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))   
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
    
        if r == 2:
            if len(center_bullets) < 200:
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))   
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
    
        if r == 3:
            if len(center_bullets) < 200:
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))   
                center_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                left_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
                right_bullets.append(enemyprojectile(round(sans.x + sans.width//2), round(sans.y + sans.height//2), 6, (0,182,0)))
            
    for bullet in bullets:
        for fairy in enemies:
            if fairy.visible:
                if bullet.y - bullet.radius < fairy.hitbox[1] + fairy.hitbox[3] and bullet.y + bullet.radius > fairy.hitbox[1]:
                    if bullet.x + bullet.radius > fairy.hitbox[0] and bullet.x - bullet.radius < fairy.hitbox[0] + fairy.hitbox[2]: 
                        pygame.mixer.Channel(1).play(hitSound)
                        fairy.hit()
                        score += 1
                        if score > highscore:
                            highscore = score
                        bullets.pop(bullets.index(bullet))
        if sans.visible:
            if bullet.y - bullet.radius < sans.hitbox[1] + sans.hitbox[3] and bullet.y + bullet.radius > sans.hitbox[1]:
                if bullet.x + bullet.radius > sans.hitbox[0] and bullet.x - bullet.radius < sans.hitbox[0] + sans.hitbox[2]: 
                    pygame.mixer.Channel(1).play(hitSound)
                    sans.hit()
                    score += 1
                    if score > highscore:
                            highscore = score
                    bullets.pop(bullets.index(bullet))
                
        if bullet.y < display_height and bullet.y > -10:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        
    for cbullet in center_bullets:
        q = random.randint(-2,2)
        if len(center_bullets) > 0:
            if cbullet.y - cbullet.radius < reimu.hitbox[1] + reimu.hitbox[3] and cbullet.y + cbullet.radius > reimu.hitbox[1]:
                if cbullet.x + cbullet.radius > reimu.hitbox[0] and cbullet.x - cbullet.radius < reimu.hitbox[0] + reimu.hitbox[2]: 
                    pygame.mixer.Channel(1).play(hitSound)
                    reimu.hit()
                    score -= 100
                    if score > highscore:
                        highscore = score
                    center_bullets.pop(center_bullets.index(cbullet))
                    center_bullets.clear()
                    left_bullets.clear()
                    right_bullets.clear()
            if cbullet.y - cbullet.radius < reimu.y + reimu.height and cbullet.y + cbullet.radius > reimu.y:
                if cbullet.x + cbullet.radius > reimu.x and cbullet.x - cbullet.radius < reimu.x + reimu.width:
                    graze += 1
            if cbullet.y < display_height and cbullet.y > -10:
                if sans.visible:
                    cbullet.y += 3
                    cbullet.x += 2 * q
                else:    
                    cbullet.y += cbullet.vel
                    cbullet.x += 1 * q
            else:
                if len(center_bullets) > 0:
                    center_bullets.pop(center_bullets.index(cbullet))
    
    for lbullet in left_bullets:
        if len(left_bullets) > 0:
            if lbullet.y - lbullet.radius < reimu.hitbox[1] + reimu.hitbox[3] and lbullet.y + lbullet.radius > reimu.hitbox[1]:
                if lbullet.x + lbullet.radius > reimu.hitbox[0] and lbullet.x - lbullet.radius < reimu.hitbox[0] + reimu.hitbox[2]: 
                    pygame.mixer.Channel(1).play(hitSound)
                    reimu.hit()
                    score -= 100
                    if score > highscore:
                        highscore = score
                    left_bullets.pop(left_bullets.index(lbullet))
                    center_bullets.clear()
                    left_bullets.clear()
                    right_bullets.clear()
            if lbullet.y - lbullet.radius < reimu.y + reimu.height and lbullet.y + lbullet.radius > reimu.y:
                if lbullet.x + lbullet.radius > reimu.x and lbullet.x - lbullet.radius < reimu.x + reimu.width:
                    graze += 1
            if lbullet.y < display_height and lbullet.y > -10 and lbullet.x < display_width and lbullet.x > -10:
                if sans.visible:
                    lbullet.y += 3
                    lbullet.x -= lbullet.vel * random.randint(0,3)
                else:
                    lbullet.x -= lbullet.vel * random.randint(0,3)
                    lbullet.y += lbullet.vel
            else:
                if len(left_bullets) > 0:
                    left_bullets.pop(left_bullets.index(lbullet))
    
    for rbullet in right_bullets:
        if len(right_bullets) > 0:
            if rbullet.y - rbullet.radius < reimu.hitbox[1] + reimu.hitbox[3] and rbullet.y + rbullet.radius > reimu.hitbox[1]:
                if rbullet.x + rbullet.radius > reimu.hitbox[0] and rbullet.x - rbullet.radius < reimu.hitbox[0] + reimu.hitbox[2]: 
                    pygame.mixer.Channel(1).play(hitSound)
                    reimu.hit()
                    score -= 100
                    if score > highscore:
                        highscore = score
                    right_bullets.pop(right_bullets.index(rbullet))
                    center_bullets.clear()
                    left_bullets.clear()
                    right_bullets.clear()
        if rbullet.y - rbullet.radius < reimu.y + reimu.height and rbullet.y + rbullet.radius > reimu.y:
                if rbullet.x + rbullet.radius > reimu.x and rbullet.x - rbullet.radius < reimu.x + reimu.width:
                    graze += 1
        if rbullet.y < display_height and rbullet.y > -10 and rbullet.x < display_width and rbullet.x > -10:
            if sans.visible:
                rbullet.y += 3
                rbullet.x += rbullet.vel * random.randint(0,3)
            else:
                rbullet.x += rbullet.vel * random.randint(0,3)
                rbullet.y += rbullet.vel
        else:
            right_bullets.pop(right_bullets.index(rbullet))
        
    if r == 1:
        if enemies[0].visible:        
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
        if enemies[1].visible:
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
        if enemies[2].visible:    
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
    if r == 2:
        if enemies[2].visible:
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
        if enemies[0].visible:
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
        if enemies[1].visible:
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
    if r == 3:
        if enemies[1].visible:
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[1].x + enemies[1].width//2), round(enemies[1].y + enemies[1].height//2), 6, (0,182,0)))
        if enemies[2].visible:
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[2].x + enemies[2].width//2), round(enemies[2].y + enemies[2].height//2), 6, (0,182,0)))
        if enemies[0].visible:
            if len(center_bullets) < 50:
                center_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
            if len(left_bullets) < 75:
                left_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
            if len(right_bullets) < 75:
                right_bullets.append(enemyprojectile(round(enemies[0].x + enemies[0].width//2), round(enemies[0].y + enemies[0].height//2), 6, (0,182,0)))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_z]:
        pygame.mixer.Channel(0).play(bulletSound)
        if len(bullets) < 30:
            bullets.append(projectile(round(reimu.x + reimu.width//2), round(reimu.y + reimu.height//2), 6, white))
        
    if keys[pygame.K_LEFT] and reimu.x > reimu.vel:
        reimu.x -= reimu.vel
    if keys[pygame.K_RIGHT] and reimu.x < display_width-reimu.width-reimu.vel:
        reimu.x += reimu.vel
    if keys[pygame.K_UP] and reimu.y > reimu.vel:
        reimu.y -= reimu.vel    
    if keys[pygame.K_DOWN] and reimu.y < display_height-reimu.height-reimu.vel:
        reimu.y += reimu.vel
    
    if m < 1:
        if sans.visible:
            m += 1
            pygame.mixer.music.fadeout(3000)
            font1 = pygame.font.SysFont('arial', 90)
            text = font1.render('Boss Battle: Sans!', 1, white)
            gameDisplay.fill(black)
            gameDisplay.blit(text, (display_width * 0.5 - text.get_width() * 0.5, display_height * 0.5 - text.get_height() * 0.5))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
            pygame.mixer.music.load('bossmusic.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
    
    redrawGameWindow()

pygame.quit()
