#!/usr/bin/python3
import serial # type: ignore
import time


# make use the port is correct
port = "/dev/ttyUSB0"
# we use baudrate 9600 by default and you can change it
# if you change the baudrate, make sure you conduct the same change on your controller
ser = serial.Serial(port, baudrate=9600, timeout=1)


# since we need to send cmd to the controller multiple times
# we can write a function for convenient use
def cmdSend(ser, cmd):
    # our msg must append a newline symbol, because that symbol is used for controller to check whether the cmd is fully received
    msg = str(cmd) + "\n"
    
    # encode the msg before sending
    ser.write(msg.encode())
    
    # originally received msg will end with '\r\n'
    ack_origin = ser.readline()
    
    # we can skip the last two chars
    # and then decode the msg using utf-8
    ack = ack_origin[:-2].decode("utf-8")
    
    # return the msg we get
    return ack


# let user know what is the next step
print("*** Press the GREEN button to start the robot ***")

# wait 2 seconds to give time to press the button        
time.sleep(2)

# this while loop blocks until we get response from the controller
while True:
    print("--- Sending out handshaking signal ---")
    # ser is the variable name we initialed as a serial.Serial instance, see line 10 in this file
    # cmd is 1, used for checking whether the controller have responded
    ack = cmdSend(ser, 1)

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
            


# now we can test some cmd code

### Test Case 1 - turn motor left for 1 second and then break the motor

# cmd 2 is turn left cmd
ack = cmdSend(ser, 2)
# check the output we get from the controller
print("you should be able to receive a single digit: 2")
print(ack)

# wait for 1 second and send cmd 5, which is to break the motor
time.sleep(1)
ack = cmdSend(ser, 5)
# check the output we get from the controller
print("you should be able to receive a single digit: 5")
print(ack)


### Test Case 2 - turn motor left for 1 second and then break the motor
### Warning: To test this, make sure your sonic sensor is connected to D3 of the controller

# cmd 4 is read sonic sensor cmd
ack = cmdSend(ser, 4)
# check the output we get from the controller
print("you should be able to receive a single digit: 4 plus a distance")
print(ack)
