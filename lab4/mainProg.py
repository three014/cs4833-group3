from mySerCommLibrary import *
import random

initSerComm(9600)

# moveForward(20)
# time.sleep(3)
# moveBack(20)
# time.sleep(3)
# turnLeft(20)
# time.sleep(3)
# turnRight(20)
# time.sleep(3)
# readSonicCM(3)
# time.sleep(3)
# readSonicIN(3)

startTime = time.time

while time.time < startTime+120:

  distance = readSonicCM(3)
  print("First: "+distance)

  if distance == "":
    continue

  distance = int(distance)
  print("Second: "+distance)

  if distance > 5:
    moveForward(20)
    continue
  else:
    while distance < distance+5:
      moveBack(20)
    
    
    sleepTime = random.uniform(0.1, 3.5)
    choice = random.randint(1, 2)

    if choice is 1:
      turnLeft(20)
      time.sleep(sleepTime)
    elif choice is 2:
      turnRight(20)
      time.sleep(sleepTime)



