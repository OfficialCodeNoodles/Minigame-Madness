from enum import Enum
import time

from image import *

refreshRate = 10

class Card(Enum):
    Unknown = 0 
    Mushroom = 1
    Star = 2 
    Cloud = 3
    Flower = 4
    Luigi = 5
    Mario = 6
    Goomba = 7
    Bowser = 8
    Boo = 9
    Yoshi = 10

cardTextures = [] 

cards = []
newCardTicks = 0

def emptyCards(cards) -> bool:
    for card in cards:
        if card[1] is not Card.Unknown:
            return False
    return True
def combineCards(newCards):
    global cards, newCardTicks

    if (cards == [] and len(newCards) >= 16 and len(newCards) % 2 == 0) or\
            (len(newCards) > len(cards) and len(newCards) % 2 == 0):
        cards = newCards.copy()
        newCardTicks = 0 
    elif cards != [] and len(cards) == len(newCards):
        for i, newCard in enumerate(newCards):
            newCardValue = newCard[1].value

            if newCardValue > cards[i][1].value:
                cards[i] = newCard
    elif len(newCards) == 0:
        cards = [] 
def locateCardPair(cards) -> list:
    for i, card0 in enumerate(cards):
        for j, card1 in enumerate(cards):
            if i == j:
                continue
            
            # Finds if cards are the same. 
            if card0[1] != Card.Unknown and card0[1] == card1[1]:
                # Flips cards to make card higher in array appear first.
                return ( i, j ) if i > j else ( j, i )
            
    return None
def sortCards(cards) -> list:
    # Creates a hash value that increases as the position approaches the top 
    # right corner. 
    def positionHash(position) -> int:
        return position[0] + (-position[1] * 3)

    i = 1
    while i < len(cards):
        # Reorders cards so higher hashes are later in array. 
        if positionHash(cards[i][0]) < positionHash(cards[i-1][0]):
            cards[i], cards[i-1] = cards[i-1], cards[i]
            i = 0 
        i += 1
    
    return cards

def setup():
    for cardIndex in range(11):
        cardTexture = Image.open(f"assets/Memory Master/Card{cardIndex}.png")
        cardTextures.append(cardTexture)
def update():
    global cards, newCardTicks

    #mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)

    newCards = [] 

    for i, cardTexture in enumerate(cardTextures):
        for card in pyautogui.locateAll(cardTexture, subScreen, 
                confidence=0.8 if i > 0 else 0.95):
            cardCenter = pyautogui.center(card)
            match = False

            # Removes cards that are duplicates. Note: I added this because for
            # some reason some cards get put in twice. 
            for addedCard in newCards:
                deltax = abs(addedCard[0][0] - cardCenter[0])
                deltay = abs(addedCard[0][1] - cardCenter[1])

                if deltax + deltay < 5:
                    match = True
                    break
            
            if not match:
                newCards.append(( cardCenter, list(Card)[i] ))

    newCards = sortCards(newCards)
    combineCards(newCards)
  
    cardPair = locateCardPair(cards) 

    newCardTicks += 60 / refreshRate

    # Waits to run program until cards have been fully placed. 
    if newCardTicks < 180:
        return

    if cardPair is not None:
        time.sleep(0.5)

        # Clicks on a pair of cards if a match is found. 
        for index in cardPair:
            cardPosition = cards[index][0]
            cardPosition = localToGlobalPosition(cardPosition, 
                mainScreen=False)
                
            pyautogui.moveTo(cardPosition[0], cardPosition[1])
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        # Removes cards from array after they have been pressed. 
        for index in cardPair:
            cards.pop(index)

        time.sleep(1)
    else:
        for card in cards:
            # Clicks on random card if no matches have been located. 
            if card[1] is Card.Unknown: 
                cardPosition = card[0]
                cardPosition = localToGlobalPosition(cardPosition, 
                    mainScreen=False)

                pyautogui.moveTo(cardPosition[0], cardPosition[1])
                pyautogui.mouseDown()
                pyautogui.mouseUp()

                pyautogui.moveTo(1, 1)
                time.sleep(0.5)
                break