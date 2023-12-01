import pygame
from random import choice, randint
from player import Player
from obstacle import Obstacle
from alien import Alien, Extra
from laser import Laser
from health_powerup import HealthPower

LIVES = 3
SCORE = 0

class Level:
    def __init__(self,screen, screen_width, screen_height,alien_rows, alien_cols, alien_speed_x, alien_speed_y):
        self.screen = screen 
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        ### Player Setup ###
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player((self.screen_width//2,self.screen_height - 20)))

        ### Health & Score
        self.live_surf = pygame.image.load('graphics/player.png')
        # self.live_surf.get_size[0] is the width of the life
        # *3 because we want 3 of them
        # + 30 because that will be our offset from the left of the screen 

        self.live_x_start_pos = self.screen_width - (self.live_surf.get_size()[0] +10)
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)
        

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
        self.obstacle_x_positions = [num * (self.screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]                  
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.create_mult_obstacles(*self.obstacle_x_positions, x_start = (self.screen_width/15), y_start = 500)

        ### Alien setup ###
        self.aliens = pygame.sprite.Group()
        self.rows = alien_rows
        self.col = alien_cols
        # the amount of rows and columns we want for our alien setup
        self.alien_setup(self.rows, self.col)
        self.alien_x_speed = alien_speed_x
        self.alien_y_speed = alien_speed_y
        self.alien_pos_checker(alien_speed_x)
        self.alien_lasers = pygame.sprite.Group()

        ### Extra setup ###
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

        ### Health setup ###
        self.health = pygame.sprite.GroupSingle()
        self.health_spawn_time = randint(100,200)

        ### Sound ###
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.player_hurt_sound = pygame.mixer.Sound('audio/player_hurt_1.wav')
        self.player_hurt_sound2 = pygame.mixer.Sound('audio/player_hurt_2.wav')
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
    
    def alien_pos_checker(self,alien_speed_x):
        """
        This checks the position of the alien sprites
        and makes sure they don't move out of the screen
        """
        global LIVES

        for alien in self.aliens.sprites():
            if alien.rect.right == self.screen_width:
                self.alien_x_speed = -1 * alien_speed_x 
                self.alien_down(self.alien_y_speed)
            elif alien.rect.left == 0:
            
                self.alien_x_speed = -1 * alien_speed_x
                self.alien_down(self.alien_y_speed)

            for alien in self.aliens:
                if alien.rect.y >= self.screen_height:
                    LIVES = 0
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
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        """
        This controls how often the extra alien on top
        spawns in
        """
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['left','right']),self.screen_width))
            self.extra_spawn_time = randint(400,800)
    
    def health_timer(self):
        """
        This controls how often the health powerup spawns in
        """
        self.health_spawn_time -= 1
        if self.health_spawn_time <= 0:
            self.health.add(HealthPower(self.screen_width))
            self.health_spawn_time = randint(100,200)

    def collision_check(self):

        """
        Handles the collisions between the player, aliens,
        and the obstacles
        """
        global LIVES
        global SCORE
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
                        SCORE += alien.value
                # extra collsion
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.explosion_sound.play()
                    SCORE += 500
                # health collision
                if pygame.sprite.spritecollide(laser,self.health,True):
                    laser.kill()
                    self.explosion_sound.play()
                    LIVES += 1
        # Alien Laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                # player collision
                if pygame.sprite.spritecollide(laser,self.player,False):
                    self.player_hurt_sound.play()
                    laser.kill()
                    LIVES -= 1
 
        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    LIVES = 0

    def display_lives(self):
        """
        Displays the lives on the screen
        """
        for live in range(LIVES):
            # The second part is just the offset between lives
            # print(self.live_x_start_pos)
            # print(live *(self.live_surf.get_size()[0] + 10))
            # print(self.live_surf.get_size()[0])
            x = self.live_x_start_pos - (live * 70 )
            print(x)
            self.screen.blit(self.live_surf,(x,8))
            
    def display_score(self):
        """
        Displays the score
        """
        global SCORE
        score = self.font.render(f'Score: {SCORE}',False,'white')
        score_rect = score.get_rect(topleft = (10,-15))
        self.screen.blit(score,score_rect)

    
    def reset(self):
        self.__init__(self.screen, self.screen_width, self.screen_height, self.rows, self.col, self.alien_x_speed, self.alien_y_speed)

    def run(self):
        """
        Updates all sprite groups and draws them as well
        """
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()



        self.aliens.update(self.alien_x_speed)
        self.alien_pos_checker(self.alien_x_speed)
        self.extra_alien_timer()
        self.collision_check()

        self.player.sprite.lasers.draw(self.screen)
        self.player.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.extra.draw(self.screen)
        self.display_lives()
        self.display_score()
        if LIVES < 5:
            self.health.update()
            self.health_timer()
            self.health.draw(self.screen)
