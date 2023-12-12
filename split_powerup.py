import pygame
from random import randint

class Split(pygame.sprite.Sprite):

    def __init__(self,screen_width,screen_height):
        super().__init__()
        self.image = pygame.image.load("graphics/shield_powerup.png")
        self.random_x_pos = randint(50,screen_width - 50)
        self.rect = self.image.get_rect(topleft = (self.random_x_pos,10))
        self.screen_height = screen_height
        self.speed = 2  

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.screen_height + 50:
            self.kill()   