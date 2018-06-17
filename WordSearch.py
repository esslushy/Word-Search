import random
import numpy as np
from enum import Enum, auto
import codecs
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
    try:
        x = int(input("How wide should it be?\n"))
        y = int(input("How tall should it be?\n"))
        words = input("What words should it contain?(split with a space)\n").split(" ")
        for i in words:
            wordWithDirection.append(Word(i))
        return Params(x, y, wordWithDirection)
    except ValueError:
        print("that's not right. Please use words and/or numbers in the appropiate sections")
        return takeParams()

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
    letters = "abcdefghijklmnopqrstuvwxyz"
    for row in range(0, y):
        for column in range(0, x):
            if playfieldMatrix[row][column] is None:
                playfieldMatrix[row][column] = letters[random.randint(0, 25)]
    return playfieldMatrix

def setValidDirection(arrayWords, x, y):
    newArray = []
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
        newArray.append(i)
    return newArray

def organizeBySize(words):
    normalWords = []
    specialWords = []
    for i in words:
        normalWords.append(i.word)
    normalWords.sort(key = len)
    for i in normalWords:
        specialWords.append(Word(i))
    return specialWords[::-1]

def addWords(searchArea, stepx, stepy, x, y, word, dictionary):#pos for right neg for left reminder y then x
    randRow = random.randrange(0, y)
    randColumn = random.randrange(0, x)
    try:
        for l in range(0, len(word)):
                        #changes which way it moves starts at no move and then step affects 0 = no move
            if dictionary[(randRow+(l*stepy), randColumn+(l*stepx))] is None or dictionary[(randRow+(l*stepy), randColumn+(l*stepx))] is word[l]:
                pass
            else:
                return addWords(searchArea, stepx, stepy, x, y, word, dictionary)
        for l in range(0, len(word)):
            dictionary[(randRow+(l*stepy), randColumn+(l*stepx))]=word[l]
            searchArea[randRow+(l*stepy)][randColumn+(l*stepx)]=word[l]#add to search area    
        return (searchArea, dictionary)        
    except KeyError:#if try to access an area outside possible dictionary rerun function until works (may never work so set rerun to 2000)
        return addWords(searchArea, stepx, stepy, x, y, word, dictionary)
        

def addWordsToSearchArea(searchArea, words, x, y, dictionary):
    values = None
    for word in words:
        if (word.direction is Direction.right):
            values = addWords(searchArea, 1, 0, x, y, word.word, dictionary)
        elif (word.direction is Direction.left):
            values = addWords(searchArea, -1, 0, x, y, word.word, dictionary)
        elif (word.direction is Direction.up):
            values = addWords(searchArea, 0, -1, x, y, word.word, dictionary)
        elif (word.direction is Direction.down):
            values = addWords(searchArea, 0, 1, x, y, word.word, dictionary)
        elif (word.direction is Direction.upRight):
            values = addWords(searchArea, 1, -1, x, y, word.word, dictionary)
        elif (word.direction is Direction.upLeft): 
            values = addWords(searchArea, 1, -1, x, y, word.word, dictionary)
        elif (word.direction is Direction.downRight):
            values = addWords(searchArea, 1, 1, x, y, word.word, dictionary)
        elif (word.direction is Direction.downLeft):
            values = addWords(searchArea, -1, 1, x, y, word.word, dictionary)
        searchArea = values[0]
        dictionary = values[1]
    return searchArea

def makeDictForArea(x, y):
    tempDict= {}
    for y1 in range (0, y):
        for x1 in range (0, x):
            tempDict[(y1,x1)] = None
    return tempDict   
#start of the program
random.seed()
params = Params(0, 0, None)
useFile = input("Are you using a config file? y/n: ") == "y"
if(useFile):
    print("Please make sure your file is setup correctly: Each value split by a space and the first value relates to the x-width and the second value relating to the y-height which are both integers. The rest of the values are words and there can be any amount, but keep in mind too many words will break the board.")
    fileName = input("What is the name of your config file. Note: please include the extension ex: .txt\n")
    data  = codecs.open(fileName, "r", "utf-8").read().split()#get file data
    fancyWords = []
    for x in data[2:]:
        fancyWords.append(Word(x))
    params = Params(int(data[0]), int(data[1]), fancyWords)#set params
else:
    params = takeParams()
if(checkIfWordsValid(params.words, params.x, params.y)):
    searchArea = setupSearchArea(params.x, params.y)#index by going y coord x coord
    params.words = organizeBySize(params.words)#largest to smallest
    params.words = setValidDirection(params.words, params.x, params.y)
    #final steps
    checkingDict = makeDictForArea(params.x, params.y)#index y,x like the array in a tuple
    searchArea = addWordsToSearchArea(searchArea, params.words, params.x, params.y, checkingDict)
    searchArea = setRandomLetters(searchArea, params.x, params.y)#set all open spots to random letters
    print(np.matrix(searchArea))
    print("Find these words: ")
    findWords = ""
    for word in params.words:
        findWords += word.word + "  "
    print(findWords)

