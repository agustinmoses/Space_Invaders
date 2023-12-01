import pygame
import sys
from random import choice, randint
import levels

class TV:
    def __init__(self):
        self.image = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.image, (screen_width,screen_height))

    def create_lines(self):
        """
        Creates the lines that mimick the old classic TVs
        """
        line_height = 3
        line_amount = int(screen_width/line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(909,y_pos),1)
    def draw(self):
        """
        Draws the TV filter and the lines
        """
        self.tv.set_alpha(randint(75,95))
        self.create_lines()
        screen.blit(self.tv, (0,0))

class GameManager:
    def __init__(self):
        self.game_state = 'intro'
        self.music_loop = 0
        self.game_over_loop = 0
        self.victory_loop = 0
        self.game_score_copy = 0
        self.game_over_sound = pygame.mixer.Sound('audio/game_over.mp3') 
        self.victory_sound = pygame.mixer.Sound('audio/victory_sound.mp3')
        default_music = pygame.mixer.music.load('audio/music.wav')
        
        ### Setup for blinking text in Intro Screen###
        self.blink_interval = 300  # Blink every 300 milliseconds
        self.last_blink_time = pygame.time.get_ticks()
        self.show_message = True

                
    def intro(self):
        """
        Controls the intro screen
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_state = 'level1'


        screen.fill((30,30,30))
        crt.draw()
        screen.blit(intr_message,intr_rect)
        screen.blit(red_alien,red_alien_rect)
        current_time = pygame.time.get_ticks()

        if current_time - self.last_blink_time >= self.blink_interval:
            self.show_message = not self.show_message
            self.last_blink_time = current_time
        if self.show_message:
            screen.blit(instruc_message, instruc_rect)

        pygame.display.update()

    def level1(self):
        """
        Runs and controls the events that happen in level 1
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == LEVEL1_ALIENLASER:
                level1.alien_shoot()
        if levels.LIVES == 0:
            self.game_state = 'over'

        if not level1.aliens.sprites():
            self.game_state = 'level2'
        
        screen.fill((30,30,30))
        level1.run()
        crt.draw()
        pygame.display.update()
    
    def level2(self):
        """
        Runs and controls the events that happen in level 2
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == LEVEL2_ALIENLASER:
                level2.alien_shoot()
        
        if levels.LIVES == 0:
            print(levels.LIVES)
            self.game_state = 'over'
        if not level2.aliens.sprites():
            self.game_state = 'level3'
        screen.fill((30,30,30))
        level2.run()  
        crt.draw()
        pygame.display.update()

    def level3(self):
        """
        Runs and controls the events that happen in level 3
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == LEVEL3_ALIENLASER:
                level3.alien_shoot()
        
        if levels.LIVES == 0:
            self.game_state = 'over'
        if not level3.aliens.sprites():
            self.game_state = 'victory'
        screen.fill((30,30,30))
        level3.run()  
        crt.draw()
        pygame.display.update()
    
    def play_default_music(self):
        """
        Controls the default music, specifically the amount of times it plays
        """
        if self.music_loop == 0:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            self.music_loop = 1

    def play_game_over(self):
        """
        Controls the game over sound, specifically the amount of times it plays
        
        """
        if self.game_over_loop == 0:
            self.game_over_sound.play()
            self.game_over_loop = 1
    
    def play_victory(self):
        """
        Controls the victory sound, specifically the amount of times it plays
        """
        if self.victory_loop == 0:
            self.victory_sound.play()
            self.victory_loop = 1

    def reset(self):
        self.__init__()

    def game_over(self):
        """
        Controls the game over screen
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_r):
                    levels.LIVES = 3
                    levels.SCORE = 0
                    reset_levels()
                    self.reset()

        screen.fill((30,30,30))
        crt.draw()
        screen.blit(game_over, game_over_rect)
        screen.blit(red_alien, red_alien_rect)
        screen.blit(game_over_instruc, game_over_instruc_rect)

        score_message = score_font.render(f"Your Score: {levels.SCORE}", False, 'white')
        score_message_rect = score_message.get_rect(center = (screen_width/2,450))
        screen.blit(score_message, score_message_rect)
        pygame.display.update()
   
    def victory(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        levels.LIVES = 3
                        levels.SCORE = 0
                        reset_levels()
                        self.reset()

        score_message = score_font.render(f"Your Score: {levels.SCORE}", False, 'white')
        score_message_rect = score_message.get_rect(center = (screen_width/2,300))
        screen.fill((30,30,30))
        crt.draw()
        screen.blit(victory,victory_rect)
        screen.blit(victory_message, victory_message_rect)
        pygame.display.update()
    def state_manager(self):


        if self.game_state == 'intro':
            self.intro()
        elif self.game_state == 'level1':
            self.level1()
        elif self.game_state == 'level2':
            self.level2()
        elif self.game_state == 'level3':
            self.level3()
        elif self.game_state == 'over':
            self.game_over()    
        elif self.game_state == 'victory':
            self.victory()

        if (self.game_state == 'intro') or (self.game_state == 'level1') or (self.game_state == 'level2'):
            pass
            # self.play_default_music()
        if (self.game_state == 'over'):
            pygame.mixer.music.stop()
            self.play_game_over()
        if (self.game_state == 'victory'): 
            pygame.mixer.music.stop()  
            self.play_victory()

def reset_levels():
    """
    Function that resets the levels to their original state
    """
    level1.reset()
    level2.reset()
    level3.reset()

if __name__ == '__main__':
    ### General Setup ###
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
 
    crt = TV()
    game_state = GameManager()
    pygame.mixer.init()

    ### Level Setup ###
    level1 = levels.Level(screen, screen_width, screen_height,1,1,1,2)
    level2 = levels.Level(screen, screen_width, screen_height,1,1,2,2) 
    level3 = levels.Level(screen, screen_width, screen_height,6,12,2,2)

    ### Blinking Text Setup ###

    blink_interval = 500  # Blink every 500 milliseconds
    last_blink_time = pygame.time.get_ticks()

    ### Alien Laser Setup ###

    LEVEL1_ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(LEVEL1_ALIENLASER,800)

    LEVEL2_ALIENLASER = pygame.USEREVENT + 2
    pygame.time.set_timer(LEVEL2_ALIENLASER,500)

    LEVEL3_ALIENLASER = pygame.USEREVENT + 3
    pygame.time.set_timer(LEVEL3_ALIENLASER,300)
    


    ### Intro Screen Setup ###
    game_font = pygame.font.Font('font/pixeled.ttf',20)
    message = """ The Aliens Have Taken Over!"""
    intr_message = game_font.render(message,False,'white')
    intr_rect = intr_message.get_rect(center = (screen_width/2,185))

    instruc_message = game_font.render("Press the 'p' key to Begin!", False, 'white')
    instruc_rect = instruc_message.get_rect(center = (screen_width/2,500))

    red_alien = pygame.image.load('graphics/red.png').convert_alpha()
    red_alien = pygame.transform.scale2x(red_alien,)
    red_alien_rect = red_alien.get_rect(center = (screen_width//2,312))

    ### Game Over Screen Setup ###
    game_over_font = pygame.font.Font('font/pixeled.ttf', 40)
    score_font = pygame.font.Font('font/pixeled.ttf', 20)



    game_over = game_over_font.render("Game Over!", False, 'white')
    game_over_rect = game_over.get_rect(center = (screen_width/2,200))

    game_over_instruc = game_font.render("Press the 'R' Key to Try Again!", False, 'white')
    game_over_instruc_rect = game_over_instruc.get_rect(center = (screen_width/2,500))


    ### Victory Screen Setup ###
    victory_font = pygame.font.Font('font/pixeled.ttf', 20)
    
    victory = victory_font.render("You Defeated the Alien Invasion!", False, 'white')
    victory_rect = victory.get_rect(center = (screen_width/2,200))

    victory_message = game_font.render("Press the 'R' Key to Play Again!", False, 'white')
    victory_message_rect = victory_message.get_rect(center = (screen_width/2,500))

    
    while True:
    
        game_state.state_manager()
        
        
        clock.tick(60)
