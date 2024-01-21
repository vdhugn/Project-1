from tkinter import *
from time import sleep
from tkinter.messagebox import showinfo
from bst.constant import *

rootNode = None
window = Tk()
canvas = Canvas(window, bg=background_color)
canvas.pack(side='top', fill='both', expand=2)

class Node:
    def __init__(self, value):
        self.value = value
        self.leftChild = None
        self.rightChild = None

def calculate_left_child_pos(parent_x, parent_y, childDepth):
    leftChild_x = parent_x - ((window_width - x_padding) / pow(2, childDepth)) / 2
    leftChild_y = parent_y + node_radius * 4
    return (leftChild_x, leftChild_y)


def calculate_right_child_pos(parent_x, parent_y, childDepth):
    rightChild_x = parent_x + ((window_width - x_padding) / pow(2, childDepth)) / 2
    rightChild_y = parent_y + node_radius * 4
    return (rightChild_x, rightChild_y)

def oval_with_text(canvas, centerX, centerY, radius, ovalColor, text, textColor, fontSize):
    oval = canvas.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius, fill=ovalColor, width=0)
    text = canvas.create_text(centerX, centerY, text=text, fill=textColor, font=("Calibri " + str(int(fontSize)) + " bold"))
    
def insertNode(rootNode, value, root_x, root_y, nodeDepth, canvas, window):
    if nodeDepth > maxDepth:
        showinfo(title="Insert", message="Max depth reached")
        return rootNode

    if rootNode is None:
        rootNode = Node(value)
        return rootNode
    
    if value < rootNode.value:
        leftChild_X, leftChild_Y = calculate_left_child_pos(root_x, root_y, nodeDepth + 1)
        rootNode.leftChild = insertNode(rootNode.leftChild, value, leftChild_X, leftChild_Y, nodeDepth + 1, canvas, window)
    elif value > rootNode.value:
        rightChild_X, rightChild_Y = calculate_right_child_pos(root_x, root_y, nodeDepth + 1)
        rootNode.rightChild = insertNode(rootNode.rightChild, value, rightChild_X, rightChild_Y,nodeDepth + 1, canvas, window)
    elif value == rootNode.value:
        showinfo(title="Insert", message="Node already in the tree")

    return rootNode


def insertNode_(rootNode, value, nodeDepth):
    #insert node without animation
    if nodeDepth > maxDepth:
        return rootNode
    if rootNode is None:
        rootNode = Node(value)
        return rootNode
    if value < rootNode.value:
        rootNode.leftChild = insertNode_(rootNode.leftChild, value, nodeDepth + 1)
    elif value > rootNode.value:
        rootNode.rightChild = insertNode_(rootNode.rightChild, value, nodeDepth + 1)
    return rootNode


def searchTree(rootNode, value, root_x, root_y, nodeDepth, canvas, window):
    if rootNode is None:
        showinfo(title="Search", message="Node not found")
        return
    
    if value < rootNode.value:
        leftChild_X, leftChild_Y = calculate_left_child_pos(root_x, root_y, nodeDepth + 1)
        canvas.create_line(root_x, root_y, leftChild_X, leftChild_Y, fill="blue", width=5)
        window.update()
        sleep(0.5)
        searchTree(rootNode.leftChild, value, leftChild_X, leftChild_Y, nodeDepth + 1, canvas, window)
    elif value > rootNode.value:
        rightChild_X, rightChild_Y = calculate_right_child_pos(root_x, root_y, nodeDepth + 1)
        canvas.create_line(root_x, root_y, rightChild_X, rightChild_Y, fill="blue", width=5)
        window.update()
        sleep(0.5)
        searchTree(rootNode.rightChild, value, rightChild_X, rightChild_Y,nodeDepth + 1, canvas, window)
    elif value == rootNode.value:
        
        oval_with_text(canvas, root_x, root_y,node_radius, "red", value, hightlight_text, font_size)
        window.update()
        sleep(2)


def deleteNode(rootNode, value, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode is None:
        showinfo(title="Delete", message="Node not found")
        return None

    if value < rootNode.value:
        leftChild_X, leftChild_Y = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.leftChild = deleteNode(rootNode.leftChild, value, leftChild_X, leftChild_Y, nodeDepth + 1, canvas, window)

    elif value > rootNode.value:
        rightChild_X, rightChild_Y = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        rootNode.rightChild = deleteNode(rootNode.rightChild, value, rightChild_X, rightChild_Y,nodeDepth + 1, canvas, window)

    elif value == rootNode.value:
        
        if rootNode.leftChild is None and rootNode.rightChild is None:
            return None

        clearAndDrawTree()

        if rootNode.rightChild is not None:
            rightChild_X, rightChild_Y = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
            rootNode.value = getMinNodeValue(rootNode.rightChild, rightChild_X, rightChild_Y, nodeDepth + 1, canvas, window)
            clearAndDrawTree()
            rootNode.rightChild = deleteNode(rootNode.rightChild, rootNode.value,rightChild_X, rightChild_Y,nodeDepth + 1,canvas, window)

        else:
            leftChild_X, leftChild_Y = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
            rootNode.value = getMaxNodeValue(rootNode.leftChild, leftChild_X, leftChild_Y, nodeDepth + 1, canvas, window)

            clearAndDrawTree()

            rootNode.leftChild = deleteNode(rootNode.leftChild, rootNode.value,leftChild_X, leftChild_Y,nodeDepth + 1,canvas, window)

    return rootNode


def getMinNodeValue(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode.leftChild is None:
        return rootNode.value
    else:
        leftChild_X, leftChild_Y = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        return getMinNodeValue(rootNode.leftChild, leftChild_X, leftChild_Y,  nodeDepth + 1, canvas, window)

    
def getMaxNodeValue(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode.rightChild is None:
        return rootNode.value
    else:
        rightChild_X, rightChild_Y = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        return getMaxNodeValue(rootNode.rightChild, rightChild_X, rightChild_Y, nodeDepth + 1, canvas, window)

def drawTree(rootNode, rootPositionX, rootPositionY, nodeDepth, canvas, window):
    if rootNode is None:
        return

    if rootNode.leftChild is not None:
        leftChild_X, leftChild_Y = calculate_left_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,leftChild_X, leftChild_Y, fill=line_color, width=5)
        drawTree(rootNode.leftChild, leftChild_X, leftChild_Y, nodeDepth + 1,canvas, window)

    if rootNode.rightChild is not None:
        rightChild_X, rightChild_Y = calculate_right_child_pos(rootPositionX, rootPositionY, nodeDepth + 1)
        canvas.create_line(rootPositionX, rootPositionY,rightChild_X, rightChild_Y, fill=line_color, width=5)
        drawTree(rootNode.rightChild, rightChild_X, rightChild_Y, nodeDepth + 1,canvas, window)

    oval_with_text(canvas, rootPositionX, rootPositionY, node_radius, node_color, rootNode.value, text_color, font_size)
    window.update()

def clearAndDrawTree():
    tree_X = window_width/2
    tree_Y = y_padding
    canvas.delete("all")
    drawTree(rootNode, tree_X, tree_Y, 0, canvas, window)

