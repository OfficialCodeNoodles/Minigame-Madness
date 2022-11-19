import time
import sys

from image import * 

gameScripts = [ "Wanted", "Sort_or_Splode", "Bobomb_Squad", "Memory_Master" ]
gameNames = [ "Wanted", "Sort or 'Splode", "Bob-omb Squad", "Memory Master" ]
gameScriptIndex = 1

def loadApplication():
    properties.loadFile()
    # This failsafe isn't neccesary as I have built one in already. 
    pyautogui.FAILSAFE = False

if __name__ == "__main__":
    try:
        loadApplication()

        sys.path.append("./scripts/Minigames")

        # Loads required Python scripts. 
        for script in gameScripts:
            exec(f"import {script}")
    except Exception as exception:
        print(exception)
        exit()

    # Confirmation box to start the program. 
    buttonSelected = pyautogui.confirm(
        "Select a minigame to have the program play.",
        title="Minigame Madness", 
        buttons=gameNames + ["Cancel"]
    )
    
    if buttonSelected == "Cancel" or buttonSelected is None:
        exit()
    else:
        gameScriptIndex = gameNames.index(buttonSelected)

    applicationClosed = False
    gameScript = gameScripts[gameScriptIndex]

    eval(f"{gameScript}.setup()") 

    while not applicationClosed:
        # Amount of time in seconds required for each frame. 
        frameDuration = 1.0 / eval(f"{gameScript}.refreshRate")

        startTime = time.time() 

        eval(f"{gameScript}.update()")

        endTime = time.time() 
        difference = endTime - startTime
        time.sleep(max(frameDuration - difference, 0))

        # Emergency exits the program when the mouse is in the top left corner. 
        mousex, mousey = pyautogui.position()
        applicationClosed = mousex + mousey == 0        