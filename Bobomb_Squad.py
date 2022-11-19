import math

from image import *

refreshRate = 10

bombTextures = []
cannonBallTexture = None
cloudTextures = [] 

bombs = [] 
cannonBallPosition = None

def calculateBombHeight(bomb) -> int:
    # Finds how far down the screen a bob-omb is (in pixels). 
    height = bomb[0][1]
    # Adds the height of the screen if on the subscreen. 
    if bomb[1] == 1:
        height += dsHeight
    return height

def setup():
    global cannonBallTexture

    bombTexture = Image.open("assets/Bob-omb Squad/Bomb.png")
    bombTextures.append(bombTexture)

    # Generates rotated images to use for image recognition. 
    for angle in range(20, 60, 5):
        # Rotates image in both directions. 
        rightTurn = bombTexture.rotate(angle, Image.NEAREST)
        leftTurn = bombTexture.rotate(-angle, Image.NEAREST)

        # Crops images towards the center to remove transparent pixels when
        # rotating. 
        rightTurn = rightTurn.crop((2, 2, 8, 8))
        leftTurn = leftTurn.crop((2, 2, 8, 8))
 
        bombTextures.append(rightTurn)
        bombTextures.append(leftTurn)
    
    cannonBallTexture = Image.open("assets/Bob-omb Squad/CannonBall.png")
def update():
    global cannonBallTexture, bombs, cannonBallPosition

    mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)
    screens = ( mainScreen, subScreen )

    # Finds the cannon ball before searching for bob-ombs. 
    if cannonBallPosition is None:
        cannonBallBounds = pyautogui.locate(cannonBallTexture, subScreen, 
            confidence=0.9)
        
        # Sets position of cannon ball only if one is located. 
        if cannonBallBounds is not None:
            cannonBallCenter = pyautogui.center(cannonBallBounds)
            cannonBallPosition = ( cannonBallCenter, 1 )
    else:
        bombs = [] 

        # Searches for bob-ombs. 
        for i, screen in enumerate(screens):
            for bombTexture in bombTextures:
                for bomb in pyautogui.locateAll(bombTexture, screen, 
                        confidence=0.9):
                    bombCenter = pyautogui.center(bomb)
                    bombs.append(( bombCenter, i ))

        # If a bob-omb is found then try to shoot it. 
        if bombs != []:
            targetBomb = None
            target = 0 

            farthest = calculateBombHeight(bombs[target])
            
            # Finds which bob-omb is lowest on the screen. 
            for bombIndex in range(1, len(bombs)):
                currentHeight = calculateBombHeight(bombs[bombIndex])

                if currentHeight > farthest:
                    farthest = currentHeight
                    target = bombIndex

            targetBomb = bombs[target]

            # Offset from target bob-omb to cannon ball. 
            deltax = targetBomb[0][0] - cannonBallPosition[0][0]
            deltay = calculateBombHeight(targetBomb) -\
                calculateBombHeight(cannonBallPosition) 

            angle = math.atan2(deltay, deltax)
            
            # Aims ball to move towards the bob-omb if it is higher up. 
            if deltay < 0:
                angle += math.pi

            # Calculates a vector for the cannon ball to hit the bob-omb.
            offsetx = 150 * math.cos(angle) * properties.subScreenScale
            offsety = 150 * math.sin(angle) * properties.subScreenScale

            cannonBallPoint = localToGlobalPosition(cannonBallPosition[0], 
                mainScreen=False)

            pyautogui.moveTo(cannonBallPoint[0], cannonBallPoint[1], 
                _pause=False)
            pyautogui.drag(offsetx, offsety, 0.2, button="left", _pause=False)