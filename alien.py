import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        """
        Initializes the Alien class

        Input:
            color[str]: A string representing what color we want the
            alien to be
            x[int]: the x-postition we want to place our rectangle object
            y[int]: the y-position we want to place our rectangle object

        """
        super().__init__()
        file_path = 'graphics/'+ color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        if color == 'red':
            self.value = 100
        elif color == 'green':
            self.value = 200
        else:
            self.value = 300
        
    
    def update(self,direction):
        """
        Updates the alien by just shifting its x-position
        Input:
            direction[int]: By how much you want to change the alien's
            position. The bigger the integer, the faster it moves left or right.
        """
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    
    def __init__(self,side, screen_width =50):
        """
        Initializes the Extra class

        Input:
            side[str]: A string representing what side we want our extra alien
            to spawn in. Should be random
            screen_width[int]: simply just used as a way to offset our x-position
            so that it enters from right and not just spawns on the right.
            The default argument is used for testing.
        """
        super().__init__()
        self.image = pygame.image.load('graphics/extra.png')
        if side == 'right':
            self.x = screen_width + 50 
            self.speed = -3
        elif side == 'left':
            self.x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (self.x,10))

    def update(self):
        """
        Updates the extra alien x-postion
        """
        self.rect.x += self.speed