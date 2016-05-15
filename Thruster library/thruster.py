# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import serial
import pygame
from pygame.locals import *
from math import atan
from time import sleep

port = ""     # Used in init() don't change
ser = ""      # Will be defined as a serial port
timeout = 10  # Timeout for communication with Master in seconds

def init(port_val = "COM4", # Change to "/dev/ttyACM0" if on Linux, Name of port used to communicate with Arduino
         ):
    # global port
    # port = port_val
    # global ser
    # ser = serial.Serial(port, timeout = timeout)
    pygame.joystick.init()
    global xbox
    xbox = pygame.joystick.Joystick(0)
    xbox.init()
    screen = pygame.display.set_mode((320, 160))
    pygame.display.set_caption("Thruster")
    # while(not ser.isOpen()): # Waits until port opens
        # pass

# Tests whether is it able to communicate to Xbox controller and both Arduinos
def test():
    # Testing connection to the controller
    if(pygame.joystick.get_count() == 0):
        print("No controller found")
        return
    n = 1
    print("Press the 'start' button!")
    while n:
        for event in pygame.event.get():
            if event.type == JOYBUTTONDOWN:
                if event.button == 7:
                    print("Connection to controller verified")
                    n -= 1

    # Verifying conection to the master Arduino
    ser.write(b'A')
    ser.write(b'A')
    ser.write(b'm')
    ser.write(b'm')
    ser.write(b'E')
    read = ser.read(2)
    if(read == 'mm'):
        print("Conection to master verified")
    else:
        print("Failed to verify connection to master")
        return

def angle(x, y):

    if x == 0:
        if y < 0:
            return 270
        if y > 0:
            return 90
        else:
            return 0

    tan  = y / x
    arctan = atan(tan) / 3.14 * 180

    if x > 0 and y >= 0:
        return arctan
    elif x > 0 and y < 0:
        return arctan + 360
    elif x < 0 and y <= 0:
        return arctan + 180
    elif x < 0 and y > 0:
        arctan + 180

# Code that continiously is being looped through
def main():

    thrusters = [None] * 7
    tForce = [None] * 7

    n = 1
    while(n <= 6):
        thrusters[n] = Thruster(n)
        n += 1

    # Xbox controller button IDs
    a_but = 0
    b_but = 1
    x_but = 2
    y_but = 3
    l_but = 4
    r_but = 5
    back_but = 6
    start_but = 7
    ls_but = 8 # change to 9 if using linux
    rs_but = 9 # change to 10 if using linux

    # Xbox controller axis IDs
    lsx = 0
    lsy = 1
    trig = 2
    rsx = 3
    rsy = 4

    # Xbox controller button values (states)
    a_butVal = 0
    b_butVal = 0
    x_butVal = 0
    y_butVal = 0
    l_butVal = 0
    r_butVal = 0
    back_butVal = 0
    start_butVal = 0
    ls_butVal = 0
    rs_butVal = 0

    # Xbox controller axis values
    lsxVal = 0
    lsyVal = 0
    print(lsyVal)
    trigVal = 0
    rsxVal = 0
    rsyVal = 0

    while True:
        for event in pygame.event.get():
            # Uppon a button press updates values (states) of all buttons
            # Comment out buttons not used
            if event.type == pygame.JOYBUTTONUP:
                a_butVal = xbox.get_button(a_but)
                b_butVal = xbox.get_button(b_but)
                x_butVal = xbox.get_button(x_but)
                y_butVal = xbox.get_button(y_but)
                l_butVal = xbox.get_button(l_but)
                r_butVal = xbox.get_button(r_but)
                back_butVal = xbox.get_button(back_but)
                start_butVal = xbox.get_button(start_but)
                ls_butVal = xbox.get_button(ls_but)
                rs_butVal = xbox.get_button(rs_but)
            # Uppon joystick movement updates values for all joysticks
            if event.type == pygame.JOYAXISMOTION:
                lsxVal = round(xbox.get_axis(lsx)*100, 0)
                lsyVal = round(xbox.get_axis(lsy)*100, 0)*-1
                trigVal = round(xbox.get_axis(trig)*100, 0)
                rsxVal = round(xbox.get_axis(rsx)*100, 0)
                rsyVal = round(xbox.get_axis(rsy)*100, 0)

        # Detects direction of left joystick
        ang = angle(lsxVal, lsyVal)
        if ang >= 45 and ang < 135:
            print('forward')
        elif ang >= 135 and ang < 225:
            print('left')
        elif ang >= 225 and ang < 315:
            print('back')
        elif ang >= 315 or ang < 45:
            print('right')

# Class that defines properties for each individual thruster
class Thruster:
# Function automatically executed upon creation of a thruster object
    def __init__(self,
                 num,# ID of a thruster
                 lb = 1140, # Lower bound of PWM that will be sent to a thruster
                 ub = 1855): # Upper bound of PWM that will be sent to a thruster
        self.num = num
        self.lb = lb
        self.ub = ub

# Function to write values to an ESC through Arduinos
    def write(self, signal):
        ser.write(self.num)
        ser.write(self.num)
        ser.write(signal)
        ser.write(signal)

init()
main()