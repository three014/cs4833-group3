from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

#!/usr/bin/python3
import serial # type: ignore
import time

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

port = "/dev/ttyUSB0"
ser = None
color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

def cmdSend(ser, cmd, param):
    msg = str(cmd) + str(param) + "\n"
    # encode the msg before sending
    ser.write(msg.encode())
    # originally received msg will end with '\r\n'
    ack_origin = ser.readline()
    ack = ack_origin[:-2].decode("utf-8")
    return ack

def initSerComm(baudrate):
    global ser
    ser = serial.Serial(port, baudrate, timeout=1)
    print("*** Press the GREEN button to start the robot ***")
    time.sleep(2)
    while True:
        print("--- Sending out handshaking signal ---")
        ack = cmdSend(ser, 1, 0)

        if not ack:
            print("*** Try again ***")
            print("*** Press the GREEN button to start the robot ***")
        else:
            print("!!! Connected to the robot !!!")
            ser.readall()
            break

def moveForward(power):
    cmdSend(ser, 2, power)

def moveBack(power):
    cmdSend(ser, 3, power)

def turnLeft(power):
    cmdSend(ser, 4, power)

def turnRight(power):
    cmdSend(ser, 5, power)

def stopMove():
    cmdSend(ser, 8, None)

def readSonicCM(port):
    return int(cmdSend(ser, 6, port)[1:])

def readSonicIN(port):
    return int(cmdSend(ser, 7, port)[1:])

def endProgram():
    cmdSend(ser, 9, None)

def readColor():
    try:
        color_num = BP.get_sensor(BP.PORT_1)
        return color[color_num]
    except brickpi3.SensorError as error:
        print(error)
        return color[0]

def touchSensor():
    try:
        r1 = BP.get_sensor(BP.PORT_2)
    except brickpi3.SensorError as error:
        print(error)
        r1 = 0
    return r1

