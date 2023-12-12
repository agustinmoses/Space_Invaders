import pygame
from random import  randint


class HealthPower(pygame.sprite.Sprite):

    def __init__(self, screen_width):
        super().__init__()
        
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.random_x_pos = randint(50,screen_width - 50)
    
        self.rect = self.image.get_rect(topleft = (self.random_x_pos,10))
        self.speed = 2

    def update(self):
        
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.kill()