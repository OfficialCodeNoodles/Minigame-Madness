import math
import random

from image import *

refreshRate = 5

bobombTexture = None
fireballTexture = None
leftEyeTexture = None
bobombLocated = False
bobombPosition = None
leftEyeCenter = 0
timeSinceLastLeftEyeLocation = 0
ticks = 0

def distance(vec1, vec2) -> float:
    return math.sqrt(
        pow(vec1[0] - vec2[0], 2) + pow(vec1[1] - vec2[1], 2)
    )
def generateBobombBounds(screen) -> any:
    bobombBounds = pyautogui.locate(bobombTexture, screen, confidence=0.85)
    return bobombBounds

def setup():
    global bobombTexture, fireballTexture, leftEyeTexture
    bobombTexture = Image.open("assets/Danger, Bob-omb! Danger!/Bob-omb.png")
    fireballTexture = Image.open("assets/Danger, Bob-omb! Danger!/Fireball.png")
    leftEyeTexture = Image.open("assets/Danger, Bob-omb! Danger!/LeftEye.png")
def update():
    global bobombLocated, bobombPosition, ticks, leftEyeCenter, timeSinceLastLeftEyeLocation

    mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)

    # Checks for bob-omb if it hasn't yet been located. 
    if not bobombLocated:
        bobombBounds = generateBobombBounds(subScreen)

        if bobombBounds is not None:
            boundCenter = pyautogui.center(bobombBounds)

            # Grabs the bob-bomb.
            pyautogui.moveTo(boundCenter[0], boundCenter[1], _pause=False)
            pyautogui.mouseDown()
            pyautogui.move(0, 1)

            bobombLocated = True
            bobombPosition = boundCenter
    else:
        # Checks if the bob-omb can still be located, if it can't, then the program stops. 
        if ticks % (refreshRate * 2) == 0:
            bobombBounds = generateBobombBounds(subScreen)

            if bobombBounds is None:
                pyautogui.mouseUp()
                exit()
        
        fireballs = pyautogui.locateAll(fireballTexture, subScreen, confidence=0.75)
        fireballCenters = []
        leftEyeBounds = pyautogui.locate(leftEyeTexture, mainScreen, confidence=0.75)

        if fireballs is not None or leftEyeBounds is not None:
            edgeOffset = 40
            edgeStep = 20

            # Adds fireballs to the edges of the map. 
            for xpos in range(edgeOffset, dsWidth - edgeOffset, edgeStep):
                edgePoint1 = ( xpos, edgeOffset )
                edgePoint2 = ( xpos, dsHeight - edgeOffset )
                fireballCenters.append(edgePoint1)
                fireballCenters.append(edgePoint2)
            for ypos in range(edgeOffset, dsHeight - edgeOffset, edgeStep):
                edgePoint1 = ( edgeOffset, ypos )
                edgePoint2 = ( dsWidth - edgeOffset, ypos )
                fireballCenters.append(edgePoint1)
                fireballCenters.append(edgePoint2)

            if leftEyeBounds is not None:
                timeSinceLastLeftEyeLocation = 0
                boundCenter = pyautogui.center(leftEyeBounds)
                leftEyeCenter = boundCenter[0] + 10
            else: 
                timeSinceLastLeftEyeLocation += 1

            # Adds fireballs where Bowser's fire is. 
            if timeSinceLastLeftEyeLocation < refreshRate * 2:
                for ypos in range(edgeOffset, dsHeight - edgeOffset, edgeStep):
                    edgePoint = ( leftEyeCenter, ypos )
                    fireballCenters.append(edgePoint)

            # Centers all of the normal fireballs. 
            for fireballBounds in fireballs:
                boundCenter = pyautogui.center(fireballBounds)
                fireballCenters.append(boundCenter)

            angleStep = 2
            bestAngle = 0
            bestDistance = 0
            furthestDistance = 0

            # This loop is used to find the best angle/distance pair to move the mouse along. 
            for angle in range(-angleStep, 360, angleStep):
                radians = angle / (180 / math.pi)
                currentDistance = 0 if angle == -angleStep else 3 * (1 + ((angle // angleStep) % 5))
                currentBobombPosition = (
                    bobombPosition[0] + (currentDistance * math.cos(radians)), 
                    bobombPosition[1] + (currentDistance * math.sin(radians))
                )

                closestDistance = dsWidth

                for fireballCenter in fireballCenters:
                    transformedBobombPosition = (
                        currentBobombPosition[0], 
                        currentBobombPosition[1] - 10
                    )
                    bobombFireballDistance = distance(fireballCenter, transformedBobombPosition)
                    closestDistance = min(closestDistance, bobombFireballDistance)

                # Only considers attempts where the shortest fireball distance is larger than the 
                # previous attempts. 
                if closestDistance > furthestDistance:
                    bestAngle = radians
                    bestDistance = currentDistance
                    furthestDistance = closestDistance

            # Calculates the new bob-omb position. 
            bobombPosition = ( 
                bobombPosition[0] + (bestDistance * math.cos(bestAngle)), 
                bobombPosition[1] + (bestDistance * math.sin(bestAngle)) 
            )

        globalBobombPosition = localToGlobalPosition(bobombPosition, mainScreen=False)
        pyautogui.moveTo(globalBobombPosition[0], globalBobombPosition[1])

    ticks += 1