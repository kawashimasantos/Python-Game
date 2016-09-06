# This class works wo make all the algoritm that calculates the better path that each zombie should take to achieve
# the main character

import pygame
from object_classes import *
from tiles import Tile

# a non return type function that make all the algoritm to the path
def A_Star_Path(screen, survivor, total_frames, FPS):

	half = Tile.width // 2

	# this number is the number of tile the character walks in each direction
	# right(east - e), it moves 1, left, -1; North 18(horizontal) just have to count in the screen
	N = -30 # north 
	S = 30 # south
	E = 1 # east
	W = -1 # west

	# same case for these ones
	NW = -23 # northwest
	NE = -21
	SE =23
	SW = 21

# it fix the bug that if the player is sunround by walls, the zombie still can
	for tile in Tile.List:
		tile.parent = None
		tile.H, tile.G, tile.F = 0,0,0

# function that put a tile in the tile list, if the surrounding tile of the zombie is in North, South, etc
# not add if it NW, SE, SW, NW, because zombie cannot walk in diagonal
	def blocky(tiles, diagonals, surrounding_node):
		if surrounding_node.number not in diagonals:
			tiles.append(surrounding_node)
		return tiles


	# define each value of these value in each zombie, theses values we use to calculate the better path 
	def get_surrounding_tiles(base_node):

		# makes an array that save all the combinations of tiles surround the zombie( base_node == zombieTile)
		# so if zombie moves to N, W, or etc, we have all these combinations numbers (position + 1 or - 1 or + 18, etc)
		# so then we can use them to our math to predict the better path
		array =(
			(base_node.number + N),
			(base_node.number + NE),
			(base_node.number + E),
			(base_node.number + SE),
			(base_node.number + S),
			(base_node.number + SW),
			(base_node.number + W),
			(base_node.number + NW),
			)

		tiles = []

		# *****
		# make this change to make the zombie to be able to walk just N,S,E,W - not NE,SW, etc
		# original node number
		onn = base_node.number 
		diagonals = [onn + NE, onn + NW, onn + SE, onn + SW]
        # *****


        # this for get all the new position(number of the tiles) from the array, that represet the tiles sorround from the Zombie
        # and get the tile, from Tile list in Tile class. Then we check if zombie can really go in the direction(tile)
        # if it does, we add that tile for the tile list
		for tile_number in array:

			surrounding_tile = Tile.get_tile(tile_number)

			# to avoid a zombie to get possible new path in tiles that doen's exist, for example if the zombie is in the
			# border, it cannot go up, for that we have to avoid with this if below
			if tile_number not in range(1, Tile.total_tiles + 1):
			    continue # if there'e not that tile, we jump the for for the next loop, so then, it doen's run the lines below
			    			# and consequently, it doen't calculate the path for that tile

			if surrounding_tile.walkable and surrounding_tile not in closed_list:
			    #tiles.append(surrounding_tile) # Diagonal movement - just add this and coment next line

				tiles = blocky(tiles, diagonals, surrounding_tile) # make sure to add the tile just if it is n,s,w,e

		return tiles

		
	# G cost doen's change
	def G(tile):
		# formula as well

		# this get the number diference between the the "new" tile and the parent tile
		# it returns for where you're going, -1, +1, 18, +18, etc
		diff = tile.number - tile.parent.number

		# tile.parent.G is just to make it clear, but it'll always gonna start with 0, then result will be 10 and 14
		if diff in (N, S, E, W):
			tile.G = tile.parent.G + 10 # it's just a formula
		elif diff in (NE, NW, SW, SE):
			tile.G = tile.parent.G + 14

	def H(): # for H, we use the marathan calculate method
		for tile in Tile.List:
			# so it means you really get the tile, by reference
			# then we are really change the value of H with this sentence below
			# this formula is from marathan method, more in: http://www.raywenderlich.com/4946/introduction-to-a-pathfinding
			tile.H = 10 * (abs(tile.x - survivor.x) + abs(tile.y - survivor.y)) // Tile.width

	def F(tile):
	    # F = G + H formula - more inf : http://www.raywenderlich.com/4946/introduction-to-a-pathfinding
		tile.F = tile.G + tile.H

	# function that get a tile that has already calculate all the tiles surround it and calculate the values
	# of H, F, G, etc. so we don't do calculate it anymore. So, remove it from open list(that is walkable and we have
		# to calculate the values) and add to the closed list( unwalkable or already process)
	# because we calculate all the possibilites for all zombies, so after get done with one, we remove it from the list
	def swap(tile):
		open_list.remove(tile)
		closed_list.append(tile)


	def get_LFT(): # get Lowest F Value

		# gete all F from all tiles in open_list
		F_Values = []
		for tile in open_list:
			F_Values.append(tile.F)

		o = open_list[::-1] # it basacally just return the same list but in order reverse
		# so then if there are repetive numbers, we get actually the first one, just for better performance

		for tile in o:	# get the lowest F value in Tile
			if tile.F == min(F_Values):
				return tile

# kind of same of how we calculated the G value in G()
	def move_to_G_cost(LFT, tile):

		GVal = 0
		diff = LFT.number - tile.number

		if diff in (N, S, E, W):
			GVal = LFT.G + 10
		elif diff in (NE, NW, SE, SW):
			GVal = LFT.G + 14

		return GVal

	# we did calculate the F,H,G values for the tiles souround the zombie, now we have to find the better path/wat
	# and at the same time, calculate the F,H,G for the "new" future position for the zombie
	# because we calculate for the tiles sounround, and then we have the better tile to go next, but after that
	# we still to go to more tiles, ultil get the main character, no then we make a recursive loop that get calculate
	# all the number for the future tiles, already in the best way/path
	def loop():

		# first we get the lowest F tile, so sen find our better path
		LFT = get_LFT() 

		swap(LFT) # drop the tile with the lowest F from the open_list and drop to close_list
		# so then in the next loop it'll garanted to don't get the same tile again and again

		# then get the "new" surround nodes for the "new"/next tile in the path, to then calculate its G,H,F
		surrounding_nodes = get_surrounding_tiles(LFT)

		for node in surrounding_nodes:

			# same logic we use in the for Zombie, so if the "new" tile is not in the list, we add it, to then calculate
			# its F,G,H 
			if node not in open_list:

			    open_list.append(node)
			    node.parent = LFT

			# it still can get crazy path and direction, so it where G value is important to fix these problems
			elif node in open_list:

				# ***** Imporant
				# this check if it'll be more benefit to go to this node, that is already in the list or not
				calculated_G = move_to_G_cost(LFT, node)
				if calculated_G < node.G:

					# if it's, we change the lowest f, for that node g
					# then recalculate G and F value for that node
					node.parent = LFT 
					G(node)
					F(node)


		# calculate G and F for each node in the open_list again
		for node in open_list:

			G(node)
			F(node)

		# check if the open list is empty, if it's we stop the loop
		# or if the zombie got the main character
		if open_list == [] or survivor.get_tile() in closed_list:
			return 

		loop()


# it goes zombie by zombie the Zombie List, from Zombia class in Object_Classes.py
	for zombie in Zombie.List: 

		# it's speed the zombies - because if the zombie already has its target, we don't need to calculate everything
		# for that zombie, so then we just jump the loop for the next interection of the loop
		if zombie.tx != None or zombie.ty != None:
			continue


		# each zombie has its own list
		# open list we save all the possibilites tiles that we can move, a path 
		open_list = []
		# Close list we save all the tile unwakable and those one we already check and calculate their G,F,H, etc
		# it's not a local variable, it visable for all class
		closed_list = []

		# return the exactly tile the zombie is
		zombie_tile = zombie.get_tile()
		open_list.append(zombie_tile)

		# we need to get tiles that are all around that tile from the zombie
		surrounding_nodes = get_surrounding_tiles(zombie_tile)

		# after return the list of surrounding nodes that acessible
		# we set one by pne for the open_list( means path that is possible to go)
		# and also set the parent equal zombie tile, so then we can check later for those tile that has zombie as a 
		# parent
		# **** where where set the 
		for node in surrounding_nodes:
			node.parent = zombie_tile
			open_list.append(node)      

		swap(zombie_tile)

		H()

		# we make outide, instead of inside of method, lihe H, because we calculate just for 
		#those tiles sunround from the Zombie Tile
		for node in surrounding_nodes:
			G(node)
			F(node) 

		loop()

		# **** After calculate the better path, we have to trace it, to really get there

		# create an array that will save with tile that the zombie has to go
		return_tiles = []

		parent = survivor.get_tile()  # parent reveice the player(main Chareter) tile

		while True:

			return_tiles.append(parent)

			parent = parent.parent # parent get the parent of his parent

			# it means the while loop for runs until calculate the better path, tile by tile, for each zombie
			# and here we trace the path, as we can see drawing the little circles
			# so then we break the for when there's no more player or it zumbie achieve the player
			if parent == None:  # if there's no more player
				break

			if parent.number == zombie.get_number():  # zombie achieve player
				break

		# set a target tile by next goal tile, in the path, for the zombie
		if len(return_tiles) > 1:
			next_tile = return_tiles[-1]
			zombie.set_target(next_tile) # it sets a target for the next tile of the better path, one by one in the loop







