#!/usr/bin/python3
import serial # type: ignore
import time
# import brickpi3 # import the BrickPi3 drivers
port = "/dev/ttyUSB0"
ser = serial.Serial(port, 9600, timeout=1)

def cmdSend(ser, cmd, param):
    # our msg must append a newline symbol, because that symbol is used for controller to check whether the cmd is fully received
    msg = str(cmd) + str(param) + "\n"

    
    # encode the msg before sending
    ser.write(msg.encode())
    
    # originally received msg will end with '\r\n'
    ack_origin = ser.readline()
    
    # we can skip the last two chars
    # and then decode the msg using utf-8
    ack = ack_origin[:-2].decode("utf-8")
    
    # return the msg we get
    return ack

def initSerComm(baudrate):
    global ser
    ser = serial.Serial(port, baudrate, timeout=1)

def moveForward(power):
    cmdSend(ser, 2, power)

def moveBack(power):
    cmdSend(ser, 3, power)

def turnLeft(power):
    cmdSend(ser, 4, power)

def turnRight(power):
    cmdSend(ser, 5, power)

def readSonicCM(port):
    cmdSend(ser, 6, port)

def readSonicIN(port):
    cmdSend(ser, 7, port)

# let user know what is the next step
print("*** Press the GREEN button to start the robot ***")
# wait 2 seconds to give time to press the button        
time.sleep(2)
# this while loop blocks until we get response from the controller
while True:
    print("--- Sending out handshaking signal ---")
    # ser is the variable name we initialed as a serial.Serial instance, see line 10 in this file
    # cmd is 1, used for checking whether the controller have responded
    ack = cmdSend(ser, 1, 0)

    # not received any msg
    if not ack:
        print("*** Try again ***")
        print("*** Press the GREEN button to start the robot ***")
    
    # received msg
    else:
        print("!!! Connected to the robot !!!")
        
        # clear the serial receive buffer
        ser.readall()

        # we can break this while loop now
        break
