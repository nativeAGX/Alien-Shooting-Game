import random
import pygame
import math
from pygame import mixer
pygame.init()
#Screen
screen=pygame.display.set_mode((900, 600))
#Background
background=pygame.image.load('Background 2.png')
#Background Music
mixer.music.load('Backround Music.mp3')
mixer.music.play(-1)
#Game Icon and Logo
pygame.display.set_caption("Galactic Wars")
logo=pygame.image.load('Icon 2.png')
pygame.display.set_icon(logo)
#Spaceship aka Player
spaceshipImg=pygame.image.load('spaceship.png')
spaceshipX=480
spaceshipY=450
spaceshipX_change=0
spaceshipY_change=0
#Enemy
enemyImg= []
enemyX= []
enemyY= []
enemyX_change= []
enemyY_change= []
numOfEnemies=5
#Multiple Enemies
for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0,836))
    enemyY.append(random.randint(0,250))
    enemyX_change.append(2)
    enemyY_change.append(40)
#Bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=418
bulletX_change=0
bulletY_change=4
bulletState="Ready"
#Drawing Spaceship on Screen
def player(x,y):
    screen.blit(spaceshipImg,(x,y))
#Drawing Mutiple Enemies on Screen
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
#Firing Bullet
def fire_bullet(x,y):
    global bulletState
    bulletState="Fire"
    screen.blit(bulletImg,(x,y))
#Checking for Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance <= 25:
        return True
    else:
        return False
#Score   
score_value=0
font=pygame.font.Font('Font1.ttf', 50)
textX=10
textY=10
def showScore(x,y):
    score=font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))
#Game Over
gameover_font=pygame.font.Font('Font1.ttf', 80)
def Game_Over():
    gameover_text=gameover_font.render("GAME OVER !!!", True, (255,255,255))
    screen.blit(gameover_text, (150,250))
    gameover_sound=mixer.Sound('Game Over.mp3')
    gameover_sound.play()
#Game Loop
running=True
while running:
    screen.fill((0,255,255))
    screen.blit(background,(0,0))  
    for event in pygame.event.get(): #Closing the Game
        if event.type == pygame.QUIT:
            running=False
        
        if event.type==pygame.KEYDOWN: #Checking for Keystrokes
            if event.key==pygame.K_LEFT: #Spaceship Movement
                spaceshipX_change = -2
            elif event.key==pygame.K_RIGHT:
                spaceshipX_change = 2
            elif event.key==pygame.K_SPACE: #Firing Bullet on Space Bar press
                if bulletState is "Ready":
                    bulletSound=mixer.Sound('Laser 2.mp3') #Laser Firing Sound
                    bulletSound.play()
                    bulletX=spaceshipX
                    fire_bullet(bulletX,bulletY)          
        
        elif event.type==pygame.KEYUP: #Release of KeyStroke
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                spaceshipX_change = 0   
    
    spaceshipX += spaceshipX_change 
    if spaceshipX <= 0: 
        spaceshipX=0
    elif spaceshipX >= 836:
        spaceshipX=836 
    
    for i in range(numOfEnemies):
        if enemyY[i] >= 420: #Condition and Loop for game to be Over
            for j in range(numOfEnemies):
                enemyY[j]=1000
            Game_Over()
            break

        enemyX[i] += enemyX_change[i] #Enemy at Boundary
        if enemyX[i] <= 0:
            enemyX_change[i]=2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i]=-2
            enemyY[i] += enemyY_change[i]
        
        collision= isCollision(enemyX[i], enemyY[i], bulletX, bulletY) #Collision Detection
        if collision:
            explosionSound=mixer.Sound('Explosion 2.mp3') #Collision Sound
            explosionSound.play()
            bulletY=418
            bulletState="Ready"
            score_value +=1
            enemyX[i]=random.randint(0,836) #Enemy Respawn
            enemyY[i]=random.randint(0,250)
        enemy(enemyX[i],enemyY[i],i)  
                                    
                                     

    
    if bulletY <= 0: #Bullet State
        bulletY=418
        bulletState="Ready"
    
    if bulletState is "Fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    player(spaceshipX,spaceshipY) #Calling player Function
    showScore(textX,textY) #Calling showScore Function    
    pygame.display.update() #Screen Update    