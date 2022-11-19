import pyautogui
from PIL import Image, ImageDraw
import cv2

from properties import *

dsWidth = 256
dsHeight = 192

def getScreenshot(mainScreen=True) -> Image:
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region=properties.mainScreen if mainScreen else properties.subScreen)
    size = screenshot.size
    scale = properties.mainScreenScale if mainScreen else\
        properties.subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize( ( int(size[0] / scale), 
        int(size[1] / scale) ), Image.NEAREST)
    return screenshot
def localToGlobalPosition(position, mainScreen=True) -> tuple:
    # Converts a position on the subscreen to a position on the total screen. 
    scale = properties.mainScreenScale if mainScreen else\
        properties.subScreenScale
    offset = properties.mainScreen if mainScreen else\
        properties.subScreen
    return (
        ( position[0] * scale ) + offset[0],
        ( position[1] * scale ) + offset[1]
    )