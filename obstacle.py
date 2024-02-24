import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        """
        Initializes the Obstacle class

        Inputs:
            size[int]: the size we want our Surface object to be
            color[tuple[int,int,int]]: The color of the surface
            x[int]: The x-position we want our Surface to be
            y[int]: The y-postion we want our Surface to be
        """
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))
