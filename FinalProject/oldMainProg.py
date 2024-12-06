from mySerCommLibrary import *
import random


def resetValues():
  print("RESET")
  global leftTime
  global rightTime
  global leftSleepTime
  global rightSleepTime
  global motorPower
  leftTime = 10
  rightTime = 5
  leftSleepTime = 1
  rightSleepTime = 1.2
  motorPower = 15

initSerComm(9600)

startTime      = int(time.time())
endTime        = int(time.time())

leftTime       = 10
rightTime      = 5
stuckThreshold = 3
rightSleepTime = 1.2
leftSleepTime  = 1
motorPower     = 15

previousTurn = "none"

currentColor = "none"

counters = {
    "Red": 0,
    "Yellow": 0,
    "Green": 0,
    "Black": 0,
    "Blue": 0,
    "none": 0,
  }


while endTime - startTime < 180:
  
  moveForward(motorPower)
  
  tempColor = readColor()

  loopCounter = 0
  while tempColor != currentColor and tempColor != "Black":
    stopMove()
    counters[readColor()] += 1
    loopCounter += 1
    if loopCounter >= 3:
      tempColor = max(counters, key=counters.get)
      counters = counters.fromkeys(counters, 0)
      break


  if tempColor == "Blue":
    break
  
  if (tempColor == "Red" and  currentColor != "Red") or (tempColor == "Yellow" and currentColor != "Yellow") or (tempColor == "Green" and  currentColor != "Green"):
    currentColor = tempColor
    print("New current color: " + currentColor)
    motorPower = 10
    if previousTurn == "Left":
      turnRight(motorPower)
      time.sleep(.2)
    elif previousTurn == "Right":
      turnLeft(motorPower)
      time.sleep(.2)
    resetValues()
    moveForward(motorPower)
    time.sleep(.5)
  elif tempColor == currentColor and currentColor != "none":
    print("Moving Back")
    moveBack(7)
    time.sleep(.2)
    print("Turning on color: " + currentColor + ", Sleep time: " + str(leftSleepTime))
    turnLeft(motorPower)
    time.sleep(leftSleepTime)
    leftTime = int(time.time())
    previousTurn = "Left"
    if (currentColor == "Yellow" or currentColor == "Red") and leftSleepTime < 3.0 :
      leftSleepTime += (leftSleepTime * .1)
    

  distance = readSonicCM(3) 
  if distance < 30 and currentColor != "none":
    print("Turning on distance: " + str(distance))
    turnRight(motorPower)
    time.sleep(rightSleepTime)
    rightTime = int(time.time())
    previousTurn = "Right"
    rightSleepTime += (rightSleepTime * .1)

  if abs(leftTime - rightTime) < stuckThreshold:
    print("STUCK")
    moveBack(motorPower)
    time.sleep(1)
    turnLeft(motorPower)
    time.sleep(leftSleepTime)
    resetValues()

  endTime = int(time.time())

stopMove()
endProgram()



