import random
import numpy as np
from enum import Enum, auto
class Params:
    def __init__(self, x, y, words):
        self.x =x
        self.y = y
        self.words = words

class Word:
    def __init__(self, word):
        self.word = word
        self.direction = None#to be set later to a certain direction

class Direction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()
    upLeft = auto()
    upRight = auto()
    downLeft = auto()
    downRight = auto()

def takeParams():
    wordWithDirection = []
    x = int(input("How wide should it be?\n"))
    y = int(input("How tall should it be?\n"))
    words = input("What words should it contain?(split with a space)\n").split(" ")
    for i in words:
        wordWithDirection.append(Word(i))
    return Params(x,y, wordWithDirection)

def makeXArray(x):
    array = []
    for _ in range(0, x):
        array.append(None)
    return array

def setupSearchArea(x, y):
    yArray = []
    for _ in range(0, y):
        yArray.append(makeXArray(x))
    return yArray

def checkIfWordsValid(wordArray, x, y):
    for i in wordArray:
        if len(i.word) > x:
            if len(i.word) > y:
                print(i.word + " is too long")
                return False
    return True

def setRandomLetters(playfieldMatrix, x, y):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for row in range(0, y):
        for column in range(0, x):
            if playfieldMatrix[row][column] is None:
                playfieldMatrix[row][column] = letters[random.randint(0, 25)]
    return playfieldMatrix

def setValidDirection(arrayWords, x, y):
    verticalOnlyFit = (Direction.up, Direction.down)
    horizontalOnlyFit = (Direction.left, Direction.right)
    allFit = (Direction.left, Direction.right, Direction.up, Direction.down, Direction.upLeft, Direction.upRight, Direction.downLeft, Direction.downRight)
    for i in arrayWords:
        if len(i.word) > x:
            i.direction = verticalOnlyFit[random.randint(0, 1)]
        elif len(i.word) > y:
            i.direction = horizontalOnlyFit[random.randint(0, 1)]
        else:
            i.direction = allFit[random.randint(0, 7)]
    return arrayWords

def organizeBySize(words):
    normalWords = []
    specialWords = []
    for i in words:
        normalWords.append(i.word)
    normalWords.sort(key = len)
    for i in normalWords:
        specialWords.append(Word(i))
    return specialWords[::-1]

def horizontalMove(searchArea, movePosition, x, y):#pos for right neg for left reminder y then x
    randRow = random.randrange(0, y)
    randColumn = random.randrange(0, x)
    
    return searchArea

def addWordsToSearchArea(searchArea, words, x, y, dictionary):
    for word in words:
        if (word.direction is Direction.right):
            searchArea = horizontalMove(searchArea, 1, x, y)
        elif (word.direction is Direction.left):
            searchArea = horizontalMove(searchArea, -1, x, y)
        elif (word.direction is Direction.up):
            x = None
        elif (word.direction is Direction.down):
            x = None
        elif (word.direction is Direction.upRight):
            x = None
        elif (word.direction is Direction.upLeft):
            x = None
        elif (word.direction is Direction.downRight):
            x = None
        elif (word.direction is Direction.downLeft):
            x = None
    return searchArea

def makeDictForArea(x, y):
    tempDict= {}
    for y1 in range (0, y):
        for x1 in range (0, x):
            tempDict[y1,x1] = None
    return tempDict


random.seed()
params = takeParams()
if(checkIfWordsValid(params.words, params.x, params.y)):
    searchArea = setupSearchArea(params.x, params.y)#index by going y coord x coord
    params.words = setValidDirection(params.words, params.x, params.y)
    params.words = organizeBySize(params.words)#largest to smallest
    #create dictionary to store what areas are open/what letters they have made by [y, x] index and then returns space
    openAreasDict = makeDictForArea(params.x, params.y)
    #final steps
    searchArea = setRandomLetters(searchArea, params.x, params.y)
    print(openAreasDict)
