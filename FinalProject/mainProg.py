from mySerCommLibrary import *
import random

class Timer():
  def __init__(self, time):
    self.time = time
    self.start = None
    self.end = None

  def startTimer(self):
    self.start = time.time()
    self.end = self.start + self.time

  def isStarted(self):
    return self.start != None

  def isFinished(self):
    return self.end < time.time()

class StuckCounter():
  def __init__(self, threshold):
    self.lastLeft = None
    self.lastRight = None
    self.threshold = threshold

  def resetStuck(self):
    self.leftLeft = None
    self.lastRight = None

  # Returns whether a right and left turn
  # both occurred within the threshold time
  def isStuck(self):
    if self.lastLeft == None or self.lastRight == None:
      return False
    return abs(self.lastLeft - self.lastRight) < self.threshold

  # Mark the last time we decided to turn left
  def markLeft(self):
    self.lastLeft = time.time()

  # Mark the last time we decided to turn right
  def markRight(self):
    self.lastRight = time.time()

  # Return the last direction we chose to turn,
  # otherwise return None if we have yet to make
  # a choice
  def getLastTurn(self):
    if self.lastLeft == None and self.lastRight == None:
      return None
    if self.lastLeft > self.lastRight:
      return "Left"
    else:
      return "Right"

initSerComm(9600)

startTime = int(time.time())
endTime = int(time.time())

# Using smaller values since now we're constantly
# watching for barriers/borders
rightSleepTime = 0.6
defaultRightSleepTime = rightSleepTime
leftSleepTime = 1.0
defaultleftSleepTime = leftSleepTime
motorPower = 12
backSleepTime = 0.2
defaultBackSleepTime = backSleepTime

# Using an array to represent the border
# colors so that we can keep track 
# of how "far" we are inside the arena.
borderColors = ["none", "White", "Red", "Yellow", "Blue"]
currentColorIdx = 0
currentColor = borderColors[currentColorIdx]

# Timers for deciding which direction
# to move the rover. First direction
# takes precedence over the next direction,
# and so on.
moveBackwardTimer = None
turnLeftTimer = None
turnRightTimer = None
moveForwardTimer = None

# Used to indicate that there's
# nothing else to do but move forward
defaultMoveForward = False

# Keeps track of when we made left
# and right turns in order to 
# figure out when we're stuck
stuckCounter = StuckCounter(1)

counters = {
    "Red": 0,
    "Yellow": 0,
    "White": 0,
    "Brown": 0,
    "Green": 0,
    "Black": 0,
    "Blue": 0,
    "none": 0,
  }

while endTime - startTime < 180:

  # --- Gather information ---

  tempColor = readColor()
  distance = readSonicCM(3)

  # --- Decide what to do ---

  if tempColor == borderColors[currentColorIdx + 1]:
    # Poll check for accurate color
    loopCounter = 0
    while tempColor != currentColor and (tempColor == "Red" or tempColor == "Yellow" or tempColor == "White"):
      print("Found Color: " + tempColor)
      stopMove()
      counters[readColor()] += 1
      loopCounter += 1
      if loopCounter >= 3:
        tempColor = max(counters, key=counters.get)
        print("Common Color: " + tempColor)
        counters = counters.fromkeys(counters, 0)
        moveForward(motorPower)
        break
  # elif tempColor == borderColors[currentColorIdx - 1]:
  #   loopCounter = 0
  #   while tempColor != currentColor and (tempColor == "Red" or tempColor == "Yellow" or tempColor == "White"):
  #     print("Found Previous Color: " + tempColor)
  #     stopMove()
  #     counters[readColor()] += 1
  #     loopCounter += 1
  #     if loopCounter >= 3:
  #       tempColor = max(counters, key=counters.get)
  #       print("Common Previous Color: " + tempColor)
  #       counters = counters.fromkeys(counters, 0)
  #       moveBack(motorPower)
  #       break

  # Stop if we hit blue inside the inner zone
  if tempColor == "Blue" and borderColors[currentColorIdx] == "Yellow":
    print("FOUND DA WATAH MAH LORD")
    break

  # If we entered the next zone, we should turn into
  # the zone, move forward a bit, then update our
  # current color
  if tempColor == borderColors[currentColorIdx + 1]:
    print("New Color: " + tempColor)
    leftSleepTime = defaultleftSleepTime
    time.sleep(.7)

    # If we're inside a border already, then we turn opposite
    # of the last turn we did
    if currentColor != "none":
      lastTurn = stuckCounter.getLastTurn()
      if lastTurn != None and lastTurn == "Right":
        print("Turning Left after New Color: " + tempColor)
        turnLeftTimer = Timer(leftSleepTime)
        turnRightTimer = None
        stuckCounter.markLeft()
      elif lastTurn != None and lastTurn == "Left":
        print("Turning Right after New Color: " + tempColor)
        turnLeftTimer = None
        turnRightTimer = Timer(rightSleepTime)
        stuckCounter.markRight()

    # We then move forward a tiny bit
    moveForwardTimer = Timer(0.2)

    # Update new border colors
    currentColor = borderColors[currentColorIdx + 1]
    currentColorIdx += 1

  # If we hit our current border (and we're actually in 
  # the zone), we turn back into the zone
  elif tempColor == borderColors[currentColorIdx] and currentColorIdx != 0:
    print("Move Back Turning Left Hit Current Color Border: " + tempColor)
    moveBackwardTimer = None
    backSleepTime = defaultBackSleepTime
    if leftSleepTime < defaultleftSleepTime + .5:
      leftSleepTime += .04
    turnLeftTimer = Timer(leftSleepTime)
    turnRightTimer = None
    stuckCounter.markLeft()

  # If we're too close to a wall, we turn away from it
  if distance < 25:
    print("Too Close Turning Right: " + str(distance))
    turnLeftTimer = None
    turnRightTimer = Timer(rightSleepTime)
    stuckCounter.markRight()

  # If we are stuck, then we need to move backwards,
  # then to the left
  if stuckCounter.isStuck():
    print("STUCK STUCK STUCK STUCK")
    if backSleepTime < defaultBackSleepTime + 1:
      backSleepTime += .2
    moveBackwardTimer = Timer(backSleepTime)
    turnLeftTimer = Timer(defaultleftSleepTime)
    turnRightTimer = None
    stuckCounter.resetStuck()

  # --- Take Action ---

  # Steps:
  # For each direction, check if there exists
  # a timer to move in that direction
  # 
  # If a timer exists, then check if we've already
  # started moving in that direction
  # If we haven't, then start moving in that direction!
  #
  # If the timer exists and is finished, 
  # then remove that timer
  if moveBackwardTimer != None:
    if not moveBackwardTimer.isStarted():
      moveBackwardTimer.startTimer()
      moveBack(motorPower)
    elif moveBackwardTimer.isFinished():
      moveBackwardTimer = None
  elif turnLeftTimer != None:
    if not turnLeftTimer.isStarted():
      turnLeftTimer.startTimer()
      turnLeft(motorPower)
    elif turnLeftTimer.isFinished():
      turnLeftTimer = None
  elif turnRightTimer != None:
    if not turnRightTimer.isStarted():
      turnRightTimer.startTimer()
      turnRight(motorPower)
    elif turnRightTimer.isFinished():
      turnRightTimer = None
  elif moveForwardTimer != None:
    if not moveForwardTimer.isStarted():
      moveForwardTimer.startTimer()
      moveForward(motorPower)
    elif moveForwardTimer.isFinished():
      moveForwardTimer = None

  # After all that, we check if there
  # are any timers left. If no more timers
  # available, then we keep moving forward!
  if not (moveBackwardTimer or turnLeftTimer or turnRightTimer or moveForwardTimer):
    print("Default Moving Forward, Current Color: " + currentColor)
    if not defaultMoveForward:
      defaultMoveForward = True
      moveForward(motorPower)
  else:
    defaultMoveForward = False
      
  endTime = int(time.time())

stopMove()
endProgram()
