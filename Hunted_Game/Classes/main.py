# Copyright by Thiago Santos
# All rights reserved

# Reference Websites
# http://www.raywenderlich.com/4946/introduction-to-a-pathfinding    - About A* path
# http://www.raywenderlich.com/4946/introduction-to-a-pathfinding    - About A* path
# http://programarcadegames.com/index.php   - Examples of pygame codes
# http://opengameart.org/  - Free Kenney(imgs btmp)
# http://soundbible.com/tags-shooting.html  - Free effects sounds
# http://stackoverflow.com/  - Most of my problem's solutions are found in this website

# Main class 
# Use to control the logic of the game
import pygame, sys
from time import sleep
from tiles import Tile
from object_classes import *
# from class interaction you import method interaction
from interaction import interaction
from A_Star_Path import A_Star_Path
import DisplayText  # class to display any text on screen
from welcome_over import *



BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [153, 153, 153]
BEGE = [222,184,135]
GREEN = [0,255,0]
RED = [255,0,0]
WIDTH = 960
HEiGHT = 640

pygame.init()
pygame.mixer.pre_init()
pygame.mixer.set_num_channels(3)
pygame.font.init() # initialize font class in pygame
pygame.mixer.init()
  
                                # 30 tiles horizontal per line
                                # 30 columns of blocks in total

                                # and 20 vertical per vertical line
                                # 20 lines of block in total

screen = pygame.display.set_mode((WIDTH, HEiGHT)) # 32 x 32  size of tiles
pygame.display.set_caption("Hunted")

# set up all the tiles
Tile.pre_init(screen)

clock = pygame.time.Clock()
FPS = 24 # if we increase this number, the speed of character will be lower
total_frames = 0
total_frames_welcome = 0

survivor = Survivor(32, 32*6)

princess = Princess()

# set the welcome/final page of the game
Welcome.set_welcome(screen)

# load the background music
#pygame.mixer.music.load('../Sound_Effects/background2.wav')
#pygame.mixer.music.play(-1) # -1 put to loop the music forever

welcome_img = pygame.image.load('../Images/welcome/zombie2.jpg')

pygame.mouse.set_visible(False)

# Loop until the user clicks the close button.
done = False
while True:

    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    clock_elapsed_seconds = milliseconds / 1000.0 # seconds passed since last frame (float)

    # show the welcome page just at the begening of end of the game
    if Welcome.page_welcome_active:

        Welcome.setScoresComparable()
        
        # start/restart the game
        survivor = Survivor(32, 32*6)

        princess = Princess()

        Zombie.reset()

        # uf the welcome total frames is 0(just start), then we load and play the music for the welcome page
        if total_frames_welcome ==0:
            pygame.mixer.music.load('../Sound_Effects/welcome/Haunted1.wav')
            # play the background game music
            pygame.mixer.music.play(-1) # -1 put to loop the music forever
            Welcome.update() # update the menu when run in the first time

        screen.blit(welcome_img, (0,0) )
        Welcome.draw_menus(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if Welcome.buttonSelected < 4: # if we can still move down
                        Welcome.buttonSelected +=1
                        Welcome.update() # method that update the image of the buttons, changing to selected or not

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if Welcome.buttonSelected >1: # if we can still move up
                        Welcome.buttonSelected -=1
                        Welcome.update()

                # user press enter in one of the options
                if event.key == pygame.K_SPACE:
                    if Welcome.buttonSelected == 1: # if the new game button is selected
                        Welcome.page_welcome_active = False
                        pygame.mixer.music.load('../Sound_Effects/background2.wav')
                        # play the background game music
                        pygame.mixer.music.play(-1) # -1 put to loop the music forever

                    if Welcome.buttonSelected == 2:
                        Welcome.page_score_active = True; # currently page changes for show scores page
                        Welcome.page_welcome_active = False

                    if Welcome.buttonSelected == 3:
                        Welcome.page_help_active = True 
                        Welcome.page_welcome_active = False

                    if Welcome.buttonSelected == 4: # quit the game
                        pygame.quit()
                        sys.exit()

                    

        total_frames_welcome += 1

    # page to show the game's best scores
    elif Welcome.page_score_active:

        Welcome.display_scores(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # return to welcome page
                    Welcome.page_score_active = False 
                    Welcome.page_welcome_active = True

    # page to show the help page, with all the tips player need to play
    elif Welcome.page_help_active:

        Welcome.display_help(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Welcome.page_help_active = False 
                    Welcome.page_welcome_active = True

    # page to get player's names and score(best), and save to the scores.txt file
    elif Welcome.page_getScore:

        Welcome.get_user_score(screen, survivor.score)

        if Welcome.getUserScoredone:

            # make a pause before reset everything
            if total_frames % (FPS * 2) == 0:
                Welcome.getUserScoredone = False
                Welcome.page_getScore = False
                Welcome.page_welcome_active = True
                Welcome.txtbxScoreSaved = False

        total_frames +=1

    #otherwise and the player is alive, show and play the game
    elif survivor.isAlive:
        """
        if total_frames == 0:
            # stop the currectly sound to load and play the next one
            #pygame.mixer.music.stop()
            # load the background music
            pygame.mixer.music.load('../Sound_Effects/background2.wav')
            # play the background game music
            pygame.mixer.music.play(-1) # -1 put to loop the music forever
        """

        ####  Put the background image to screen
       
        Tile.draw_tiles(screen)

        princess.update(screen,total_frames, FPS)
     

        # interaction method from Interaction class. It control all events from the game
        interaction(screen, survivor)

        # move to the new direction, and also draw the player in the screen
        survivor.update(screen,clock_elapsed_seconds)

        # check if there's colision of any bullet, all the time
        Bullet.update(screen,survivor)

        # create and put a new zombie in the screen, controlling by the total of the frames
        Zombie.spawn(total_frames, FPS)

        Zombie.update(screen, survivor)

        # make the math to check the better path for each zombie 
        A_Star_Path(screen, survivor, total_frames,FPS) # it runs the logic and make the zombies walk position by position

        # create a new fruit bonus, in an specific intervale of time
        FruitsBonus.spawn(total_frames, FPS)

        FruitsBonus.update(screen,survivor, total_frames, FPS)

        LifeBonus.spawn(total_frames, FPS)

        LifeBonus.update(screen,survivor, total_frames, FPS)

        # display the healthy of the player in the screen
        DisplayText.text_to_screen(screen, 'Health: {0}'.format(survivor.health), 0,0,16, WHITE)

        # display the player score
        DisplayText.text_to_screen(screen, 'Score: {0}'.format(survivor.score), 32*10,0,16, WHITE)

        # display the currently best score ever in the game(goal for the player)
        # if player had got a better score than the highest in the file, his score appear in screen
        if survivor.score > Welcome.highestScoreFile:
            DisplayText.text_to_screen(screen, 'Best Score Recorded: {0}'.format(survivor.score), 32*20,0,16, WHITE)

        # else, the highest score in the file appear 
        else:
            DisplayText.text_to_screen(screen, 'Best Score Recorded: {0}'.format(Welcome.highestScoreFile), 32*20,0,16, WHITE)

        total_frames += 1

    elif not survivor.isAlive :

        pygame.mixer.music.stop()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display you're dead
        # save the score
        # go back to the welcome page

        
        GameOver.game_over(screen)  # GameOver - class from welcome_over.py
        if total_frames % (FPS * 2) == 0:

            # if player had a god score, highest than any of the scores saved in the game, it goes to
            # get and save player score
            if survivor.score > Welcome.lowestScoreFile:
                Welcome.page_getScore = True
            # else, player is just a loser, and game just restart
            else:
                Welcome.page_welcome_active = True # reset the game and display the first screen
        
        total_frames += 1

        # load and play background welcome page sound again
        pygame.mixer.music.load('../Sound_Effects/welcome/Haunted1.wav')
        # play the background game music
        pygame.mixer.music.play(-1) # -1 put to loop the music forever

        

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()






