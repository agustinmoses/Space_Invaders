import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        """
        Initiates the player sprite class.

        Inputs:
            pos[tuple[int,int]]: the position of the player
        """
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 6
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.screen_width = 800
        self.screen_height = 600
        self.powerup = False

        self.lasers = pygame.sprite.Group()

    def input(self):
        """
        This manages all the inputs of the player
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] and (self.rect.right <= self.screen_width):
            self.rect.x += self.speed 
        elif keys[pygame.K_LEFT] and (self.rect.left >= 0):
            self.rect.x -= self.speed
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.ready:  
            self.shoot()
            self.laser_sound.play()
            self.ready = False
            self.laser_time = pygame.time.get_ticks() 

    def recharge(self):
        """
        This manages the cooldown for the laser
        """
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot(self):
        """
        Simply adds a Laser sprite to the group.
        """
        ### Potential Powerup ???? ###
        print(self.powerup)
        if self.powerup:
            self.lasers.add(Laser((self.rect.center[0] + 20 ,self.rect.center[1]),8,self.rect.bottom))
            self.lasers.add(Laser((self.rect.center[0] - 20,self.rect.center[1]) ,8,self.rect.bottom))
        self.lasers.add(Laser(self.rect.center,8, self.rect.bottom))

    def update(self):
        """
        Runs all the methods mentioned above
        """
        self.input()
        self.recharge()
        # updates the laser sprites
        # This is from the Laser class
        self.lasers.update()


    