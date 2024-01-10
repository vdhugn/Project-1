from random import randint
from tkinter.messagebox import showerror
from tkinter import font
from bst.bstVizualize import *

def createRectangleWithText(canvas, centerX, centerY, width, height, rectangleColor, text, textColor, fontSize):
    canvas.create_rectangle(centerX - width / 2, centerY - height / 2,
                            centerX + width / 2, centerY + height / 2,
                            fill=rectangleColor, width=0)
    canvas.create_text(centerX, centerY,
                       text=text, fill=textColor, font=("Arial " + str(int(fontSize)) + " bold"))


def isInputValid(value) -> bool:
    try:
        value = int(value)
    except ValueError:
        showerror(title="ERROR", message="Invalid input")
        return False
    if value > MAX_VALUE:
        showerror(title="ERROR", message="Input value exceeding max allowed")
        return False
    if value < MIN_VALUE:
        showerror(title="ERROR", message="Input value under min allowed")
        return False
    return True


def onClickInsert(value):
    global rootNode
    values = [val.strip() for val in value.split(',')]
    for val in values:
        if not isInputValid(val):
            return
        val = int(val)
        root_x = WINDOW_WIDTH / 2
        root_y = Y_PADDING
        disableUI()
        rootNode = insertNode(rootNode, val, root_x, root_y, 0, canvas, window)
        sleep(1)
        canvas.delete("all")
        drawTree(rootNode, root_x, root_y, 0, canvas, window)
    enableUI()


def onClickSearch(value):
    if not isInputValid(value):
        return
    value = int(value)
    rootPositionX = WINDOW_WIDTH/2
    rootPositionY = Y_PADDING
    disableUI()
    searchTree(rootNode, value, rootPositionX, rootPositionY, 0, canvas, window)
    sleep(1)
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)   
    enableUI()


def onClickDelete(value):
    global rootNode
    if not isInputValid(value):
        return
    value = int(value)
    rootPositionX = WINDOW_WIDTH/2
    rootPositionY = Y_PADDING
    disableUI()
    rootNode = deleteNode(rootNode, value, rootPositionX, rootPositionY, 0, canvas, window)
    sleep(1)
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)   
    enableUI()


def onClickGenerateRandomTree():
    global rootNode
    rootNode = None
    numberOfInserts = randint(100, 100)
    for x in range(numberOfInserts):
        nodeValue = randint(MIN_VALUE, MAX_VALUE)
        rootNode = insertNodeWithoutAnimation(rootNode, nodeValue, 0)   
    rootPositionX = WINDOW_WIDTH/2
    rootPositionY = Y_PADDING
    canvas.delete("all")
    drawTree(rootNode, rootPositionX, rootPositionY, 0, canvas, window)

def onClickClear():
    global rootNode
    disableUI()
    rootNode = None
    canvas.delete("all")
    enableUI()


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

button_font = font.Font(family="Tektur", size=14, weight="bold")

inputField = Entry(window, font = font.Font(family="Tektur", size=12))
inputField.pack(side=LEFT, expand=1)

generateRandomTreeButton = Button(window, text="Generate Random Tree", font=button_font, 
                                  command=lambda: onClickGenerateRandomTree())
generateRandomTreeButton.pack(side=LEFT, fill=X, expand=1)

insertButton = Button(window, text="Insert", font=button_font, command=lambda: onClickInsert(inputField.get()))
insertButton.pack(side=LEFT, fill=X, expand=1)

deleteButton = Button(window, text="Delete", font=button_font, command=lambda: onClickDelete(inputField.get()))
deleteButton.pack(side=LEFT, fill=X, expand=1)

searchButton = Button(window, text="Search", font=button_font, command=lambda: onClickSearch(inputField.get()))
searchButton.pack(side=LEFT, fill=X, expand=1)

clearButton = Button(window, text="Clear", font=button_font, command=onClickClear)
clearButton.pack(side=LEFT, fill=X, expand=1)

def generate():
    window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + "+100-100")
    window.resizable(True, True)
    window.title("Binary Search Tree")
    window.mainloop()