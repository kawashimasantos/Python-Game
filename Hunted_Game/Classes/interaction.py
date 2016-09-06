# file to control the logic of the game
# control user event input, movements of the characters, etc

import pygame, sys
from tiles import Tile
from object_classes import Bullet

# function to haldle the survivor interaction with the screen
def interaction(screen, survivor):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # you can change the gun when you press the key/letter 'e'
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                survivor.current += 1
                survivor.current %= 3 # to make sure it goes to 0,1,2 - because when you get 3, mode 3 by 3 =0
                

    # Movemnt of the player is gonna be not just when you press a key, but when you press or you are holding
    # that's why it goes outside of the loop events
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:# North

    	# first, before move we have to ckeck if that position is walkable
    	# so them, you first get the "new" position for that character
    	# in this case we get the number of the character, that represents
    	# his position on screen, minus how many we can move, Remember that is is to
    	# left or right, is gonna move always 1 block, if it's up or down, 18 block
        future_tile_number = survivor.get_number() - Tile.V

        # then we check if that number of tile is walkable, for the we move
        # the character
        # first if check if the new tile actually exist, if the tile number is in the Tile list, it can move
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable: # if player can move for that direction(future tile), we set the target with that tile
                                     # and the method will take cara of how to move the player smothly - on object-classes.py
                survivor.set_target(future_tile) # it make the movemnt
                survivor.rotate('n') # since we are moving north, we change the rotation of the picture to north
                survivor.future_tile_number = future_tile_number
             
    if keys[pygame.K_s]: # South
    
        future_tile_number = survivor.get_number() + Tile.V
        if future_tile_number in range(1, Tile.total_tiles + 1):

            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable: # if player can move for that direction(future tile), we set the target with that tile
                                     # and the method will take cara of how to move the player smothly - on object-classes.py
                survivor.set_target(future_tile)
                survivor.rotate('s') 
                survivor.future_tile_number = future_tile_number 

    if keys[pygame.K_a]: # West
        future_tile_number = survivor.get_number() - Tile.H

        if future_tile_number in range(1, Tile.total_tiles + 1):
            
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable: # if player can move for that direction(future tile), we set the target with that tile
                                     # and the method will take cara of how to move the player smothly - on object-classes.py
                survivor.set_target(future_tile)
                survivor.rotate('w')
                survivor.future_tile_number = future_tile_number

    if keys[pygame.K_d]: # East
        future_tile_number = survivor.get_number() + Tile.H
       # print("Future left ",future_tile_number)

        if future_tile_number in range(1, Tile.total_tiles + 1):
            
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable: # if player can move for that direction(future tile), we set the target with that tile
                                     # and the method will take cara of how to move the player smothly - on object-classes.py
                survivor.set_target(future_tile)
                survivor.rotate('e')
                survivor.future_tile_number = future_tile_number

    # you use the arrow to rotate the character, to point for with direction you want to shot. so you can walk left
    # pressind 'A', but zombies are coming from right, so you can turn your face to right and shot in that direction
    # but keep walking for left

    if keys[pygame.K_LEFT]:
        survivor.rotate('w')
        
        Bullet(survivor.centerx, survivor.centery +5, -20, 0, 'w', survivor.get_bullet_type() )

    elif keys[pygame.K_RIGHT]:
        survivor.rotate('e')
        Bullet(survivor.centerx, survivor.centery +5, 20, 0, 'e', survivor.get_bullet_type() )

    elif keys[pygame.K_UP]:
        survivor.rotate('n')
        Bullet(survivor.centerx, survivor.centery +5, 0, -20, 'n', survivor.get_bullet_type() )

    elif keys[pygame.K_DOWN]:
        survivor.rotate('s')
        Bullet(survivor.centerx, survivor.centery +5, 0, 20, 's', survivor.get_bullet_type() )






