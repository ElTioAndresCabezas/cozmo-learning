#Python script meant to enable Cozmo to play
#Rock, Paper and Scissors
#----------------------------------
#Script de Python para permitir que Cozmo
#juege al cachipun
#----------------------------------
#Developed by / Desarrollado por: Andrés Cabezas
#For IIC1005 class of 2021-1
#Instructed by Professor Denis Parra

'''
ToDo list:
1. Add Light Chaser to all the cubes, to give feedback on the gameplay
2. Give Cozmo expressions when he wins, loses, or ties
3. Make the game just prettier
'''

import cozmo
import asyncio
import time
from cozmo.util import degrees
from random import randint
from PIL import Image as image
import os


class Cube(cozmo.objects.LightCube):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._chaser = None

    def start_light_chaser(self):
        '''Cycles the lights around the cube with 1 corner lit up green,
        changing to the next corner every 0.1 seconds.
        '''
        if self._chaser:
            raise ValueError("Light chaser already running")
        async def _chaser():
            while True:
                for i in range(4):
                    cols = [cozmo.lights.off_light] * 4
                    cols[i] = cozmo.lights.green_light
                    self.set_light_corners(*cols)
                    await asyncio.sleep(0.1, loop=self._loop)
        self._chaser = asyncio.ensure_future(_chaser(), loop=self._loop)
    
    def stop_light_chaser(self):
        if self._chaser:
            self._chaser.cancel()
            self._chaser = None


cozmo.world.World.light_cube_factory = Cube

def image_preparation():
    current_d = os.path.dirname(os.path.realpath(__file__))
    
    rock_png = os.path.join(current_d,'images','rock.png')
    paper_png = os.path.join(current_d,'images','paper.png')
    scissors_png = os.path.join(current_d,'images','scissors.png')
    
    image_settings = [(rock_png, image.NEAREST),(paper_png, image.NEAREST),(scissors_png, image.NEAREST)]
    icons = []

    for image_name, resampling_mode in image_settings:
        icon = image.open(image_name)

        resized_image = icon.resize(cozmo.oled_face.dimensions(), resampling_mode)
        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)

        icons.append(face_image)
    return icons

def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(-5.0)).wait_for_completed()

    cozmo_score = 0 #Both Cozmo and the player start with 0 points
    player_score = 0

    rock = None #Each type of play are represented in the program as objects
    paper = None
    scissors = None

    icons = image_preparation()

    print('Rock, Paper, Scissors for Cozmo! - Cachipun para Cozmo!')
    print('The first to get 5 points wins! - El primero en obtener 5 puntos gana!')
    #Establish Rock - Establecer Piedra
    print('Show me Rock - Muestrame Piedra')
    rock = robot.world.wait_for_observed_light_cube()
    print('Rock found! - Piedra encontrada!')
    #Wait in order to not crash anything
    time.sleep(5)

    #Establish Rock - Establecer Piedra
    print('Show me Paper - Muestrame Papel')
    paper = robot.world.wait_for_observed_light_cube()
    print('Paper found! - Papel encontrado!')
    #Wait in order to not crash anything
    time.sleep(5)

    #Establish Rock - Establecer Piedra
    print('Show me Scissors - Muestrame Tijeras')
    scissors = robot.world.wait_for_observed_light_cube()
    print('Scissors found! - Tijeras encontradas!')
    #Wait in order to not crash anything
    time.sleep(5)

    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE)

    '''
    The game will run as long as the score requirement hasn't met
    El juego correra indefinidamente, a menos que se cumpla el requisito de puntaje
    '''
    while cozmo_score < 5 and player_score < 5:
        #let's make Cozmo choose a play - Hagamos que Cozmo elija una jugada
        cozmo_choice = randint(0,2)
        '''
        0: Rock - Piedra
        1: Paper - Papel
        2: Scissors - Tijeras
        '''

        player_choice = None

        rock.last_tapped_time = None
        paper.last_tapped_time = None
        scissors.last_tapped_time = None
        
        #print(cozmo_choice) #This is cheating! - Esto es hacer trampa!

        while player_choice == None:
            print('Waiting for input - Esperando entrada')
            time.sleep(1)
            if rock.last_tapped_time != None:
                #print('rock')
                player_choice = 0
            elif paper.last_tapped_time != None:
                #print('paper')
                player_choice = 1
            elif scissors.last_tapped_time != None:
                #print('scissors')
                player_choice = 2

        #print(player_choice)
        #print(cozmo_choice)

        if cozmo_choice == 0: #Cozmo chooses Rock - Cozmo elije Piedra
            robot.display_oled_face_image(icons[0], 1000).wait_for_completed()

            if player_choice == 0:
                print('Tie - Empate')
            elif player_choice == 1:
                print('Cozmo loses - Cozmo pierde')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                player_score += 1
            elif player_choice == 2:
                print('Cozmo wins - Cozmo gana')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                cozmo_score += 1

        elif cozmo_choice == 1: #Cozmo chooses Paper - Cozmo elije Papel
            robot.display_oled_face_image(icons[1], 1000).wait_for_completed()
            
            if player_choice == 0:
                print('Cozmo wins - Cozmo gana')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                cozmo_score += 1
            elif player_choice == 1:
                print('Tie - Empate')
            elif player_choice == 2:
                print('Cozmo loses - Cozmo pierde')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                player_score += 1

        elif cozmo_choice == 2: #Cozmo chooses Scissors - Cozmo elije Tijeras
            robot.display_oled_face_image(icons[2], 1000).wait_for_completed()
            
            if player_choice == 0:
                print('Cozmo loses - Cozmo pierde')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                player_score += 1
            elif player_choice == 1:
                print('Cozmo wins - Cozmo gana')
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                cozmo_score += 1
            elif player_choice == 2:
                print('Tie - Empate')

        print('Scores - Puntajes')
        print('Cozmo:', cozmo_score, '- Player:', player_score)

    if cozmo_score > player_score:
        print('Cozmo wins the game! - Cozmo gana la partida!')
        robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
    elif cozmo_score < player_score:
        print('The player wins the game! - El jugador gana la partida!')
        robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()

    return 0

cozmo.run_program(cozmo_program)