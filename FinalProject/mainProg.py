from mySerCommLibrary import *
import random

initSerComm(9600)

startTime = int(time.time())
endTime = int(time.time())

rightSleepTime = 1.2
leftSleepTime = 1
motorPower = 15

currentColor = "none"


while endTime - startTime < 180:
  
  moveForward(motorPower)
  
  tempColor = readColor()

  if tempColor == "Blue":
    break
  
  if (tempColor == "Red" and  currentColor != "Red") or (tempColor == "Yellow" and currentColor != "Yellow"):
    currentColor = tempColor
    print("New current color: " + currentColor)
    motorPower = 7
    time.sleep(.5)
    motorPower = 15
    rightSleepTime = 1.2
    leftSleepTime = 1
  elif tempColor == currentColor and currentColor != "none":
    print("Moving Back")
    moveBack(7)
    time.sleep(.2)
    print("Turning on color: " + currentColor + ", Sleep time: " + str(leftSleepTime))
    turnLeft(motorPower)
    time.sleep(leftSleepTime)
    if (currentColor == "Yellow" or currentColor == "Red") and leftSleepTime < 3.0 :
      leftSleepTime += (leftSleepTime * .1)

  distance = readSonicCM(3) 
  if distance < 20:
    print("Turning on distance: " + str(distance))
    turnRight(motorPower)
    time.sleep(rightSleepTime)
    rightSleepTime += (rightSleepTime * .1)

  #TODO: counters for when stuck on a corner



  endTime = int(time.time())

stopMove()
endProgram()



