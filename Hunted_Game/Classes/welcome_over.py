# This class will works to show the initial/final page, with instructions, best scores, and start a new game

import pygame
from random import randint
from  DisplayText import text_to_screen
import time
import os
from pygame.locals import *
import sys, eztext


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
BEGE = [222,184,135]
GREEN = [0,255,0]
RED = [255,0,0]

pygame.font.init()

class GameOver(pygame.Rect):
	gameOver_img = pygame.image.load('../Images/game_over/died.jpg')
	
	@staticmethod
	def game_over(screen):
		screen.blit(GameOver.gameOver_img, (0,0) )
		



class Welcome(pygame.Rect):

	width, height = 130,40
	List = []
	page_welcome_active = True
	page_help_active = False # it change the page/frame, to show just the instructions
	page_score_active = False
	page_getScore = False
	highestScoreFile = 0
	lowestScoreFile = 0  # get the lowest Score we have saved in the file
	buttonSelected = 1  # we have 4 buttons, and each number represent widtch button we selected
	total_buttons = 0  # save how many menus we have, and then we can ckeck the button number
	getUserScoredone = False # get user input for the score name
	txtbxScoreSaved = False

	# create the input box
	txtbx = eztext.Input(maxlength=7, color=(255,255,255), prompt='Enter you name:  ')

	# Save the buttons images
	newGame_img = pygame.image.load('../Images/buttons/newGame.png')
	newGame_selected_img =pygame.image.load('../Images/buttons/newGame_selected.png')

	help_img = pygame.image.load('../Images/buttons/help.png')
	help_selected_img =pygame.image.load('../Images/buttons/help_selected.png')
	help_message = pygame.image.load('../Images/welcome/help_message.png')
	help_zombie_img = pygame.image.load('../Images/welcome/zombie2.jpg')

	score_show_img = pygame.image.load('../Images/welcome/zombie1.jpg')

	quit_img = pygame.image.load('../Images/buttons/quit.png')
	quit_selected_img =pygame.image.load('../Images/buttons/quit_selected.png')

	score_img = pygame.image.load('../Images/buttons/score.png')
	score_selected_img =pygame.image.load('../Images/buttons/score_selected.png')

	exit_selected_img =pygame.image.load('../Images/buttons/exit_selected.png')

	@staticmethod
	def set_welcome(screen):
		# set the Welcomes's Menus
		Welcome(40,120,'new_game', screen)
		Welcome(40,220,'score', screen)
		Welcome(40,320,'help', screen)
		Welcome(40,420,'quit', screen)
		Welcome(830,600,'exit', screen)

	def __init__(self, x, y, Type, screen): 

		if Type =='new_game':
			self.img = Welcome.newGame_img

		elif Type =='score':
			self.img = Welcome.score_img

		elif Type =='help':
			self.img = Welcome.help_img

		elif Type =='quit':
			self.img = Welcome.quit_img

		elif Type =='exit':
			self.img = Welcome.exit_selected_img

		
		Welcome.setScoresComparable()
		

		self.type = Type 
		self.menu_number = Welcome.total_buttons +1
		pygame.Rect.__init__(self, (x, y) , (Welcome.width, Welcome.height) )

		Welcome.List.append(self) # add the title in the list of tiles
		Welcome.total_buttons +=1 # update the number of menus in the Welcome class


	@staticmethod
	def setScoresComparable():
		try:
			# make sure there's always the file scores
			# if there's not, it just create one
			if not os.path.exists('scores.txt'):
				open('scores.txt', 'w').close() 

			text_file = open("scores.txt", "r")
			lines = text_file.readlines()

			# there are at least one score in the file
			if len(lines) >=2:
				Welcome.highestScoreFile = int(lines[1]) # get the first score(hisghest)
				Welcome.lowestScoreFile = int(lines[len(lines)-1]) # get the last value of the list
		except:
			print("Error opennig file")

	# method to draw all menus in the screen every frame
	@staticmethod
	def draw_menus(screen):
		for menu in Welcome.List:   

			if menu.type != 'exit':
	            # then draw the menu in the frame - not the exit menu, that is draw just in the help windown
				screen.blit(menu.img, menu);

		text_to_screen(screen, "By: Thiago Santos.",  740,600,15,BEGE)		
		text_to_screen(screen, "Copyright. All rights reserved.",680,620,15,BEGE)


	@staticmethod
	def display_scores(screen):
		
		screen.blit(Welcome.score_show_img, (0,0) )

		# open and read the entire file 
		try:
			# make sure there's always the file scores
			# if there's not, it just create one
			if not os.path.exists('scores.txt'):
				open('scores.txt', 'w').close() 

			text_file = open("scores.txt", "r")
			lines = text_file.readlines()
		
			text_to_screen(screen, "Player's Name:", 50,50,25, RED)
			text_to_screen(screen, "Score:", 340,50,25,RED)

			xNamePos = 50
			yNamePos = 100

			xScorePos = 340
			yScorePos = 100
			
			index =1
			for line in lines:
				lineWithoutN = ""
				for char in line:
					if char != "\n":
						lineWithoutN += char
				if index %2 !=0:
					text_to_screen(screen, lineWithoutN, xNamePos, yNamePos, 20, WHITE)
					yNamePos +=50
				else:
					text_to_screen(screen, lineWithoutN, xScorePos, yScorePos, 20, WHITE)
					yScorePos +=50

				index +=1

			text_file.close()

		except:
			print("Error opennig file")

		# draw the exit button
		for menu in Welcome.List:   
			if menu.type == 'exit': # draw the button exit 
				screen.blit(menu.img, menu);
	
	@staticmethod
	def get_user_score(screen, playerScore):

		events = pygame.event.get()
		for event in events:

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					Welcome.getUserScoredone = True

		screen.blit(Welcome.score_show_img, (0,0) )
		text_to_screen(screen, "Congratulations, you're in the top 5 of best scores", 80, 35, 25, RED)
		text_to_screen(screen, "Name", 80,100,25, RED)
		text_to_screen(screen, "Final Score", 330,100,25, RED)
		text_to_screen(screen, playerScore, 330,200,22, RED)
		
		# while user doen's press space to save score, he can still typing
		if not Welcome.getUserScoredone:
			# update txtbx
			Welcome.txtbx.update(events)
			text_to_screen(screen, "Press Space to save", 130,250,17, WHITE)

		else:
			# if already save the score in the file
			if Welcome.txtbxScoreSaved:
				# show message saved with sucess
				text_to_screen(screen, "Your score was successfully saved", 50,400,25, BEGE)

			# otherwise, save the score
			else:
				listNames =[]
				listScores = []
				listCopyScores = []
				listIndexOrder = []
				if not os.path.exists('scores.txt'):
					open('scores.txt', 'w').close() 

				text_file = open("scores.txt", "r")
				lines = text_file.readlines()

				index =1
				done = False
				for line in lines:

					# save a diction with the names, with index being the key
					if index %2 !=0:
						name = line
					else:
						score = line	
						listNames.append(name)
						listScores.append(score)
						listCopyScores.append(score)

					index +=1

				text_file.close()

				# order the list 
				highest = -1
				indexHighest = 0
				count = 1

				# add player score to the list
				listScores.append( str( str(playerScore) + "\n") )
				listCopyScores.append(playerScore)
				# add player name to the list of name
				listNames.append( str(Welcome.txtbx.getValue() +"\n") )
				while not done:

					for i in range(0,len(listCopyScores)):
						if int(listCopyScores[i]) > highest:
							highest = int(listCopyScores[i])
							indexHighest = i

					listIndexOrder.append(indexHighest)
					listCopyScores[indexHighest] = "-2"
					indexHighest = -1
					highest = -1

					if count >= len(listCopyScores):
						done = True

					count +=1

				# after sort the file, time to write the "new" sequence of the file
				text_file = open("scores.txt", "w")

				
				for i in range(0,len(listScores)):
					# Game allowed to save just the top 5 scores
					if i <5:
						name = str(listNames[listIndexOrder[i]])
						score = str(listScores[listIndexOrder[i]]) 
						text_file.write(name)
						text_file.write(score)
				text_file.close()



				Welcome.txtbxScoreSaved = True
				Welcome.txtbx.resetValue()
			

        # blit txtbx on the sceen
		Welcome.txtbx.draw(screen)

		return Welcome.getUserScoredone
		


	@staticmethod
	def display_help(screen):
		screen.blit(Welcome.help_zombie_img, (0,0) )
		screen.blit(Welcome.help_message, (70,50) )
		for menu in Welcome.List:   

			if menu.type == 'exit': # draw the button exit 
				screen.blit(menu.img, menu);


	@staticmethod
	def update():

		for menu in Welcome.List:

			if menu.type =='new_game' : # if the new game button is selected, we change the image then
				if Welcome.buttonSelected == menu.menu_number: # if it's selected we change the img
					menu.img = Welcome.newGame_selected_img
				else:
					menu.img = Welcome.newGame_img

			elif menu.type =='score' : 
				if Welcome.buttonSelected == menu.menu_number: 
					menu.img = Welcome.score_selected_img
				else:
					menu.img = Welcome.score_img

			elif menu.type =='help' : 
				if Welcome.buttonSelected == menu.menu_number: 
					menu.img = Welcome.help_selected_img
				else:
					menu.img = Welcome.help_img

			elif menu.type =='quit' : 
				if Welcome.buttonSelected == menu.menu_number: 
					menu.img = Welcome.quit_selected_img
				else:
					menu.img = Welcome.quit_img








