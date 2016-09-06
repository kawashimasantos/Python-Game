# This class works to make and control a new character - player and zombie


import pygame
from tiles import Tile
from random import randint
from welcome_over import *

# class to control the a Character
# as a tile, it's a rectangle as well, with same size of the "bricks"
# so then we can inheritate any carachter from this class, that already control 
# the size and position of the caracther
class Character(pygame.Rect):

    width  = 32  # set the same size of the bricks
    height = 32

    def __init__(self, x, y):

        # variables to control the next target(tile) of each character
        self.tx, self.ty = None, None # target x position, and target y position
        # is the same line above, but now I save the number os the next tile was well
        self.targetTileNumber = None

    	# create the rectangle to hold the main character
        pygame.Rect.__init__(self, x, y, Character.width, Character.height)
    

   #using __ before name(__str), it makes the method private, it works for variable as well
    def __str__(self):
        return str(self.get_number())

    # it's not static because it needs to have a zombie/Characther(object) to have a target
    # and the target is actually the next tile in the better path to get the player, or for the play, the tile you want to move
    # I use this method to move our Character smothy, not with lag
    def set_target(self, next_tile):
        if self.tx == None and self.ty == None:
            self.tx = next_tile.x
            self.ty = next_tile.y # we restart them to none after the character move


    # rotate the character(player and zombi) image for what direction we're moving
    def rotate(self, direction, original_img):

        if direction == 's':
            if self.direction != 's': # direction is where the next target of the zombie is, but then if you go all north, 
            # it's gonna reasignment/load the picture all the time, every loop. So then, whe put if self.direction !='n'
            # it's mean if we are going all north, we are gonna laod and rotate just once, in the first loop. It saves memory 
                self.direction = 's'
                # furst rotate 90, and make it south
                south = pygame.transform.rotate(original_img, 90) # CCW
                # then flip, that turns 180, making north. But we could do just with one line, with rotation of 270
                self.img = pygame.transform.flip(south, False, True)

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                # rotate the picture 90
                self.img = pygame.transform.rotate(original_img, 90) # CCW

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                # flip means just turn, 180g
                self.img = pygame.transform.flip(original_img, True, False)

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = original_img # we keep just as the original, so just load the original that points to weast

   

    #important
    def get_number(self):
        # it returns the number of the tile that our character is on, so then
        # we can make sure where he is, if he can walk or not

        # Tile.H gets the diference between one block to the next block in horizontal
        # that in this case is 1. Tile.V gets the difference in the vertical,
        # These are constant variables declared in Tile Class

        return ((self.x // self.width) + Tile.H) + ((self.y // self.height) * Tile.V)
      

    # it return the exactly tile the caracther is on, so basacally this one
    # and the one above works toguether
    def get_tile(self):

        return Tile.get_tile(self.get_number())

class Princess(Character):

    pxTile = 32*14 # position x of the tile
    pyTile = 32 # position y of the tile


    princess_original_img = pygame.image.load('../Images/Princess/princess_e.png')
    #princess_original_img = pygame.transform.scale(princess_original_img, (Tile.width, Tile.height))


    def __init__(self):

       

        self.current = 0 

        self.direction = 'w' # save the direction we're goint to, we start with west, and we change it and we rotate
        self.img = Princess.princess_original_img 
    
        Character.__init__(self, Princess.pxTile, Princess.pyTile)


    # draw it and update the position of the princess
    def update(self, screen, total_frames, FPS):

        self.movement()
       # print('Position ',self.get_number())
        screen.blit(self.img, (self.x, self.y))

        # select one of the musics for princess to say
        if total_frames % (FPS * 9) == 0 and total_frames >0: # she is gonna talk every 6 seconds

            r = randint(0, 4)
            sounds = [pygame.mixer.Sound('../Sound_Effects/princess_be_careful.wav'), 
                    pygame.mixer.Sound('../Sound_Effects/princess_come_help.wav'),
                    pygame.mixer.Sound('../Sound_Effects/princess_help_cry.wav'),
                    pygame.mixer.Sound('../Sound_Effects/princess_help.wav'),
                    pygame.mixer.Sound('../Sound_Effects/princess_not_wanna_die.wav')]
            sound = sounds[ r ]
            sound.play()


    def movement(self):

        self.setFutureTile()
        
        if self.tx != None and self.ty != None: # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 1 # speed 

            if X < 0: # --->
                self.x += vel
            elif X > 0: # <----
                self.x -= vel

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None
            


    def setFutureTile(self):

        # princess move inside of the box, just east and west
        # set the new tile target, where she is going to
        if self.direction == 'e':

            future_tile_number = self.get_number() + Tile.H

            if future_tile_number in range(1, Tile.total_tiles + 1):
            
                future_tile = Tile.get_tile(future_tile_number)
                if future_tile.walkable: # if player can move for that direction(future tile), we set the target with that tile
                                         # and the method will take cara of how to move the player smothly - on object-classes.py
                    self.set_target(future_tile)
                    self.rotate('e')

                else:
                    self.direction = 'w'
                    #print('w')

        elif self.direction == 'w':

            future_tile_number = self.get_number() - Tile.H
            #print('Position ',self.get_number())

            if future_tile_number in range(1, Tile.total_tiles + 1):
                
                future_tile = Tile.get_tile(future_tile_number)
                if future_tile.walkable: 
                    self.set_target(future_tile)
                    self.rotate('w')

                    #print(future_tile_number)
                elif future_tile_number <= 32*15:
                    self.direction = 'e'
                   # print(future_tile_number)
            #print('future ',future_tile_number)


    def rotate(self, direction):

        path = '../Images/Princess/princess_'
        png = '.png'

        if direction == 'e':
            self.direction = 'e'
            self.img = pygame.image.load(path + self.direction + png)

        if direction == 'w':
            self.direction = 'w'
            self.img = pygame.image.load(path + self.direction + png)



# control the zombies
class Zombie(Character):

    List = [] # const and static variable, then we can acess all zombies we had created

    # list of zombie images
    survivor_img =[ pygame.image.load('../Images/Enemies/Zombies/zombie1.png'),
                    pygame.image.load('../Images/Enemies/Zombies/zombie2.png'),
                    pygame.image.load('../Images/Enemies/Zombies/zombie3.png')]

    # emmo/life of the zombie
    # but this variable it's not the health of a zombie, it's just a variable to control the health of all zombies
    # if we want to change, you just have to change here
    health = 100
    zombie_dmg = 5
    zombieTimeGeneration = 1 # how many second has to pass to generate a new zombie?
                             # we start with 3. it means a new zombie with appear each 3 seconds
                             # then we can change it depending in the level game

    def __init__(self, x, y):

        # set the image and direction for the rotation/initial
        self.direction = 'e'
        self.img = Zombie.survivor_img[randint(0, 2)]
        self.original_img = self.img
        self.speed = 4 # zombie.speedocity/speed of moviment for each direction

        # set the currently heath when create a new zombie
        self.health = Zombie.health

    	# create the character, and position, from inheritante
        Character.__init__(self, x, y)
        Zombie.List.append(self)
    

    @staticmethod
    def reset():
        index=len(Zombie.List)-1

        while index>=0:
            del Zombie.List[index]
            index-=1

    # update all zombies in the screen, static because don't need class instance
    # this include draw, move, etc. Before we were using draw method and a movement method
    @staticmethod
    def update(screen, survivor):

        for zombie in Zombie.List:   

            # then draw the zombies
            screen.blit(zombie.img, (zombie.x, zombie.y))

            # make a if to calculate if the zombie and player is in the exactly same position of the tile, if zombie touch player
            # because zombie and player movies in different speed, so it will be never in the just exaclty position of the tile
            # can be somewhere of that tile
            if survivor.x % Tile.width == 0 and survivor.y % Tile.height == 0: # both of them are in the same tile
                if zombie.x % Tile.width == 0 and zombie.y % Tile.height == 0: 

                    # get tile number that player is
                    tn = survivor.get_number()

                    # get the tiles around of the currently tile
                    N = tn + -(Tile.V) # V and H and the number of tiles that we move when we move hor or vert, it define in Tile class
                    S = tn +  (Tile.V)
                    E = tn +  (Tile.H)
                    W = tn + -(Tile.H)

                    # create a list just to keep the values of tiles around the player/currently player
                    NSEW = [N, S, E, W, tn]

                    # then we check if zombie achive one of the tile around the player, cannot be in the same one, because player is there
                    #but if it's around, it means zombie "touch the player"
                    # then we reduce his healthy
                    if zombie.get_number() in NSEW:
                        survivor.health -= Zombie.zombie_dmg  # each time the zombie touch the player, it takes 5 emmo
                        if survivor.health <1 : # player died
                            survivor.isAlive = False
                            # play a died/fail music
                            deadSound = pygame.mixer.Sound('../Sound_Effects/welcome/game_over.wav')
                            deadSound.play()
                        if survivor.health <0:
                            survivor.health = 0
                            

            # remove the zombie if player killed him
            if zombie.health <= 0:
                    Zombie.List.remove(zombie)

            
             #   Remove the method movement, and combine with draw
            #@staticmethod
            #def movement():
            #    for zombie in Zombie.List:
            
            if zombie.tx != None and zombie.ty != None: # Target is set

                # get the X and Y difference
                # if the result are positive, it means move left or up, and oposite
                X = zombie.x - zombie.tx
                Y = zombie.y - zombie.ty

                if X < 0: # --->
                    zombie.x += zombie.speed
                    zombie.rotate('e', zombie.original_img) # change the rotation everytime we move the zombie in direction 
                                                            # fo the player

                elif X > 0: # <----
                    zombie.x -= zombie.speed
                    zombie.rotate('w', zombie.original_img)

                if Y > 0: # up
                    zombie.y -= zombie.speed
                    zombie.rotate('n', zombie.original_img)

                elif Y < 0: # dopwn
                    zombie.y += zombie.speed
                    zombie.rotate('s', zombie.original_img)

                if X == 0 and Y == 0: # it moves until get target/next tile - then is time to check next target
                    zombie.tx, zombie.ty = None, None

# This method put a new zombie in the screen, in a random, from the positions set up on spawn_tiles, just above
    @staticmethod # 
    def spawn(total_frames, FPS):
        if total_frames % (FPS * Zombie.zombieTimeGeneration) == 0: # how much new zombies will show up per frame

            # select one of the musics for when the zombie is create
            # however, we create a new zombie around each 3 second, but we don't want to make a zombie sound every 3 second
            # so then we put * 6, to the zombie make sound, roundly choose for the list, in each 6 seconds(around)
            if total_frames % (FPS * 6) == 0 and total_frames >0:

                r = randint(0, 4)
                sounds = [pygame.mixer.Sound('../Sound_Effects/I_will_kill_you.wav'), 
                        pygame.mixer.Sound('../Sound_Effects/zombie_attack.wav'),
                        pygame.mixer.Sound('../Sound_Effects/zombie_scream1.wav'),
                        pygame.mixer.Sound('../Sound_Effects/zombie_scream2.wav'),
                        pygame.mixer.Sound('../Sound_Effects/zombie_come_here.wav')]
                sound = sounds[ r ]
                sound.play()
            


            r = randint(0, len(Tile.dangeounZombies) - 1) # get a random position from spawn_tiles, to put the zombie on screen
            tile_num = Tile.dangeounZombies[r] # get the number in that random position of the list
            spawn_node = Tile.get_tile(tile_num) # get the tile that represents that tile
            Zombie(spawn_node.x, spawn_node.y) # create a new zombie with that tile x and y position, and add to the static 
                                                # List, that has all zumbies 

    


# main character class
class Survivor(Character):

    # list of player images with differents guns
    survivor_img =[ pygame.image.load('../Images/Survivor/survivor_pistol.png'),
                    pygame.image.load('../Images/Survivor/survivor_shotgun.png'),
                    pygame.image.load('../Images/Survivor/survivor_automatic.png')]

    zombieScore = 2 # how many score the play win when he kill a zombie

    #survivor_img[0] = pygame.transform.scale(survivor_img[0], (Tile.width, Tile.height))
    #survivor_img[1] = pygame.transform.scale(survivor_img[1], (Tile.width, Tile.height))
    #survivor_img[2] = pygame.transform.scale(survivor_img[2], (Tile.width, Tile.height))

    def __init__(self, x, y):

        # give heathy/life for our player
        self.health = 500
        self.score = 0 # keep tracking the player score
        self.isAlive = True  # player start alive, and if his helthy gets bellow 0, he dies

        self.speed = 16 # speed that player walk

        # it saves the current image with gun, and we get the image gun from the list above, so 0 it's the first position, that is a pistol
        self.current = 0 # 0 -> pistol, 1 -> shotgun, 2 -> automatic

        self.direction = 'e' # save the direction we're goint to, we start with west, and we change it and we rotate
        self.img = Survivor.survivor_img[0] # the self.img  save the currectly picture for the currectly direction

        # have save the future tile number(target/next tile to move)
        self.future_tile_number = None

        Character.__init__(self, x, y)

    # get the name type of the guns
    def get_bullet_type(self):

        if self.current == 0:
            return 'pistol'
        elif self.current == 1:
            return 'shotgun'
        elif self.current == 2:
            return 'automatic'

    # function to draw and update the position(move) of the player in the scrren
    def update(self, screen, clock_elapsed):

        self.img = Survivor.survivor_img[self.current]
        rotateDirection = self.direction
        self.direction = ''
        self.rotate(rotateDirection)

        # check if next tile/target is a portal, if it's, we change the player position to one of the other portal tile
        if self.tx != None and self.ty != None: 
            self.movement(clock_elapsed)
            # have to change here, instead get where we are, get where we are going to
            targetTileNumber = ((self.x // self.width) + Tile.H) + ((self.y // self.height) * Tile.V)

            # check if the next tile number is actually inside of the portals list, in the tile class
            # it holds the tile numbers that has a portal
            if self.future_tile_number in Tile.portals:
                sortNewPortalTile = randint(0, 3)
                # make sure if actually move from the portal to another one
                while Tile.portals[sortNewPortalTile]==targetTileNumber:
                    sortNewPortalTile = randint(0, 3)

                # then change the position of player to the new portal x and y position
                futureSortPortal = Tile.get_tile(Tile.portals[sortNewPortalTile])
                
                """for i in range(10000):
                    for i in range(10000):
                        a=i
                """
                self.x = futureSortPortal.x
                self.y = futureSortPortal.y

                self.tx = None
                self.ty = None
                # after move to the new portal, we move the player, just to make the action of walking throught the portal
                """self.tx = self.x + 32  
                self.ty = self.y + 32 
                self.movement()
                """
            

        screen.blit(self.img, (self.x, self.y))
        


    def rotate(self, direction):

        # first, load the survivor picture with currently gun
        self.img = Survivor.survivor_img[self.current]

        if direction == 's':
            if self.direction != 's': # direction is where the next target of the player is, but then if you go all north, 
            # it's gonna reasignment/load the picture all the time, every loop. So then, whe put if self.direction !='n'
            # it's mean if we are going all north, we are gonna laod and rotate just once, in the first loop. It saves memory 
                self.direction = 's'
                south = pygame.transform.rotate(self.img, 90)
                self.img = pygame.transform.flip(south, False, True)

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                self.img = pygame.transform.rotate(self.img, 90) # CCW

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = Survivor.survivor_img[self.current] # original image already points to east

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = pygame.transform.flip(self.img, True, False)

  
        
 # it's not static for the player, because we have to have the player, and we have just one
    # this method make the movement smotly, instead of move a whole position, we move part of, so then it's like we
    # are walking in the path
    def movement(self, clock_elapsed):

        if self.tx != None and self.ty != None: # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            if X < 0: # --->
                self.x += self.speed #* clock_elapsed
            elif X > 0: # <----
                self.x -= self.speed #* clock_elapsed

            if Y > 0: # up
                self.y -= self.speed #* clock_elapsed
            elif Y < 0: # dopwn
                self.y += self.speed #* clock_elapsed

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None



class Bullet(pygame.Rect):
    
    width, height = 7, 10
    List = []

    # use a dictionary, so when you acess with the key gun, it get the link from the image
    imgs = { 'pistol' : pygame.image.load('../Images/Survivor/pistol_b.png'),
            'shotgun' : pygame.image.load('../Images/Survivor/shotgun_b.png'),
            'automatic' : pygame.image.load('../Images/Survivor/automatic_b.png') }
    
    # this save how mach ammo each gun takes from the zombie
    # pistol for example take 1/3 of the emmo, so it's mean he needs to shot 3 times with pistol to kill the zombie
    gun_dmg = {'pistol' : (Zombie.health / 3) + 1,
                'shotgun' : Zombie.health / 2,
                'automatic' : (Zombie.health / 6) + 1 }

    

                      # x and y of the player position
    def __init__(self, x, y, velx, vely, direction, type_):

        self.gun_sounds = [pygame.mixer.Sound('../Sound_Effects/pistol_fire1.wav'), 
                           pygame.mixer.Sound('../Sound_Effects/shotgun_fire1.wav'),
                           pygame.mixer.Sound('../Sound_Effects/automatic_fire1.wav')]

        # use to control the amount of bullets shoot. to don't shot every single time
        # makig a line of bullets
        # we don't check when the gun is automatic, because it can shoot a lot in the same time
        if type_ == 'shotgun' or type_ == 'pistol' or type_ == 'automatic':
            try:
                #list[-1] get the last value of the list
                # x diference and y diference betwen bulletes
                dx = abs(Bullet.List[-1].x - x)
                dy = abs(Bullet.List[-1].y - y)

                # we make 2 differents if because the shotgun has more power than pistol
                # so then we can shoot more with pistol in the same time
                # it's here, in the number 50 pixels and 30 pixels, that we calculate the intervale of the shoot

                if dx < 70 and dy < 70 and type_ == 'shotgun':
                    y -=4 # shotgun is a double shoot, so just to up the shoot, to apear in the center of the plaer
                          # we decrease the bullet y
                    

                    return

                elif dx < 60 and dy < 60 and type_ == 'pistol':
                    
                    return   

                elif dx < 40 and dy < 40 and type_ == 'automatic':
                   
                    return     

            except: pass

        try:

                if  type_ == 'shotgun':
                    sound = self.gun_sounds[1]
                    vol = sound.get_volume()
                    sound.set_volume(min(vol*1,0.25))
                    sound.play()

                elif type_=='pistol':
                    sound = self.gun_sounds[0]
                    vol = sound.get_volume()
                    sound.set_volume(min(vol*1,0.25))
                    sound.play()

                elif type_ == 'automatic':
                    sound = self.gun_sounds[2]
                    vol = sound.get_volume()
                    sound.set_volume(min(vol*1,0.25))
                    sound.play()    

        except: pass
       

        self.type = type_
        self.direction = direction
        self.velx, self.vely = velx, vely

        # make the rotate of the bullet, just like we did with the character rotate
        if direction == 'n':                        # it get the path of the bullet in the dictio, with key = type
            south = pygame.transform.rotate(Bullet.imgs[type_], 90) # CCW
            self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            self.img = pygame.transform.rotate(Bullet.imgs[type_], 90) # CCW

        if direction == 'e':
            self.img = pygame.transform.flip(Bullet.imgs[type_], True, False)

        if direction == 'w':
            self.img = Bullet.imgs[type_]

        # create the rectangle to hold the image
        pygame.Rect.__init__(self, x, y, Bullet.width, Bullet.height)
        # add the bullet to the list
        Bullet.List.append(self)


        # draw
        # update
        # collision --> zombies, tiles

    # check if the bullet go out of the screen, and remove it
    def offscreen(self, screen):

        if self.x < 0:
            return True
        elif self.y < 0:
            return True
        elif self.x + self.width > screen.get_width(): # -->
            return True
        elif self.y + self.height > screen.get_height():
            return True
        return False


    # method to draw, update, and check collision
    @staticmethod
    def update(screen,survivor):

        # check bullet by bullet
        for bullet in Bullet.List:

            # first move it
            bullet.x += bullet.velx
            bullet.y += bullet.vely

            # draw it
            screen.blit(bullet.img, (bullet.x , bullet.y))

            # check if it's off of screen, if it's, remove it from the list, and jump for the next loop(buller)
            if bullet.offscreen(screen):
                Bullet.List.remove(bullet)
                continue # jump for next interaction loop

            
            # check zombie by zombie if that bullet hit one of the zombies
            for zombie in Zombie.List:
                # if the bullet hit a zombie
                if bullet.colliderect(zombie): # method that calculate if there's colision between rectangles
                    
                    # remove ammo from the zombie, depending of each gum
                    zombie.health -= Bullet.gun_dmg[bullet.type]       # gum demage
                    # if player killed zombie, his score is increase
                    if zombie.health <= 0 :     
                        survivor.score+= Survivor.zombieScore  # increase score for user, when he kill a zombie

                    # remove the buller, because it can heat just one zombie, and break the for zombie
                    Bullet.List.remove(bullet)
                    break
                    

            # check if bullet colides with any tile not walkable(wall)
            for tile in Tile.List:
                
                if bullet.colliderect(tile) and not(tile.walkable):
                    try:
                        # then remove that tile
                        Bullet.List.remove(bullet)
                    except:
                        break # if bullet cannot be removed, then GTFO


class LifeBonus(pygame.Rect):

    width, height = 26,26
    List =[]
    life_img = pygame.image.load('../Images/Bonus_Life/heart3.png')
    extra_life = 50
    bonusTimeGeneration = 15 # each 12 second, a new bonus will apear in the screen
    bonusTimeExperation = 11 # how lond time the bonus will stay in the screen for the player

    def __init__(self, x, y):

        self.img = LifeBonus.life_img
        self.extra_life = LifeBonus.extra_life
        self.bonusTimeExperation = LifeBonus.bonusTimeExperation

        pygame.Rect.__init__(self, x, y, LifeBonus.width, LifeBonus.height)
        LifeBonus.List.append(self)


    @staticmethod 
    def spawn(total_frames, FPS):

        if total_frames % (FPS * LifeBonus.bonusTimeGeneration) == 0 and total_frames >0: 

            luckBonus = randint(1,4) # in other words, player has 33.33% of gain a heart life, each 30 seconds

            if luckBonus == 1:  # new heart will show up if the rand luck bonus is 1
                # have to put the music

                randTile = randint(1,601) # get a randow number tile, we have 600 tiles in the screen

                while(not Tile.isTileFree(randTile)):  # check if actually, that tile is free, or other words, it's an empty path
                    randTile = randint(1,601) # get a randow number tile, we have 600 tiles in the screen

                tile = Tile.get_tile(randTile) # get the tile, randTile is just the tile number
                LifeBonus(tile.x, tile.y)  # have to get the x and y from the tile number now




    @staticmethod # update the bonus, checkig if the time to stay in the screen has expired, or if player caught it
    def update(screen, survivor, total_frames, FPS):

        for life in LifeBonus.List:

            # remove the bonus lifes after the bonus time has expired
            if total_frames % (FPS * LifeBonus.bonusTimeExperation) == 0 and total_frames >0: 
                #pass
                LifeBonus.List.remove(life)

            else:
                screen.blit(life.img, (life.x, life.y) )
                # check if player collected the life
                if life.colliderect(survivor): 

                    # Player receive bonus points
                    survivor.health += life.extra_life

                    # remove life from list
                    LifeBonus.List.remove(life)




class FruitsBonus(pygame.Rect):

    width, height = 32,32
    List = [] # list to save the fruits in the screen, at that moment
    extra_points = 20
    bonusTimeGeneration = 8 # each 11 second, a new bonus will apear in the screen
    bonusTimeExperation = 11 # how lond time the bonus will stay in the screen for the player

    fruits_img =[ pygame.image.load('../Images/Fruits_Bonus/apple_red.png'),
                    pygame.image.load('../Images/Fruits_Bonus/candy_green.png'),
                    pygame.image.load('../Images/Fruits_Bonus/candy_red.png'),
                    pygame.image.load('../Images/Fruits_Bonus/candy_white.png'),
                    pygame.image.load('../Images/Fruits_Bonus/cherry.png'),
                    pygame.image.load('../Images/Fruits_Bonus/grape_blue.png'),
                    pygame.image.load('../Images/Fruits_Bonus/grape_orange.png'),
                    pygame.image.load('../Images/Fruits_Bonus/grape_red.png'),
                    pygame.image.load('../Images/Fruits_Bonus/kiwi.png'),
                    pygame.image.load('../Images/Fruits_Bonus/orange.png'),
                    pygame.image.load('../Images/Fruits_Bonus/pear.png'),
                    pygame.image.load('../Images/Fruits_Bonus/pineaple.png'),
                    pygame.image.load('../Images/Fruits_Bonus/strawberry.png'),
                    pygame.image.load('../Images/Fruits_Bonus/watermelon.png')]

    def __init__(self, x, y):

        self.img = FruitsBonus.fruits_img[randint(0,13)]
        self.extra_points = FruitsBonus.extra_points
        self.bonusTimeExperation = FruitsBonus.bonusTimeExperation

        pygame.Rect.__init__(self, x, y, FruitsBonus.width, FruitsBonus.height)
        FruitsBonus.List.append(self)

    @staticmethod # Create a new fruits in a specific intervale of tiem
    def spawn(total_frames, FPS):

        if total_frames % (FPS * FruitsBonus.bonusTimeGeneration) == 0 and total_frames >0: 

            # have to put the music

            randTile = randint(1,601) # get a randow number tile, we have 600 tiles in the screen

            while(not Tile.isTileFree(randTile)):  # check if actually, that tile is free, or other words, it's an empty path
                randTile = randint(1,601) # get a randow number tile, we have 600 tiles in the screen

            tile = Tile.get_tile(randTile) # get the tile, randTile is just the tile number
            FruitsBonus(tile.x, tile.y)  # have to get the x and y from the tile number now




    @staticmethod # update the bonus, checkig if the time to stay in the screen has expired, or if player caught it
    def update(screen, survivor, total_frames, FPS):

        for fruit in FruitsBonus.List:

            # remove the bonus fruits after the bonus time has expired
            if total_frames % (FPS * FruitsBonus.bonusTimeExperation) == 0 and total_frames >0: 
                #pass
                FruitsBonus.List.remove(fruit)

            else:
                screen.blit(fruit.img, (fruit.x, fruit.y))
                # check if player collected the fruit
                if fruit.colliderect(survivor): 

                    # Player receive bonus points
                    survivor.score += fruit.extra_points

                    # remove fruit from list
                    FruitsBonus.List.remove(fruit)






























