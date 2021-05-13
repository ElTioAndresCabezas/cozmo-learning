import cozmo
import asyncio
import time
from cozmo.util import degrees


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
    
    cube1 = None
    cube2 = None
    cube3 = None
    
    #Let's find cube1
    print("Put Cube1 in front of me please!")
    cube1 = robot.world.wait_for_observed_light_cube()
    print("Cube1 found!")
    
    cube1.start_light_chaser()
    time.sleep(10)

    #Let's find cube2
    print("Put Cube2 in front of me please!")
    cube2 = robot.world.wait_for_observed_light_cube()
    print("Cube2 found!")

    cube2.start_light_chaser()
    time.sleep(10)

    #Let's find cube3
    print("Put Cube3 in front of me please!")
    cube3 = robot.world.wait_for_observed_light_cube()
    print("Cube3 found!")

    cube3.start_light_chaser()
    time.sleep(10)

    #You will be asked to tap all the cubes in order
    print("Tap Cube1")
    cube1.wait_for_tap()
    cube1.stop_light_chaser()

    print("Tap Cube2")
    cube2.wait_for_tap()
    cube2.stop_light_chaser()

    print("Tap Cube3")
    cube3.wait_for_tap()
    cube3.stop_light_chaser()
    
    print("You are all set!")

    return 0

cozmo.run_program(cozmo_program)