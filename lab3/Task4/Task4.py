#!/usr/bin/python3
import serial # type: ignore
import time
import brickpi3 # import the BrickPi3 drivers


# make use the port is correct
port = "/dev/ttyUSB0"
# we use baudrate 9600 by default and you can change it
# if you change the baudrate, make sure you conduct the same change on your controller
ser = serial.Serial(port, baudrate=9600, timeout=1)

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.

# Configure for an EV3 color sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_COLOR_COLOR specifies that the sensor will be an ev3 color sensor.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

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
            

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
# now 
while(True):
    # ack = cmdSend(ser, 4)
    # # check the output we get from the controller
    # ack = ack[1:]
    # print(ack)

    try:
      color_num = BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError as error:
      print(error)

    if color[color_num] == "Green":
        cmdSend(ser, 2)
    if color[color_num] == "Black":
        cmdSend(ser, 3)
    if color[color_num] == "White":
        cmdSend(ser, 5)


