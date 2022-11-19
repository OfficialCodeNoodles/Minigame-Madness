from enum import Enum
import time
import math

from image import *

refreshRate = 12

class Bomb(Enum):
    Black = 0
    Red = 1

bombTextures = []
bombBoundTextures = [] 
bombBounds = []
bombBoundCenters = []

currentBomb = None

def loadBombTextures():
    for bomb in Bomb:
        bombTexture = Image.open(f"assets/Sort or 'Splode/{bomb.name}Bomb.png")
        bombTextures.append(bombTexture)

        bombBoundTexture = Image.open(
            f"assets/Sort or 'Splode/{bomb.name}BombBounds.png")
        bombBoundTextures.append(bombBoundTexture)
def distance(vec1, vec2) -> float:
    return math.sqrt(
        pow(vec1[0] - vec2[0], 2) + pow(vec1[1] - vec2[1], 2)
    )

def setup():
    loadBombTextures()
def update():
    global currentBomb, refreshRate

    #mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)

    if bombBounds == []:
        blackBombBounds = pyautogui.locate(bombBoundTextures[Bomb.Black.value], 
            subScreen, confidence=0.7)
        redBombBounds = pyautogui.locate(bombBoundTextures[Bomb.Red.value], 
            subScreen, confidence=0.7)
        bounds = ( blackBombBounds, redBombBounds )

        # Only sets the bounds if both the red and black bomb areas are located. 
        if not None in bounds:
            for bound in bounds:
                bombBounds.append(bound)

                boundCenter = pyautogui.center(bound)
                bombBoundCenters.append(boundCenter)
    else:
        drawing = ImageDraw.Draw(subScreen)

        for bound in bombBounds:
            # Draws boxes over the bomb areas to stop them from being located.
            drawing.rectangle((( bound[0], bound[1] ), 
                ( bound[0] + bound[2], bound[1] + bound[3] )), fill=(0, 0, 0))

        currentBomb = None

        for bombColor in Bomb:
            bomb = pyautogui.locate(bombTextures[bombColor.value], subScreen, 
                confidence=0.95)

            # If bomb is located set it to be moved. 
            if bomb is not None:
                bombCenter = pyautogui.center(bomb) 

                dist = 115

                # Finds distance to nearest bomb area. 
                for bound in bombBoundCenters:
                    dist = min(dist, distance(bombCenter, bound))

                # Only continues process if bomb isn't in the spawn area. 
                if dist < 115:
                    currentBomb = ( bombCenter, bombColor )
                    break
            
        # Moves bomb if one is located. 
        if currentBomb is not None:
            bombPosition = localToGlobalPosition(currentBomb[0], 
                mainScreen=False)
            bombBoundCenter = bombBoundCenters[currentBomb[1].value]
            bombBoundPosition = localToGlobalPosition(bombBoundCenter, 
                mainScreen=False)

            pyautogui.moveTo(bombPosition[0], bombPosition[1], _pause=False)
            pyautogui.mouseDown(_pause=False)
            time.sleep(0.04)
            pyautogui.moveTo(bombBoundPosition[0], bombBoundPosition[1], _pause=False)
            time.sleep(0.04)
            pyautogui.mouseUp(_pause=False)