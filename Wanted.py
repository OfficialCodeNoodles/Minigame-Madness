from enum import Enum

from image import *

refreshRate = 2

class Character(Enum):
    Mario = 0
    Luigi = 1 
    Wario = 2
    Yoshi = 3

characterMatch = None
prvsCharacterMatch = None
characterMatchTicks = 0 

characterTextures = []
characterIcons = [] 
characterSubIcons = []

def loadCharacterTextures():
    for character in Character:
        texture = Image.open(f"assets/Wanted/{character.name}.png")
        characterTextures.append(texture)

        icon = Image.open(f"assets/Wanted/{character.name}Icon.png")
        characterIcons.append(icon)
def generateIconSubregions(iconIndex) -> Image:
    iconSize = characterIcons[iconIndex].size

    # Num of columns to split icon into. 
    xSubRegions = 7
    # Num of rows to split icon into. 
    ySubRegions = 7
    subRegionWidth = iconSize[0] / xSubRegions
    subRegionHeight = iconSize[1] / ySubRegions

    for xRegion in range(0, xSubRegions):
        for yRegion in range(ySubRegions):
            # Area of new sub-icon. 
            bounds = (
                xRegion * subRegionWidth, yRegion * subRegionHeight, (xRegion 
                * subRegionWidth) + subRegionWidth, (yRegion * subRegionHeight)
                + subRegionWidth
            )
            yield characterIcons[iconIndex].crop(bounds)
def generateCharacterSubIcons():
    for character in Character:
        subIcons = []
        for subIcon in generateIconSubregions(character.value):
            pixelCount = 0
            emptyPixels = 0

            # Allows for reading color data from each pixel. 
            subIcon = subIcon.convert("RGBA")

            for pixel in Image.Image.getdata(subIcon):
                # Pixel is empty if it's alpha component is zero. 
                if pixel[3] == 0:
                    emptyPixels += 1
                pixelCount += 1
            
            # Adds sub-icon to array if doesn't contain transparent pixels. 
            if emptyPixels == 0:
                subIcons.append(subIcon)
        characterSubIcons.append(subIcons)
def removeDuplicateSubIcons():
    for character1 in Character:
        for character2 in Character:
            # Ensures same characters icons arent compared. 
            if character1.value == character2.value:
                continue
        
            for i, subIcon in enumerate(characterSubIcons[character2.value]):
                iconBounds = pyautogui.locate(subIcon, 
                    characterIcons[character1.value], confidence=0.98)

                # Removes sub-icon if it can be found in a different character.
                if iconBounds is not None:
                    characterSubIcons[character2.value].pop(i)

def setup():
    loadCharacterTextures()
    generateCharacterSubIcons()
    removeDuplicateSubIcons()
def update():
    global characterMatch, prvsCharacterMatch, characterMatchTicks

    mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)

    foundCharacter = None

    # Searches to find the character that is wanted. 
    for character in Character:
        characterBounds = pyautogui.locate(characterTextures[character.value], 
            mainScreen, confidence=0.75)
        
        if characterBounds is not None:
            foundCharacter = character
            characterMatchTicks += 60 / refreshRate
            break
    
    if foundCharacter is None or prvsCharacterMatch != characterMatch:
        characterMatchTicks = 0
        characterMatch = None
    else:
        # Starts icon search after one second. 
        if characterMatchTicks >= 60:
            characterMatch = foundCharacter

    prvsCharacterMatch = characterMatch

    if characterMatch is not None:
        # A box that represents the on screen area of the icon searched for. 
        iconBounds = pyautogui.locate(characterIcons[characterMatch.value], 
            subScreen, confidence=0.9)

        # If the icon is found, press the icon. 
        if iconBounds is not None:
            pressIcon(iconBounds)
        # Otherwise search using small sections of the icon. 
        else:
            for i, subIcon in enumerate(characterSubIcons[characterMatch.value]):
                iconBounds = pyautogui.locate(subIcon, subScreen, confidence=0.98)

                if iconBounds is not None:
                    pressIcon(iconBounds)
                    return

def pressIcon(bounds):
    # Finds center of the icon. 
    iconCenter = pyautogui.center(bounds)
    position = ( 
        ( iconCenter[0] * properties.subScreenScale ) 
            + properties.subScreen[0],                 
        ( iconCenter[1] * properties.subScreenScale ) 
            + properties.subScreen[1]
    )

    # Clicks on the icon. 
    pyautogui.moveTo(position[0], position[1])
    pyautogui.drag(0.0, 1.0, 0.15)