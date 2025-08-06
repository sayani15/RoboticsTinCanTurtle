from sbot import arduino, motors, utils

### "is_competition" in metadata.json started true
### left motor is 1, right is 0

""" rough plan
1. get to wall
2. the hard turns
3. the easy turns (and it's basically the same as the initial getting to the wall anyway)
"""

#CONSTANTS - have no clue yet for any of these values really. and lol i lowkey forgot how global variables work. also do we need right and back sensors?
MIN_FRONT, MAX_FRONT = 250, 400
MIN_LEFT, MAX_LEFT = 200, 300

#GLOBAL VARS - you cant just initialise stuff in python so their defaults can be -1
actual_front = -1
actual_left_1 = -1  #left-front
actual_left_2 = -1  #left-back - imma use L1 as "left" for most of the code. will solve the problem of the pins tomorrow
error_front = actual_front - MIN_FRONT
error_left = actual_left_1 - MIN_LEFT


#MOVEMENT METHODS
def set_motors(left, right):
    motors.set_power(0, left)
    motors.set_power(1, right)

def get_to_wall(): #initial getting to the wall from starting position
    global actual_front
    set_motors(0, 0.28) #turn 90 degrees left (probably)
    utils.sleep(1)

    actual_front = arduino.measure_ultrasound_distance(2, 3)
    while actual_front >= MIN_LEFT:
        set_motors(0.25, 0.25)
        utils.sleep(0.5) #dont know how long to set the arg in sleep() to yet
        actual_front = arduino.measure_ultrasound_distance(2, 3)
    turn_right()
  
def turn_right():  #aka for the easy turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(0.28, 0) #turn right
    utils.sleep(0.5) 
    return
        
def turn_left():   #aka for the hard turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(0, 0.28) #turn left
    utils.sleep(0.5)
    return

def proportional_control(error_left):
    #left motor speed = min speed -
    #...
    #return a tuple with the motor speeds
    return
    
     

#MAIN LOOP
get_to_wall() #i guess this is outside the main loop lol
while True:
    actual_front = arduino.measure_ultrasound_distance(2, 3)
    actual_left_1, actual_left_2 = arduino.measure_ultrasound_distance(4, 5), arduino.measure_ultrasound_distance(8, 9)
    error_front = actual_front - MIN_FRONT
    error_left = actual_left_1 - MIN_LEFT
    
    set_motors(0.2,0.2) #0.2 are placeholders, in reality this depends on the proportional control

    
    #CHECK FOR TURNS
    #1. closed-off turn
    if (MIN_LEFT-25) <= actual_front <= (MIN_LEFT+25) and (MIN_LEFT-25) <= actual_left_1 <= (MIN_LEFT+25): #is 25 too precise for ultrasound? probably
        turn_right()
    #2. more open turn
    elif actual_left_1 <= 200: #300 seems about right - except oops on turn 2 and 7 this means we'll go straight through the cans. err 200 maybe?
        turn_left()
    #CHECK WE'RE ON TRACK
        
    

    






    


#stuff from task 4 to re-use
# a=True
# while a:
#     set_motors(0.2,0.2)

#     distance_front = arduino.measure_ultrasound_distance(2, 3) #This is the front sensor
#     if distance_front <= 200:
#        set_motors(0, 0) #stop
#        utils.sleep(1)
#        set_motors(0, 0.28) #turn left

#        utils.sleep(1)
#        print("turned right")
#        print("should end now")
#        a=False
#     elif distance_front <= 400 and a == True:
#        print("distance_front is", distance_front)
#        set_motors(0, 0) #stop
#        utils.sleep(1)
#        set_motors(0.28, 0) #turn right
#        utils.sleep(1)
#        print("turned left")