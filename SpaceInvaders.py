import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("space invaders!")
clock = pygame.time.Clock()
gameover = False

my_font = pygame.font.SysFont('New Times Roman MS', 30)
text_surface = my_font.render('LIVES:', False, (255, 0, 0))

AlienDeath = pygame.mixer.Sound('LegoYodaDeath.mp3')
TankFire = pygame.mixer.Sound('VineBoom.mp3')

lives = 3
xpos = 400
ypos = 750
moveleft = False
moveright = False
shoot = False

timer = 0;

class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def move(self, time):
        if time % 800 == 0:
            self.ypos += 100
            self.direction *=-1
            return 0
    
        if time % 100 == 0:
            self.xpos+=50*self.direction
        
        return time
    def collide(self, Bulletx, Bullety):
        if self.isAlive:
            if Bulletx > self.xpos:
                if Bulletx < self.xpos + 40:
                    if Bullety < self.ypos + 40:
                        if Bullety > self.ypos:
                            pygame.mixer.Sound.play(AlienDeath)
                            self.isAlive = False
                            return False
                        
        return True
    def draw(self):
        if self.isAlive == True:
            
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
        
class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
        
    def move(self, xpos, ypos):
        if self.isAlive == True:
            self.ypos-=5
        if self.ypos < 0:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
            
    
            
    def draw(self):
        
        pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
        
bullet = Bullet(xpos+28, ypos)

class wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    def collide(self, Bulletx, Bullety):
        if self.numHits < 3:
            if Bulletx > self.xpos:
                if Bulletx < self.xpos + 40:
                    if Bullety < self.ypos + 40:
                        if Bullety > self.ypos:
                            print("hit")
                            self.numHits += 1
                            return False
                        
        return True
    def draw(self):
        if self.numHits == 0:
            pygame.draw.rect(screen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 1:
            pygame.draw.rect(screen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
class missile:
    def __init__(self):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
    def move(self):
        if self.isAlive == True:
            self.ypos+=5
        if self.ypos > 800:
            self.isAlive = False
            self.xpos = -10
            self.ypos = -10
        
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
    

armada = []
for i in range (4):
    for j in range (9):
        armada.append(Alien(j*80+50, i*70+50))
        
walls = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            walls.append(wall(j*30+200*k+50, i*30+600))

missiles = []
for i in range (10):
    missiles.append(missile())



while not gameover: #GameLoop#####################################################################
    clock.tick(60)
    timer +=1
#INPUT--------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveleft = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveleft = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moveright = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moveright = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot = True
                pygame.mixer.Sound.play(TankFire)
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shoot = False
#PHYSICS------------------------------------------------------------------------------------------
    
    if moveleft == True:
        vx =- 3
    else:
        vx = 0
            
    xpos += vx
    
    if moveright == True:
        vx =+ 3
    else:
        vx = 0
            
    xpos += vx
    
    for i in range (len(armada)):
        timer = armada[i].move(timer)
    #print(timer)
    
    if shoot == True:
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        if bullet.isAlive == True:
            for i in range (len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
                
        if bullet.isAlive == True:
            for i in range (len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
        
    else:
        bullet.xpos = xpos + 28
        bullet.ypos = ypos
        
    for i in range(len(missiles)):
        missiles[i].move()
        
        chance = random.randrange(100)
        if chance < 2:
            pick = random.randrange(len(armada))
            if armada[pick].isAlive == True:
                for i in range(len(missiles)):
                    if missiles[i].isAlive == False:
                        missiles[i].isAlive = True
                        missiles[i].xpos = armada[pick].xpos+5
                        missiles[i].ypos = armada[pick].ypos
                        break
                    
        for i in range(len(walls)):
            for j in range(len(missiles)):
                if missiles[j].isAlive == True:
                    if walls[i].collide(missiles[j].xpos, missiles[j].ypos) == False:
                        missiles[j].isAlive = False
                        break
    
        for i in range (len(missiles)):
            if missiles[i].isAlive:
                if missiles[i].xpos > xpos:
                    if missiles[i].xpos < xpos + 40:
                        if missiles[i].ypos < ypos + 40:
                            if missiles[i].ypos > ypos:
                                lives -= 1
                                time.sleep(1)
                                xpos = 400
                                ypos = 750
                                
        if lives == 0:
            gameover = True
                                
                                
#RENDER----------------------------------------------------------------------------------------
    
    screen.fill((0, 0, 0))
    
    screen.blit(text_surface, (0,0))
    
    #player
    pygame.draw.rect(screen, (150, 200, 70), (xpos, 750, 60, 20)) 
    pygame.draw.rect(screen, (150, 200, 70), (xpos + 10, 740, 40, 10)) 
    pygame.draw.rect(screen, (150, 200, 70), (xpos + 25, 720, 10, 40))
    
    #lives
    if lives == 3:
        pygame.draw.rect(screen, (150, 200, 70), (80, 10, 40, 10)) 
        pygame.draw.rect(screen, (150, 200, 70), (130, 10, 40, 10)) 
        pygame.draw.rect(screen, (150, 200, 70), (180, 10, 40, 10))
    elif lives == 2:
        pygame.draw.rect(screen, (150, 200, 70), (80, 10, 40, 10)) 
        pygame.draw.rect(screen, (150, 200, 70), (130, 10, 40, 10))
    elif lives == 1:
        pygame.draw.rect(screen, (150, 200, 70), (80, 10, 40, 10)) 
    
    
    #aliens
    for i in range (len(armada)):
        armada[i].draw()
    
    #bullet
    if bullet.isAlive == True:
        bullet.draw()       
    
    #wall
    for i in range (len(walls)):
        walls[i].draw()
        
    #missile
    for i in range (len(missiles)):
        missiles[i].draw()
    
    pygame.display.flip()
#GameLoopEnd###################################################################################

pygame.quit()
