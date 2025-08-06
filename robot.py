from sbot import arduino, motors, utils

### "is_competition" in metadata.json started true
### left motor is 1, right is 0

""" rough plan
1. get to wall
2. the hard turns
3. the easy turns (and it's basically the same as the initial getting to the wall anyway)
"""

#CONSTANTS - have no clue yet for any of these values really. also do we need right and back sensors?
MIN_FRONT, MAX_FRONT = 350, 400
MIN_LEFT, MAX_LEFT = 200, 300
MIN_SPEED_L, MIN_SPEED_R = 0.05, 0.05
K = 0.1

#GLOBAL VARS - defaults can be -1
actual_front = -1
actual_left = -1  #left-front
# actual_left_2 = -1 
error_front = actual_front - MIN_FRONT
error_left = actual_left - MIN_LEFT


#MOVEMENT METHODS
def set_motors(left, right):
    motors.set_power(0, left)
    motors.set_power(1, right)

def proportional_control(error):
    left_motor_speed = MIN_SPEED_L - (K*error)
    right_motor_speed = MIN_SPEED_R + (K*error)
    return (left_motor_speed, right_motor_speed)

# def get_to_wall(): #initial getting to the wall from starting position
#     global actual_front

#     # motor_speed_tuple = proportional_control(error_left)
#     # left_motor_speed = motor_speed_tuple[0]
#     # right_motor_speed = motor_speed_tuple[1]

#     set_motors(0, 0.28) #turn 90 degrees left on the spot
#     utils.sleep(1)

#     actual_front = arduino.measure_ultrasound_distance(2, 3)
#     while actual_front >= MIN_LEFT:
#         set_motors(MIN_SPEED_L, MIN_SPEED_R)
#         utils.sleep(1) #dont know how long to set the arg in sleep() to yet
#         actual_front = arduino.measure_ultrasound_distance(2, 3)
        
#     turn_right()
#     return
  
def turn_right():  #for the easy turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(MIN_SPEED_L+0.28, MIN_SPEED_R) #turn right
    utils.sleep(0.5) 
    return
        
def turn_left():   #for the hard turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(MIN_SPEED_L, MIN_SPEED_R+0.28) #turn right
    utils.sleep(0.5)
    return

    
     

#GET TO WALL
actual_front = arduino.measure_ultrasound_distance(2, 3)
actual_left = arduino.measure_ultrasound_distance(4, 5)
error_front = actual_front - MIN_FRONT
error_left = actual_left - MIN_LEFT

motor_speed_tuple = proportional_control(error_left)
left_motor_speed = motor_speed_tuple[0]
right_motor_speed = motor_speed_tuple[1]
get_to_wall() 

#MAIN LOOP AFTER THAT
while True:
    actual_front = arduino.measure_ultrasound_distance(2, 3)
    actual_left = arduino.measure_ultrasound_distance(4, 5)
    error_front = actual_front - MIN_FRONT
    error_left = actual_left - MIN_LEFT

    motor_speed_tuple = proportional_control(error_left)
    left_motor_speed = motor_speed_tuple[0]
    right_motor_speed = motor_speed_tuple[1]
    
    set_motors(left_motor_speed, right_motor_speed) 
    
    #CHECK FOR TURNS
    #1. closed-off turn
    if (MIN_LEFT-25) <= actual_front <= (MIN_LEFT+25) and (MIN_LEFT-25) <= actual_left <= (MIN_LEFT+25): #is 25 too precise for ultrasound? probably
        turn_right()
    #2. more open turn
    elif actual_left <= 200: #high risk of hitting cans on turn 2 and 7 
        turn_left()
    

    






    


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