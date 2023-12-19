from image import *

refreshRate = 10

montyTexture = None

def setup():
    global montyTexture
    montyTexture = Image.open("assets/Whack a Monty/Monty.png")
def update():
    subScreen = getScreenshot(mainScreen=False)

    locatedMontyBounds = pyautogui.locate(montyTexture, subScreen, confidence=0.85)

    # If a monty is located, then click on it.
    if locatedMontyBounds is not None:
        boundCenter = pyautogui.center(locatedMontyBounds)
        montyPosition = localToGlobalPosition(boundCenter, mainScreen=False)

        pyautogui.moveTo(montyPosition[0], montyPosition[1], _pause=False)
        pyautogui.drag(0, 1, 0.11, _pause=False)