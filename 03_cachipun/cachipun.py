#Python script meant to enable Cozmo to play
#Rock, Paper and Scissors
#----------------------------------
#Script de Python para permitir que Cozmo
#juege al cachipun
#----------------------------------
#Developed by / Desarrollado por: Andrés Cabezas
#For IIC1005 class of 2021-1
#Instructed by Professor Denis Parra

import cozmo
import asyncio
import time
from cozmo.util import degrees
from random import randint


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

def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(-5.0)).wait_for_completed()

    rock = None #Each type of play are represented in the program as objects
    paper = None
    scissors = None

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


    while True:
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
        

        while player_choice == None:
            print('Waiting for input - Esperando entrada')
            time.sleep(2)
            if rock.last_tapped_time != None:
                print('rock')
                player_choice = 0
            elif paper.last_tapped_time != None:
                print('paper')
                player_choice = 1
            elif scissors.last_tapped_time != None:
                print('scissors')
                player_choice = 2

        print(player_choice)

        if cozmo_choice == 0: #Cozmo chooses Rock - Cozmo elije Piedra
            if player_choice == 0:
                print('Tie - Empate')
            elif player_choice == 1:
                print('Cozmo loses - Cozmo pierde')
            elif player_choice == 2:
                print('Cozmo wins - Cozmo gana')

        elif cozmo_choice == 1: #Cozmo chooses Paper - Cozmo elije Papel
            if player_choice == 0:
                print('Cozmo wins - Cozmo gana')
            elif player_choice == 1:
                print('Tie - Empate')
            elif player_choice == 2:
                print('Cozmo loses - Cozmo pierde')

        elif cozmo_choice == 2: #Cozmo chooses Scissors - Cozmo elije Tijeras
            if player_choice == 0:
                print('Cozmo loses - Cozmo pierde')
            elif player_choice == 1:
                print('Cozmo wins - Cozmo gana')
            elif player_choice == 2:
                print('Tie - Empate')



    return 0

cozmo.run_program(cozmo_program)