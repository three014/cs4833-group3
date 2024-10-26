from mySerCommLibrary import *
import random

initSerComm(9600)

startTime = int(time.time())
endTime = int(time.time())

while endTime - startTime < 120:
  
  distance = int(readSonicCM(3)[1:])

  if distance == None:
    continue

  distanceOne = distance

  if distanceOne > 5:
    moveForward(20)
    continue
  else:
    while distance < distanceOne+5:
      distance = int(readSonicCM(3)[1:])
      moveBack(20)
    
    sleepTime = random.uniform(0.1, 2.5)
    choice = random.randint(1, 2)

    if choice == 1:
      turnLeft(20)
      time.sleep(sleepTime)
    elif choice == 2:
      turnRight(20)
      time.sleep(sleepTime)

    endTime = int(time.time())

endProgram()



