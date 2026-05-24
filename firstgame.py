import pygame
pygame.init()

screen = pygame.display.set_mode((720,440))
pygame.display.set_caption("Myy First Gamee")

bg = pygame.image.load("bg1.jpg")

clock = pygame.time.Clock()

hitSound = pygame.mixer.Sound("eren.wav")
deathSound = pygame.mixer.Sound("boy.wav")
bgSound = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

class Player():
    walkLeft = [pygame.image.load("L1.png"),pygame.image.load("L2.png"),pygame.image.load("L3.png"),pygame.image.load("L4.png"),pygame.image.load("L5.png"),pygame.image.load("L6.png"),pygame.image.load("L7.png"),pygame.image.load("L8.png"),pygame.image.load("L9.png")]

    walkRight =[pygame.image.load("R1.png"),pygame.image.load("R2.png"),pygame.image.load("R3.png"),pygame.image.load("R4.png"),pygame.image.load("R5.png"),pygame.image.load("R6.png"),pygame.image.load("R7.png"),pygame.image.load("R8.png"),pygame.image.load("R9.png")]

    def __init__(self, x, y, length, width):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.vel = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount =10
        self.standing = True
        self.hitbox = (self.x+18, self.y + 13, 26, 49)
        
    def redraw(self, screen):
            screen.blit(bg, (0,0))  
            if self.walkCount + 1>= 27:
                self.walkCount = 0
                          
            if not self.standing:
                if self.left:
                    screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.left:
                    screen.blit(self.walkLeft[0], (self.x, self.y))  
                else:
                    screen.blit(self.walkRight[0], (self.x, self.y))
            
            self.hitbox = (self.x + 18, self.y + 13, 26, 49)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)   
            
class Object():
    def __init__(self, x, y, radius, facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.facing = facing
            self.vel = 12 * facing
            
            hmg = pygame.image.load("eren.png")
            self.hmg = pygame.transform.scale(hmg, (2*self.radius, 2* self.radius))
            
    def draw(self, screen):
        screen.blit(self.hmg, (self.x - self.radius, self.y - self.radius))        
              
class Enemies():
    walkLeft = [pygame.image.load("L1E.png"),pygame.image.load("L2E.png"),pygame.image.load("L3E.png"),pygame.image.load("L4E.png"),pygame.image.load("L5E.png"),pygame.image.load("L6E.png"),pygame.image.load("L7E.png"),pygame.image.load("L8E.png"),pygame.image.load("L9E.png"),pygame.image.load("L10E.png"),pygame.image.load("L11E.png")]              
                 
    walkRight =  [pygame.image.load("R1E.png"),pygame.image.load("R2E.png"),pygame.image.load("R3E.png"),pygame.image.load("R4E.png"),pygame.image.load("R5E.png"),pygame.image.load("R6E.png"),pygame.image.load("R7E.png"),pygame.image.load("R8E.png"),pygame.image.load("R9E.png"),pygame.image.load("R10E.png"),pygame.image.load("R11E.png")]                          

    def __init__(self, x, y, length, width, end):
       self.x = x
       self.y = y
       self.length = length
       self.width = width
       self.end = end      
       self.walkCount = 0
       self.path = [self.x, self.end]      
       self.hitbox = (self.x +22, self.y +5, 28, 55)  
       self.health = 0
        
       if self.x < self.end:
           self.vel = 5
       else:
           self.vel = -5
                                                                                  
    def move(self):       
            if self.vel > 0:
                if self.x + self.vel < max(self.path):
                    self.x += self.vel
                else:
                    self.vel = -self.vel
                    self.walkCount = 0
            else:
               if self.x + self.vel > min(self.path):
                   self.x += self.vel
               else:
                  self.vel = -self.vel
                  self.walkCount = 0                      
                          
    def draw(self, screen, score):  
        if score < 100:
            self.move()
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
                    
            if self.vel < 0:
                screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1     
            self.hitbox = (self.x + 22, self.y+5, 28, 55)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)    
    
class Game(): 
    def __init__(self):
        self.character = Player(20, 366, 64, 64)  
        self.bullets = []
        self.enemies = Enemies(616, 371, 64, 64, 50)
        self.run = True              
        self.display = True
        self.score = 0
        self.font = pygame.font.SysFont("comicsans", 38, True)   
        self.sound = False
        self.frame = 0
        
    def hit(self):
        self.frame = 15
            
    def font_(self, screen):
        text = self.font.render("Score: " + str(self.score), 1,  (100, 0, 0)) 
        screen.blit(text, (595, 27))
        
        if self.frame> 0:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("-10", 1, (255,0,0))
            screen.blit(text, (self.enemies.hitbox[0]-10, self.enemies.hitbox[1]- 60))
            
        if self.score == 100:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render("KAZANDIN", 1, (0,0,0))
            screen.blit(text, (200, 200))       
    def jumpScare(self, screen):
        image = pygame.image.load("jumpscare.jpg")
        image1 = pygame.transform.scale(image, (737, 490))
        
        if self.score < 100 and self.character.y + self.character.length > self.enemies.hitbox[1] and self.character.y < self.enemies.hitbox[1] + self.enemies.hitbox[3]: 
            if self.character.x + self.character.width > self.enemies.x + 40 and self.character.x < self.enemies.hitbox[0] + self.enemies.hitbox[2]-30:
                screen.blit(image1, (0,0))           
                self.display = False 
                if not self.sound:
                    deathSound.play()
                    self.sound = True
                
    def jump(self):
        if self.character.jumpCount >= -10:
            neg = 1
            if self.character.jumpCount < 0:
                    neg = -1
            self.character.y -= (self.character.jumpCount ** 2) * 0.3 * neg
            self.character.jumpCount -= 1
        else:
            self.character.jumpCount = 10
            self.character.isJump = False
                               
    def redraw(self, screen):                 
              self.jumpScare(screen)
              if self.display:
                  self.character.redraw(screen)
                  self.enemies.draw(screen, self.score)
                  for bullet in self.bullets:
                      bullet.draw(screen)            
                  self.bars(screen)  
                  self.font_(screen)                 
                  pygame.display.update()                               
              else:
                  pygame.display.update()
              
    def process(self):
        for bullet in self.bullets[ : ]:
            if bullet.x < 720 and bullet.x > 0:                                
               bullet.x += bullet.vel
               if self.score < 100 and bullet.x - bullet.radius < self.enemies.hitbox[0] + self.enemies.hitbox[2] and bullet.x + bullet.radius > self.enemies.hitbox[0]:
                   hitSound.play()
                   self.hit()
                   self.enemies.health += 4
                   if self.score < 100:
                       self.score += 10
                   self.bullets.remove(bullet)
            else:
                self.bullets.remove(bullet)  
                                             
    def bars(self, screen):
        if self.score < 100:
            pygame.draw.rect(screen, (255,0,0), (self.enemies.hitbox[0], self.enemies.hitbox[1]-9, 40, 6))           
            pygame.draw.rect(screen, (0,255,0), (self.enemies.hitbox[0], self.enemies.hitbox[1]-9, 40-self.enemies.health, 6))
                 
    def Loop(self):
        while self.run:
            clock.tick(33)
            
            if self.frame > 0:
                self.frame-=1
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False            
                                               
                if event.type == pygame.KEYDOWN:
                    if not self.character.isJump and event.key == pygame.K_DOWN:                 
                         if self.character.left == True:
                             facing = -1
                         else:
                             facing = 1    
                         if len(self.bullets)<5:
                             self.bullets.append(Object(round((self.character.x + self.character.width//2)), round((self.character.y + self.character.length//2)), 15, facing))  
                      
            
            keys = pygame.key.get_pressed()                                                                                  
            if keys[pygame.K_LEFT] and self.character.x > self.character.vel:
                self.character.x -= self.character.vel
                if self.character.left == False:
                    self.character.walkCount = 0
                self.character.left = True
                self.character.right = False
                self.character.standing = False    
            elif keys[pygame.K_RIGHT] and self.character.x < 720 - self.character.width - self.character.vel:
                self.character.x += self.character.vel
                if self.character.right == False:
                    self.character.walkCount = 0
                self.character.left = False
                self.character.right = True
                self.character.standing = False            
            else:
                self.character.walkCount = 0
                self.character.standing = True
                
            if self.character.isJump == False:
                if keys[pygame.K_UP] and self.character.y > self.character.vel:
                      self.character.isJump = True
                      self.character.walkCount = 0
            else:
                self.jump()          
            
            self.process()
            self.redraw(screen)     
                      
        pygame.quit() 
        
game = Game()
game.Loop()
