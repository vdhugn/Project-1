from random import randint
from tkinter.messagebox import showerror
from tkinter import font
from bst.bstVizualize import *

def isInputValid(value):
    try:
        value = int(value)
    except ValueError:
        showerror(title="ERROR", message="Invalid input")
        return False
    
    if not (minValue <= value <= maxValue):
        showerror(title="ERROR", message="Input value out of range")
        return False
    return True

def disableUI():
    insertButton["state"] = DISABLED
    generateRandomTreeButton["state"] = DISABLED
    deleteButton["state"] = DISABLED
    searchButton["state"] = DISABLED
    inputField["state"] = DISABLED


def enableUI():
    insertButton["state"] = NORMAL
    generateRandomTreeButton["state"] = NORMAL
    deleteButton["state"] = NORMAL
    searchButton["state"] = NORMAL
    inputField["state"] = NORMAL
    

def InsertButtonClick(value):
    global rootNode
    values = [val.strip() for val in value.split(',')]
    for val in values:
        if not isInputValid(val):
            return
        val = int(val)
        root_x = window_width / 2
        root_y = y_padding
        disableUI()
        rootNode = insertNode(rootNode, val, root_x, root_y, 0, canvas, window)
        sleep(1)
        canvas.delete("all")
        drawTree(rootNode, root_x, root_y, 0, canvas, window)
    enableUI()


def SearchButtonClick(value):
    if not isInputValid(value):
        return
    value = int(value)
    rootPositionX = window_width/2
    rootPositionY = y_padding
    disableUI()
    searchTree(rootNode, value, rootPositionX, rootPositionY, 0, canvas, window)
    sleep(1)
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)   
    enableUI()


def DeleteButtonClick(value):
    global rootNode
    if not isInputValid(value):
        return
    value = int(value)
    rootPositionX = window_width/2
    rootPositionY = y_padding
    disableUI()
    rootNode = deleteNode(rootNode, value, rootPositionX, rootPositionY, 0, canvas, window)
    sleep(1)
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)   
    enableUI()


def GenerateRandomTreeButtonClick():
    global rootNode
    rootNode = None
    numberOfInserts = randint(100, 100)
    for x in range(numberOfInserts):
        nodeValue = randint(minValue, maxValue)
        rootNode = insertNode_(rootNode, nodeValue, 0)   
    rootPositionX = window_width/2
    rootPositionY = y_padding
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)

def ClearButtonClick():
    global rootNode
    disableUI()
    rootNode = None
    canvas.delete("all")
    enableUI()


# SET UP UI
button_font = font.Font(family="Tektur", size=14, weight="bold")

inputField = Entry(window, font = font.Font(family="Tektur", size=12))
inputField.pack(side=LEFT, expand=1)

generateRandomTreeButton = Button(window, text="Generate Random Tree", font=button_font, 
                                  command=lambda: GenerateRandomTreeButtonClick())
generateRandomTreeButton.pack(side=LEFT, fill=X, expand=1)

insertButton = Button(window, text="Insert", font=button_font, command=lambda: InsertButtonClick(inputField.get()))
insertButton.pack(side=LEFT, fill=X, expand=1)

deleteButton = Button(window, text="Delete", font=button_font, command=lambda: DeleteButtonClick(inputField.get()))
deleteButton.pack(side=LEFT, fill=X, expand=1)

searchButton = Button(window, text="Search", font=button_font, command=lambda: SearchButtonClick(inputField.get()))
searchButton.pack(side=LEFT, fill=X, expand=1)

clearButton = Button(window, text="Clear", font=button_font, command=ClearButtonClick)
clearButton.pack(side=LEFT, fill=X, expand=1)

def generate():
    window.geometry(str(window_width) + "x" + str(window_height) + "+100-100")
    window.resizable(True, True)
    window.title("Binary Search Tree")
    window.mainloop()