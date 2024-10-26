#!/usr/bin/python3
import serial # type: ignore
import time
# import brickpi3 # import the BrickPi3 drivers
port = "/dev/ttyUSB0"
ser = None

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

def readSonicCM(port):
    return cmdSend(ser, 6, port)

def readSonicIN(port):
    return cmdSend(ser, 7, port)

def endProgram():
    cmdSend(ser, 8, None)


