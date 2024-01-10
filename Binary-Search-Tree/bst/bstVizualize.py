from tkinter import *
from time import sleep
from tkinter.messagebox import showinfo
from bst.constant import *

rootNode = None
window = Tk()
canvas = Canvas(window, bg=BACKGROUND_COLOR)
canvas.pack(side='top', fill='both', expand=2)

class Node:
    def __init__(self, value):
        self.value = value
        self.leftChild = None
        self.rightChild = None

def calculate_left_child_pos(parent_x, parent_y, childDepth):
    leftChild_x = parent_x - ((WINDOW_WIDTH - X_PADDING) / pow(2, childDepth)) / 2
    leftChild_y = parent_y + NODE_RADIUS * 4
    return (leftChild_x, leftChild_y)


def calculate_right_child_pos(parent_x, parent_y, childDepth):
    rightChild_x = parent_x + ((WINDOW_WIDTH - X_PADDING) / pow(2, childDepth)) / 2
    rightChild_y = parent_y + NODE_RADIUS * 4
    return (rightChild_x, rightChild_y)


def insertNode(rootNode, value, root_x, root_y, nodeDepth, canvas, window):
    if nodeDepth > MAX_DEPTH:
        showinfo(title="Insert", message="Max depth reached")
        return rootNode

    if rootNode is None:
        rootNode = Node(value)
        return rootNode
    
    if value < rootNode.value:
        leftChildPositionX, leftChildPositionY = calculate_left_child_pos(root_x, root_y, nodeDepth + 1)
        rootNode.leftChild = insertNode(rootNode.leftChild, value, leftChildPositionX, leftChildPositionY, nodeDepth + 1, canvas, window)
    elif value > rootNode.value:
        rightChildPositionX, rightChildPositionY = calculate_right_child_pos(root_x, root_y, nodeDepth + 1)
        rootNode.rightChild = insertNode(rootNode.rightChild, value, rightChildPositionX, rightChildPositionY,nodeDepth + 1, canvas, window)
    elif value == rootNode.value:
        showinfo(title="Insert", message="Node already in tree")

    return rootNode


def insertNodeWithoutAnimation(rootNode, value, nodeDepth):
    if nodeDepth > MAX_DEPTH:
        return rootNode
    if rootNode is None:
        rootNode = Node(value)
        return rootNode
    if value < rootNode.value:
        rootNode.leftChild = insertNodeWithoutAnimation(rootNode.leftChild, value, nodeDepth + 1)
    elif value > rootNode.value:
        rootNode.rightChild = insertNodeWithoutAnimation(rootNode.rightChild, value, nodeDepth + 1)
    return rootNode


def searchTree(rootNode, value, root_x, root_y, nodeDepth, canvas, window):
    if rootNode is None:
        showinfo(title="Search", message="Node not found")
        return
    
    if value < rootNode.value:
        leftChildPositionX, leftChildPositionY = calculate_left_child_pos(root_x, root_y, nodeDepth + 1)
        canvas.create_line(root_x, root_y, leftChildPositionX, leftChildPositionY, fill="blue", width=5)
        window.update()
        sleep(0.5)
        searchTree(rootNode.leftChild, value, leftChildPositionX, leftChildPositionY, nodeDepth + 1, canvas, window)
    elif value > rootNode.value:
        rightChildPositionX, rightChildPositionY = calculate_right_child_pos(root_x, root_y, nodeDepth + 1)
        canvas.create_line(root_x, root_y, rightChildPositionX, rightChildPositionY, fill="blue", width=5)
        window.update()
        sleep(0.5)
        searchTree(rootNode.rightChild, value, rightChildPositionX, rightChildPositionY,nodeDepth + 1, canvas, window)
    elif value == rootNode.value:
        
        createOvalWithText(canvas, root_x, root_y,
                            NODE_RADIUS, "red",  
                            value, HIGHLIGHT_TEXT_COLOR, FONT_SIZE)
        window.update()
        sleep(2)


def deleteNode(rootNode, value, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode is None:
        showinfo(title="Delete", message="Node not found")
        return None

    if value < rootNode.value:

        leftChildPositionX, leftChildPositionY = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.leftChild = deleteNode(rootNode.leftChild, value, leftChildPositionX, leftChildPositionY, nodeDepth + 1, canvas, window)
    elif value > rootNode.value:
        rightChildPositionX, rightChildPositionY = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.rightChild = deleteNode(rootNode.rightChild, value, rightChildPositionX, rightChildPositionY,nodeDepth + 1, canvas, window)
    elif value == rootNode.value:
        
        if rootNode.leftChild is None and rootNode.rightChild is None:
            return None

        clearCanvasAndDrawTree()

        if rootNode.rightChild is not None:

            rightChildPositionX, rightChildPositionY = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
            rootNode.value = getMinNodeValue(rootNode.rightChild, 
                                         rightChildPositionX, rightChildPositionY, 
                                         nodeDepth + 1, 
                                         canvas, window)
            clearCanvasAndDrawTree()
            rootNode.rightChild = deleteNode(rootNode.rightChild, rootNode.value,
                                             rightChildPositionX, rightChildPositionY,
                                             nodeDepth + 1,
                                             canvas, window)
        else:
            leftChildPositionX, leftChildPositionY = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
            rootNode.value = getMaxNodeValue(rootNode.leftChild, 
                                         leftChildPositionX, leftChildPositionY, 
                                         nodeDepth + 1, 
                                         canvas, window)

            clearCanvasAndDrawTree()

            rootNode.leftChild = deleteNode(rootNode.leftChild, rootNode.value,
                                             leftChildPositionX, leftChildPositionY,
                                             nodeDepth + 1,
                                             canvas, window)
    return rootNode


def getMinNodeValue(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):

    if rootNode.leftChild is None:
        return rootNode.value
    else:
        leftChildPositionX, leftChildPositionY = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        return getMinNodeValue(rootNode.leftChild, leftChildPositionX, leftChildPositionY,  nodeDepth + 1, canvas, window)

    
def getMaxNodeValue(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):

    if rootNode.rightChild is None:
        return rootNode.value
    else:
        rightChildPositionX, rightChildPositionY = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        return getMaxNodeValue(rootNode.rightChild, rightChildPositionX, rightChildPositionY, nodeDepth + 1, canvas, window)

def drawTree(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode is None:
        return

    if rootNode.leftChild is not None:
        leftChildPositionX, leftChildPositionY = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           leftChildPositionX, leftChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(rootNode.leftChild, 
                 leftChildPositionX, leftChildPositionY, 
                 nodeDepth + 1,
                 canvas, window)

    if rootNode.rightChild is not None:
        rightChildPositionX, rightChildPositionY = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,
                           rightChildPositionX, rightChildPositionY, 
                           fill=LINE_COLOR, width=5)
        drawTree(rootNode.rightChild, 
                 rightChildPositionX, rightChildPositionY, 
                 nodeDepth + 1,
                 canvas, window)

    createOvalWithText(canvas, rootPositionX, rootPositionY, 
                     NODE_RADIUS, NODE_COLOR, 
                     rootNode.value, TEXT_COLOR, FONT_SIZE)
    window.update()

def clearCanvasAndDrawTree():
        treePositionX = WINDOW_WIDTH/2
        treePositionY = Y_PADDING
        canvas.delete("all")
        drawTree(rootNode, treePositionX, treePositionY, 0, canvas, window)

def createOvalWithText(canvas, centerX, centerY, radius, ovalColor, text, textColor, fontSize):
    oval = canvas.create_oval(centerX - radius, centerY - radius,
                       centerX + radius, centerY + radius,
                       fill=ovalColor, width=0)
    text = canvas.create_text(centerX, centerY,
                       text=text, fill=textColor, font=("Arial " + str(int(fontSize)) + " bold"))