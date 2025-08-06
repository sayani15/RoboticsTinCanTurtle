# from sbot import arduino, motors, utils

# ### "is_competition" in metadata.json started true
# ### left motor is 1, right is 0
# ### for left 2, trigger 6 echo 7


# #CONSTANTS - have no clue yet for any of these values really. also do we need right and back sensors?
# MIN_FRONT, MAX_FRONT = 350, 400
# MIN_LEFT, MAX_LEFT = 250, 300
# MIN_SPEED_L, MIN_SPEED_R = 0.05, 0.05
# K = 0.00009

# #GLOBAL VARS - defaults can be -1
# # actual_front = -1
# # actual_left = -1  #left-front
# #actual_left_2 = -1 
# # error_front = actual_front - MIN_FRONT
# # error_left = actual_left - MIN_LEFT


# actual_front = arduino.measure_ultrasound_distance(2, 3)
# actual_left = arduino.measure_ultrasound_distance(4, 5)
# error_front = actual_front - MIN_FRONT
# error_left = actual_left - MIN_LEFT

# #MOVEMENT METHODS
# def set_motors(left, right):
#     motors.set_power(0, left)
#     motors.set_power(1, right)

# def proportional_control(error):
#     left_motor_speed = MIN_SPEED_L - (K*error)
#     right_motor_speed = MIN_SPEED_R + (K*error)
#     return (left_motor_speed, right_motor_speed)

  
# def turn_right():  #for the easy turns
#     set_motors(0, 0) #stop
#     utils.sleep(0.5)
#     set_motors(MIN_SPEED_L+0.28, MIN_SPEED_R) #turn right
#     utils.sleep(0.5) 
#     return
        
# def turn_left():   #for the hard turns
#     set_motors(0, 0) #stop
#     utils.sleep(0.5)
#     set_motors(MIN_SPEED_L, MIN_SPEED_R+0.28) #turn right
#     utils.sleep(0.5)
#     return

# set_motors(MIN_SPEED_L, MIN_SPEED_R) 
# utils.sleep(1)

# #MAIN LOOP AFTER THAT
# while True:
#     actual_front = arduino.measure_ultrasound_distance(2, 3)
#     actual_left = arduino.measure_ultrasound_distance(4, 5)
#     error_front = actual_front - MIN_FRONT
#     error_left = actual_left - MIN_LEFT

    
#     motor_speed_tuple = proportional_control(error_left)
#     left_motor_speed = motor_speed_tuple[0]
#     right_motor_speed = motor_speed_tuple[1]
#     print(left_motor_speed, right_motor_speed)
#     set_motors(left_motor_speed, right_motor_speed) 

#     #CHECK FOR TURNS
#     #1. go straight
#     if actual_front < (1120-MIN_LEFT):
#         motor_speed_tuple = proportional_control(error_left)
#         left_motor_speed = motor_speed_tuple[0]
#         right_motor_speed = motor_speed_tuple[1]
#         print("hi")
#         print(left_motor_speed, right_motor_speed)
#         set_motors(left_motor_speed, right_motor_speed) 
#         print("hi")
#     #2. closed turn
#     elif (MIN_LEFT-25) <= actual_front <= (MIN_LEFT+25) and (MIN_LEFT-25) <= actual_left <= (MIN_LEFT+25): #is 25 too precise for ultrasound? probably
#         turn_right()
#     #3. more open turn
#     elif actual_left <= 200: #high risk of hitting cans on turn 2 and 7 
#         turn_left()
      

# #stuff from task 4 to re-use
# # a=True
# # while a:
# #     set_motors(0.2,0.2)

# #     distance_front = arduino.measure_ultrasound_distance(2, 3) #This is the front sensor
# #     if distance_front <= 200:
# #        set_motors(0, 0) #stop
# #        utils.sleep(1)
# #        set_motors(0, 0.28) #turn left

# #        utils.sleep(1)
# #        print("turned right")
# #        print("should end now")
# #        a=False
# #     elif distance_front <= 400 and a == True:
# #        print("distance_front is", distance_front)
# #        set_motors(0, 0) #stop
# #        utils.sleep(1)
# #        set_motors(0.28, 0) #turn right
# #        utils.sleep(1)
# #        print("turned left")




from sbot import arduino, motors, utils
from sbot import leds, Colour
### "is_competition" in metadata.json started true
### left motor is 1, right is 0

#GLOBALS
#constants
MIN_SPEED_L, MIN_SPEED_R = 0.25, 0.22 #have been tested on actual robot
MIN_LEFT_F, MIN_LEFT_B = 180, 180
MIN_FRONT = 180
K = 0 #only used in proportional_control(error)

#vars
actual_front = arduino.measure_ultrasound_distance(2, 3)
actual_left_F = arduino.measure_ultrasound_distance(4, 5)
actual_left_B = arduino.measure_ultrasound_distance(6, 7)
error_left = actual_left_F - MIN_LEFT_F 


#MOVEMENT METHODS
def set_motors(left, right):
    motors.set_power(1, -left)
    motors.set_power(0, -right)

def proportional_control(error):
    left_motor_speed = MIN_SPEED_L - (K*error)
    right_motor_speed = MIN_SPEED_R + (K*error)
    return (left_motor_speed, right_motor_speed)

  
def turn_right():  #for the easy turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(+0.28, 0) #turn right
    utils.sleep(1) #theoretically we can  double speed and half time (and same for turn left)
    return
        
def turn_left():   #for the hard turns
    set_motors(0, 0) #stop
    utils.sleep(0.5)
    set_motors(0, +0.28) #turn left
    utils.sleep(1)
    return

def go_straight(error, t): #whenever it's used proportional_control(error) must be used to generate the values for speed
    speed_tuple = proportional_control(error)
    set_motors(speed_tuple[0], speed_tuple[1])
    utils.sleep(t)



set_motors(MIN_SPEED_L, MIN_SPEED_R)

while True:
    actual_front = arduino.measure_ultrasound_distance(2, 3)
    actual_left_F = arduino.measure_ultrasound_distance(4, 5)
    actual_left_B = arduino.measure_ultrasound_distance(6, 7)
    error_left = actual_left_F - MIN_LEFT_F 

    go_straight()

    #right
    if 150 < actual_left_F < 250 and 150 < actual_front < 250:
        turn_right()
    #left
    if actual_left_F > 1200 and actual_left_B < 450:
        set_motors(MIN_SPEED_L, MIN_SPEED_R) #to clear both left sensors from wall it was just tracing
        utils.sleep(1) #needs testing 
        turn_left()

    #straight
    if actual_left >= 250:
        print(f"actual left ={actual_left}. bigger than 250")
        leds.set_colour(0, Colour.RED)
        set_motors(MIN_SPEED_L, MIN_SPEED_R)
        print("have gone straight")
        utils.sleep(0.5)
    if actual_left < 250:
        print(f"actual left={actual_left}. smaller than 250")
        leds.set_colour(0, Colour.GREEN)
        set_motors(0,0)
        utils.sleep(1.5)
        set_motors(0,0.28) #turn left
        print("have turned left")
        leds.set_colour(0, Colour.BLUE)
        utils.sleep(1.00) #probably time for 90 degree turn
