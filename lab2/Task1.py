#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running all motors while a touch sensor connected to PORT_1 of the BrickPi3 is being pressed.
# 
# Hardware: Connect EV3 or NXT motor(s) to any of the BrickPi3 motor ports. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.

try:
    print("Press touch sensor on port 2 to run motors")
    r1 = 0
    prev_r1 = 0
    while not r1:
        try:
            r1 = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            pass
    
    button_status = 0
    button_press = 0
    speed = 0
    while True:
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_2 specifies that we are looking for the value of sensor port 2.
        # BP.get_sensor returns the sensor value.
        try:
            r1 = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError as error:
            print(error)
            r1 = 0

        if r1 == prev_r1:
           continue

        if r1 == 1:
	    if speed == 50:
	        speed = 0
	    else:
	        speed = 50

        BP.set_motor_power(BP.PORT_A, speed)
        prev_r1 = r1
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder A: %6d" % BP.get_motor_encoder(BP.PORT_A))
        except IOError as error:
            print(error)
        
        time.sleep(0.1)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
