import pygame
import sys
from random import choice, randint
from player import Player
from obstacle import Obstacle
from alien import Alien, Extra
from laser import Laser
class Game:
    def __init__(self,game_score):
        ### Player Setup ###
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player((450,600)))
        self.game_condition = False
        ### Health & Score
        self.lives = 3
        self.live_surf = pygame.image.load('graphics/player.png')
        # self.live_surf.get_size[0] is the width of the life
        # *2 because we want 2 of them
        # + 20 because that will be our offset from the left of the screen 
        self.live_x_start_pos = 900 - (self.live_surf.get_size()[0] * 3 + 20 )
        self.score = game_score
        self.font = pygame.font.Font('font/Pixeled.ttf',20)
        

        ### Obstacle Setup ###
        # This is our shape of the obstacles
        self.shape =         ['  xxxxxxx ',
                              ' xxxxxxxxx ',
                              'xxxxxxxxxxx',
                              'xxxxxxxxxxx',
                              'xxxxxxxxxxx',
                              'xxx     xxx',
                              'xx       xx' ]
        self.obstacle_amount = 4
        # This give us our even spacing between the objects
        self.obstacle_x_positions = [num * (900/self.obstacle_amount) for num in range(self.obstacle_amount)]                  
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.create_mult_obstacles(*self.obstacle_x_positions, x_start = (900/15), y_start = 500)

        ### Alien setup ###
        self.aliens = pygame.sprite.Group()
        # the amount of rows and columns we want for our alien setup
        self.alien_setup(rows = 6, cols = 14)
        self.alien_movement = 1
        self.alien_pos_checker()
        self.alien_lasers = pygame.sprite.Group()

        ### Extra setup ###
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

        ### Sound ***
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
    def create_obstacle(self,x_start, y_start, offset_x):
        """
        This creates the obstacles in the game by placing a pixelated
        block following the pattern given by self.shape
        Inputs:
            x_start[int]: this is starting x position where we start placing
            blocks
            y_start[int]: this is the starting y position where we start placing
            blocks
            offset_x[int]: this is how much spacing we have between multiple blocks
        """
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    # The 'start' is where we want to begin placing our block
                    # The index lets us know where we put that block
                    # We multiply the block_size since we want want to move the
                    # x and y pos by the zize of the block.
                    # The the off_set_x makes sure we space out our blocks nicely
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start+ row_index * self.block_size
                    block = Obstacle(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)
    
    def create_mult_obstacles(self,*offset, x_start, y_start,):
        """
        This takes care of the spacing between the obstacles
        
        Input:
            offset: this is the distance between obstacles we set
            x_start[int]: the parameter we put in create_obstacle()
            y_start[int]: the parameter we put in create_obstacle()
        """
        for offset_x in offset:
            self.create_obstacle(x_start,y_start, offset_x)

    def alien_setup(self,rows,cols, x_distance = 60, y_distance=48, x_offset = 40, y_offset = 40):
        """
        This sets up the alien's positions on the screen

        Inputs:
            rows[int]: how many rows of enemies we want
            cols[int]: how many columns of enemies we want
            x_distance[int]: The distance we start placing them on the x_pos
            y_distance[int]: The distance we start placing them on the y_pos
            x_offset[int]: The spacing between enemies in the rows
            y_offset[int]: The spacing between enemies in the columns
        """

        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien('yellow',x, y)
                elif row_index >= 1 and row_index < 3:
                    alien_sprite = Alien('green',x,y)
                else:
                    alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)
    
    def alien_pos_checker(self):
        """
        This checks the position of the alien sprites
        and makes sure they don't move out of the screen
        """

        for alien in self.aliens.sprites():
            if alien.rect.right == 900:
                self.alien_movement = -1
                self.alien_down(2)
            elif alien.rect.left == 0:
                self.alien_movement = 1
                self.alien_down(2)

            for alien in self.aliens:
                if alien.rect.y >= 625:
                    self.game_condition = False
    def alien_down(self,distance):
        """
        This shift the alien sprites down by a certain distance

        Inputs:
            distance[int]: The amount, in pixels, you want to move the
            pixels down
        """
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    
    def alien_shoot(self):
        """
        This handles the shooting mechanism of the aliens shooting
        """
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, 625)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        """
        This controls how often the extra alien on top
        spawns in
        """
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['left','right']),900))
            self.extra_spawn_time = randint(400,800)

    def collision_check(self):

        """
        Handles the collisions between the player, aliens,
        and the obstacles
        """
        # Player Laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                # alien collision
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    self.explosion_sound.play()
                    laser.kill()
                    for alien in aliens_hit:
                        if self.score == 1:
                            self.score = 0
                        self.score += alien.value
                # extra collsion
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.explosion_sound.play()
                    self.score += 500
        # Alien Laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                # player collision
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_condition = False
        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.game_condition = False

    def display_lives(self):
        """
        Displays the lives on the screen
        """
        for live in range(self.lives):
            # The second part is just the offset betwween lives
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0]+ 10))
            screen.blit(self.live_surf,(x,8))
            
    def display_score(self):
        """
        Displays the score
        """
        score = self.font.render(f'Score: {self.score}',False,'white')
        score_rect = score.get_rect(topleft = (10,-15))
        screen.blit(score,score_rect)

    def victory_message(self):
        """
        Displays a victory message if there are no more aliens.
        """
        if not self.aliens.sprites():
            victory_surf = self.font.render("You Defeated the Alien Invasion!",False, 'white')
            victory_rect = victory_surf.get_rect(center = (900/2, 625/2))
            screen.blit(victory_surf,victory_rect)

    def reset(self):
        """
        This 'resets' the game by just re-intializing the
        class.
        """
        if self.game_condition == False:
            self.__init__(1)

    def run(self):
        """
        Updates all sprite groups and draws them as well
        """
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()


        self.aliens.update(self.alien_movement)
        self.alien_pos_checker()
        self.extra_alien_timer()
        self.collision_check()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()
        self.reset()

class TV:
    def __init__(self):
        self.image = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.image, (900,625))

    def create_lines(self):
        """
        Creates the lines that mimick the old classic TVs
        """
        line_height = 3
        line_amount = int(900/line_height)
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

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900,625))
    clock = pygame.time.Clock()
    game = Game(0)
    crt = TV()
    music = pygame.mixer.Sound('audio/music.wav') 
    music.play(loops=-1)
    
    ### Intro Screen ###
    game_font = pygame.font.Font('font/pixeled.ttf',20)
    message = """ The Aliens Have Taken Over!"""
    intr_message = game_font.render(message,False,'white')
    intr_rect = intr_message.get_rect(center = (900/2,200))

    instruc_message = game_font.render('Press Any Key to Begin!', False, 'white')
    instruc_rect = instruc_message.get_rect(center = (900/2,500))

    ### Game Over ###
    game_over_font = game_font = pygame.font.Font('font/pixeled.ttf',40)
    game_over = game_font.render("Game Over!", False, 'white')
    game_over_rect = game_over.get_rect(center = (900/2,200))

    # Work in-progress #
    score_message = game_font.render(f'Your score: {game.score}',False,'white')
    score_message_rect = score_message.get_rect(center = (900/2,500))


    red_alien = pygame.image.load('graphics/red.png').convert_alpha()
    red_alien = pygame.transform.scale2x(red_alien)
    red_alien_rect = red_alien.get_rect(center = (450,312))

    ### Aliens setup ###
    ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.game_condition:
                if event.type == ALIEN_LASER:
                    game.alien_shoot()
            else:
                if event.type == pygame.KEYDOWN:
                    game.game_condition = True
        if game.game_condition:    
            screen.fill((30,30,30))
            game.run()
            crt.draw()
        else:
            screen.fill((30,30,30))
            if game.score == 0:
                crt.draw()
                screen.blit(intr_message,intr_rect)
                screen.blit(instruc_message, instruc_rect)
                screen.blit(red_alien,red_alien_rect)
            else:
                crt.draw()
                screen.blit(game_over, game_over_rect)
                screen.blit(red_alien, red_alien_rect)


        pygame.display.update()
        clock.tick(60)
