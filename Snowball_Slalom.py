import time
import math
import random

from image import *

refreshRate = 4

playAgainTexture = None
activeAttempt = False
restartTime = 0
restarted = False
furthestDistance = 0
currentDistance = 0 
prvsDistance = 0 
timeStuck = 0
bestAttempt = []
currentAttempt = []
nextAttemptQueue = []
timeAfterAttemptQueue = 0

def setup():
    global playAgainTexture
    playAgainTexture = Image.open("assets/Play Again.png")
    pyautogui.MINIMUM_DURATION = 0
def update():
    global activeAttempt, restartTime, restarted, furthestDistance, currentDistance,\
        prvsDistance, timeStuck, bestAttempt, currentAttempt, nextAttemptQueue,\
        timeAfterAttemptQueue

    subScreen = getScreenshot(mainScreen=False)

    if not activeAttempt:
        playAgainBounds = pyautogui.locate(playAgainTexture, subScreen, confidence=0.75)

        # Resets the attempt if the Play Again button is located. 
        if playAgainBounds is not None:
            boundCenter = pyautogui.center(playAgainBounds)
            playAgainPosition = localToGlobalPosition(boundCenter, mainScreen=False)

            time.sleep(1.0)
            pyautogui.moveTo(playAgainPosition[0], playAgainPosition[1])
            pyautogui.drag(0, 1, 0.2)
            activeAttempt = True
            restarted = False
            restartTime = time.time()
            currentDistance = 0
            prvsDistance = 0 
            timeStuck = 0 
            currentAttempt = []
            timeAfterAttemptQueue = 0 
    else:
        if not restarted:
            currentTime = time.time()
            restartDelta = currentTime - restartTime

            # Waits 4 seconds after the Play Again button is clicked before starting.
            if restartDelta > 4:
                restarted = True
        else:
            progressBarBottomPixelPosition = (239, 156)
            currentPixelPosition = tuple(list(progressBarBottomPixelPosition))
            currentPixelColor = subScreen.getpixel(currentPixelPosition)
            currentPixelAverage = (currentPixelColor[0] + currentPixelColor[1] + currentPixelColor[2]) / 3
            
            # Calculates the snowball's current distance. 
            while currentPixelAverage < 220 and currentPixelPosition[1] > 0:
                currentPixelPosition = (currentPixelPosition[0], currentPixelPosition[1] - 1)
                currentPixelColor = subScreen.getpixel(currentPixelPosition)
                currentPixelAverage = (currentPixelColor[0] + currentPixelColor[1] + currentPixelColor[2]) / 3
            
            currentDistance = progressBarBottomPixelPosition[1] - currentPixelPosition[1]
            
            if currentDistance <= prvsDistance:
                timeStuck += 1
            else:
                prvsDistance = currentDistance
                timeStuck = 0

            # Resets the attempt if the snowball gets stuck. 
            if timeStuck >= refreshRate / 2 and currentDistance > 10:
                if currentDistance > furthestDistance or currentDistance * 1.5 < furthestDistance:
                    furthestDistance = currentDistance
                    bestAttempt = currentAttempt[:-(refreshRate+1)]

                activeAttempt = False
                nextAttemptQueue = bestAttempt[:]

            pushAngle = math.pi / 2

            # Move the cursor in a random direction. 
            if furthestDistance > 0:
                if random.randint(0, refreshRate * (5 if timeAfterAttemptQueue >= 1 else 0)) == 0:
                    pushAngle += random.randint(-100, 100) / 50.0

            # Uses the previous attempt if the queue is still loaded. 
            if len(nextAttemptQueue) > 0:
                pushAngle = nextAttemptQueue.pop(0)
            else:
                timeAfterAttemptQueue += 1

            pushVerticalOffset = 0
            pushOrigin = ( dsWidth / 2, dsHeight - pushVerticalOffset)
            pushDistance = dsHeight - pushVerticalOffset
            pushDestination = ( 
                pushOrigin[0] + pushDistance * math.cos(pushAngle),
                pushOrigin[1] + pushDistance * -math.sin(pushAngle)
            )

            # The start of the mouse stroke. 
            globalPushOrigin = localToGlobalPosition(pushOrigin, mainScreen=False)
            # The end of the mouse stroke. 
            globalPushDestination = localToGlobalPosition(pushDestination, mainScreen=False)

            # Move the mouse along the calculated stroke. 
            pyautogui.moveTo(globalPushOrigin[0], globalPushOrigin[1], _pause=False)
            pyautogui.mouseDown(_pause=False)
            pyautogui.moveTo(globalPushDestination[0], globalPushDestination[1], 0.2, _pause=False)
            pyautogui.mouseUp(_pause=False)

            currentAttempt.append(pushAngle)