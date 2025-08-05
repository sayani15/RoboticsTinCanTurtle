# from sbot import *
# from sbot import leds, Colour
# from sbot import arduino
# from sbot import comp
# from sbot import motors, utils
# import numpy
# from sbot import GPIOPinMode

### "is_competition" in metadata.json started true
### left motor is 1, right is 0

from sbot import arduino, motors, utils

#global variables
min_front, max_front = 250, 400 #have no clue yet for any of these values really
min_left, max_left = 200, 300
# min_right, max_right = 200, 400
#min_back - probably not neccessary?

def set_motors(left, right):
    motors.set_power(0, left)
    motors.set_power(1, right)

""" rough plan
1. get to wall
2. the hard turns
3. the easy turns (and it's basically the same as the initial getting to the wall anyway)
"""

#initial getting to the wall from starting position
def get_to_wall(actual_front): #havent decided whether actual values should be parameters or measured in the main loop as global vars?
    set_motors(0, 0.28) #turn 90 degrees left (probably)
    utils.sleep(1)

    actual_front = arduino.measure_ultrasound_distance(2, 3)
    while actual_front >= min_front:
        set_motors(0.25, 0.25)
        utils.sleep(0.5) #dont know how long to set the arg in sleep() to yet
        actual_front = arduino.measure_ultrasound_distance(2, 3)
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(0.28, 0) #turn right



    





    


#stuff from task 4 to re-use
a=True
while a:
    set_motors(0.2,0.2)

    distance_front = arduino.measure_ultrasound_distance(2, 3) #This is the front sensor
    if distance_front <= 200:
       set_motors(0, 0) #stop
       utils.sleep(1)
       set_motors(0, 0.28) #turn left

       utils.sleep(1)
       print("turned right")
       print("should end now")
       a=False
    elif distance_front <= 400 and a == True:
       print("distance_front is", distance_front)
       set_motors(0, 0) #stop
       utils.sleep(1)
       set_motors(0.28, 0) #turn right
       utils.sleep(1)
       print("turned left")

