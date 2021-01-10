import pygame
import math
from queue import PriorityQueue
import numpy
pygame.init()
black=(0,0,0)
white=(255,255,255)
blue=(0,0,255)
red=(255,0,0)
green=(38,219,50)
yellow=(255,255,0)
width=800
win=pygame.display.set_mode((width,width))
pygame.display.set_caption('A* PATH FINDING BY BARA BARHAM')
selectedNodes=[]


class Node:
    def __init__(self,row,col,width,totalRows):
        self.row=row
        self.col=col
        self.width=width
        self.totalRows=totalRows
        self.x=row*width
        self.y=col*width
        self.color=white
        self.neghibours=[]



    def getPosition(self):
        return (self.row,self.col)

    def draw(self,win):
        #top left corner is (0,0) and as u move to right x increases and as u move down y increases
        # :D
        #say that the width is 800 and height is 800 then the
        #bottom right corner is (800,800) or (799,799) im not really sure :)
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def makeColorBlack(self):
        self.color=black

    def reset(self):
        self.color=white
    #start node color
    def makeColorRed(self):
        self.color=red

    #end node color
    def makeColorBlue(self):
        self.color=blue

    #visited nodes
    def makeColorGreen(self):
        self.color=green

    def makeColorYellow(self):
        self.color=yellow

def makeTheGrids(rows,width):
        grid=[]
        gap=width//rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                #gap means distance between each grid which is width up
                #rows means total amount of rows the grid is spliited into
                node=Node(i,j,gap,rows)
                #lets say i=0 so now in first row append this new node which will be a white square etc etc
                grid[i].append(node)
        return grid

#this function is to draw lines between these squares

def drawGridLines(win,rows,width):
    gap=width // rows
    for i in range(rows):
        #draw horizontal line first
        #pass the window, the color of line, coordinates where line starts from
        #and coordinates where line ends
        pygame.draw.line(win,black,(0,i*gap),(width,i*gap))
        #now draw the vertical lines
        for j in range(rows):
            pygame.draw.line(win, black, ( j * gap,0), ( j * gap,width))

def drawTheMainScreen(win,grid,rows,width):
    win.fill(white)
    for row in grid:
        for nodes in row:
            nodes.draw(win)

    drawGridLines(win,rows,width)
    #this one just updates the screen
    pygame.display.update()


def get_mouse_click_position(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

def A_Star_Algorithm(draw,startNode,endNode,grid):
    #we want to start from startNode
    #visit upward downward left right
    queue=PriorityQueue()
    currentIndex=startNode
    queue.put((math.inf,0))
    x2=endNode[0]
    y2=endNode[1]
    visitedNodes=[]
    #visitedNodes.append(startNode)
    cameFrom=[]
    g_score=dict()
    g_score[startNode]=0
    while queue.qsize()>0:
        #loop through all four possible neghibors for node
        #switchDirections means switch from left and right to upside and downside

        switchDirection=0
        for i in range(4):
            # add upper neghibour
            if switchDirection==0:
                # check if its not on upper side to make sure it has a upper neghibour
                # currentIndex[0] = Y-axis , currentIndex[1]=X-axis
                if currentIndex[1]!=0:
                    #check if we already visited it
                    if (currentIndex[0],currentIndex[1]-1) in visitedNodes==True:
                        #print('This node is already visited')
                        switchDirection+=1
                        continue
                    #check if its not a block or startnode
                    if grid[currentIndex[0]][currentIndex[1]-1].color!=black and(currentIndex[0],currentIndex[1]-1)!=startNode:
                        #check if this the goal node
                        if (currentIndex[0],currentIndex[1]-1)==endNode:
                            drawFinalPath(startNode,visitedNodes,grid,currentIndex,cameFrom)
                            return

                        x1=currentIndex[0]
                        y1=currentIndex[1]-1
                        hDistance=h(x1,y1,x2,y2)
                        gDistance=g_score[currentIndex]+1
                        #print('Updated the gScore for '+str((x1,y1))+' with value of : '+str(g_score[currentIndex]+1))
                        if (x1,y1) in g_score:
                            if g_score[(x1,y1)]>gDistance:
                                g_score[(x1, y1)] = gDistance
                                queue.put((hDistance+gDistance,(x1,y1),currentIndex))
                        else:
                            g_score[(x1, y1)] = gDistance
                            queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        selectedNodes.append(grid[currentIndex[0]][currentIndex[1]-1])
                        #we store the node we came from and the neghibour node in visitedNodes so
                        #we can use it in drawFinalPath function
                        visitedNodes.append(((x1,y1)))
                        cameFrom.append(currentIndex)


            #add lower neghibour
            elif switchDirection==1:
                # check if its not on lower side to make sure it has a lower neghibour
                # currentIndex[0] = Y-axis , currentIndex[1]=X-axis
                if currentIndex[1]!=49:
                    if (currentIndex[0],currentIndex[1]+1) in visitedNodes:
                        #print('This node is already visited')
                        switchDirection+=1
                        continue
                    if grid[currentIndex[0]][currentIndex[1] + 1].color != black and(currentIndex[0],currentIndex[1]+1)!=startNode:
                        #check if this is goal node
                        if (currentIndex[0],currentIndex[1]+1)==endNode:
                            drawFinalPath(startNode, visitedNodes, grid, currentIndex,cameFrom)
                            return
                        #grid[currentIndex[0]][currentIndex[1] + 1].makeColorGreen()
                        x1 = currentIndex[0]
                        y1 = currentIndex[1] + 1
                        hDistance = h(x1, y1, x2, y2)
                        gDistance = g_score[currentIndex] + 1
                        #print('Updated the gScore for '+str((x1,y1))+' with value of : '+str(g_score[currentIndex]+1))
                        if (x1, y1) in g_score:
                            if g_score[(x1, y1)] > gDistance:
                                g_score[(x1, y1)] = gDistance
                                queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        else:
                            g_score[(x1, y1)] = gDistance
                            queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        selectedNodes.append(grid[currentIndex[0]][currentIndex[1]+1])
                        # we store the node we came from and the neghibour node in visitedNodes so
                        # we can use it in drawFinalPath function
                        visitedNodes.append((x1, y1))
                        cameFrom.append(currentIndex)

            #add left neghibour:
            elif switchDirection==2:
                #check if its not on left side to make sure it has a left neghibour
                #currentIndex[0] = Y-axis , currentIndex[1]=X-axis
                if currentIndex[0]!=0:
                    if (currentIndex[0]-1,currentIndex[1]) in visitedNodes:
                        #print('This node is already visited')
                        switchDirection+=1
                        continue
                    if grid[currentIndex[0]-1][currentIndex[1]].color!=black and(currentIndex[0]-1,currentIndex[1])!=startNode:
                        #check if its goal node
                        if (currentIndex[0]-1,currentIndex[1])==endNode:
                            drawFinalPath(startNode, visitedNodes, grid, currentIndex,cameFrom)
                            return
                        #grid[currentIndex[0]-1][currentIndex[1]].makeColorGreen()
                        x1 = currentIndex[0]-1
                        y1 = currentIndex[1]
                        hDistance = h(x1, y1, x2, y2)
                        gDistance = g_score[currentIndex] + 1
                        #print('Updated the gScore for '+str((x1,y1))+' with value of : '+str(g_score[currentIndex]+1))
                        if (x1, y1) in g_score:
                            if g_score[(x1, y1)] > gDistance:
                                g_score[(x1, y1)] = gDistance
                                queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        else:
                            g_score[(x1, y1)] = gDistance
                            queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        selectedNodes.append(grid[currentIndex[0]-1][currentIndex[1]])
                        # we store the node we came from and the neghibour node in visitedNodes so
                        # we can use it in drawFinalPath function
                        visitedNodes.append((x1, y1))
                        cameFrom.append(currentIndex)

            #add right neghibour
            else:
                # check if its not on right side to make sure it has a right neghibour
                # currentIndex[0] = Y-axis , currentIndex[1]=X-axis
                if currentIndex[0]!=49:
                    if (currentIndex[0]+1,currentIndex[1]) in visitedNodes:
                        #print('This node is already visited')
                        switchDirection+=1
                        continue
                    if grid[currentIndex[0]+1][currentIndex[1]].color!=black and (currentIndex[0]+1,currentIndex[1])!=startNode:
                        #check if its goal node
                        if (currentIndex[0]+1,currentIndex[1])==endNode:
                            drawFinalPath(startNode, visitedNodes, grid, currentIndex,cameFrom)
                            return
                        #grid[currentIndex[0]+1][currentIndex[1]].makeColorGreen()
                        x1 = currentIndex[0]+1
                        y1 = currentIndex[1]
                        hDistance = h(x1, y1, x2, y2)
                        gDistance = g_score[currentIndex] + 1
                        #print('Updated the gScore for '+str((x1,y1))+' with value of : '+str(g_score[currentIndex]+1))
                        if (x1, y1) in g_score:
                            if g_score[(x1, y1)] > gDistance:
                                g_score[(x1, y1)] = gDistance
                                queue.put((hDistance + gDistance, (x1, y1), currentIndex))
                        else:
                            g_score[(x1, y1)] = gDistance
                            queue.put((hDistance + gDistance, (x1, y1), currentIndex))

                        selectedNodes.append(grid[currentIndex[0]+1][currentIndex[1]])
                        # we store the node we came from and the neghibour node in visitedNodes so
                        # we can use it in drawFinalPath function
                        visitedNodes.append((x1, y1))
                        cameFrom.append(currentIndex)
            switchDirection+=1
        #for loop ends here
        tempNode=queue.get()
        currentIndex=tempNode[1]
        draw()
        grid[currentIndex[0]][currentIndex[1]].makeColorGreen()
        #return
    #while loop ends here

def h(x1,y1,x2,y2):
    return abs(y1-y2) + abs(x1-x2)

#this function will draw the final path in yellow after finding the best path
def drawFinalPath(startNode,visitedNodes,grid,currentNode,cameFrom):
    if currentNode==startNode:
        print('done')
        return
    else:
        grid[currentNode[0]][currentNode[1]].makeColorYellow()

    #now after coloring it with yellow we wanna get the node that we came from
    #so if its like A->B->C->D->GOAL
    #we will go from GOAL->D->C->B->A
    indexOfParent=visitedNodes.index(currentNode)
    drawFinalPath(startNode,visitedNodes,grid,cameFrom[indexOfParent],cameFrom)




def main():
    rows=50
    grid=makeTheGrids(rows,width)
    start=None
    end=None
    run=True
    started=False
    first=0

    while run:
        drawTheMainScreen(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=0
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    print("start from node: "+str(start)+" and finish at node "+str(end))

                    A_Star_Algorithm(lambda: drawTheMainScreen(win, grid, rows, width),start,end,grid)

            elif pygame.mouse.get_pressed()[0]:
                #if this is the first time u press then make it red and second click makes it blue
                if first<2:
                    pos = pygame.mouse.get_pos()
                    row, col = get_mouse_click_position(pos, rows, width)
                    if first==0:
                        start=(row,col)
                        grid[row][col].makeColorRed()
                        selectedNodes.append(grid[row][col])
                    else:
                        end=(row,col)
                        grid[row][col].makeColorBlue()
                        selectedNodes.append(grid[row][col])
                    first+=1
                #if first is larger than 2 then this means we already set the start and end points
                else:
                    pos = pygame.mouse.get_pos()
                    row,col=get_mouse_click_position(pos,rows,width)
                    grid[row][col].makeColorBlack()
                    selectedNodes.append(grid[row][col])
            #reset the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for i in selectedNodes:
                        i.reset()
                    first=0
                    selectedNodes.clear()



    pygame.quit()

main()





