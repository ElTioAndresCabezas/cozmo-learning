import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):    
    robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
    robot.move_head(1)
    robot.say_text("Hello ai ai see one o o five").wait_for_completed()
    robot.play_anim(name="anim_poked_giggle").wait_for_completed()


    


cozmo.run_program(cozmo_program)