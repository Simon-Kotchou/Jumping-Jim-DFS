from queue import Queue
from enum import Enum

#Inputting maze
class State(Enum):
    UNDISCOVERED = 1
    DISCOVERED = 2
    EXPLORED = 3

intMaze = []
global rowDim, colDim

with open('input.txt', 'r') as inputFile:
    temp = [int(i) for i in inputFile.readline().split()]
    rowDim, colDim = temp[0],temp[1]
    for line in inputFile:
        tempList = [int(i) for i in line.split()]
        intMaze.append(tempList)
    inputFile.close()

mazeGraphHV = [[] for x in range(colDim*rowDim)]
mazeGraphDiag = [[] for x in range(colDim*rowDim)]
bfsQueue = Queue()
prevList = [-1 for i in range(colDim*rowDim)]
posList = [-1 for i in range(colDim*rowDim)]
stateList = [State.UNDISCOVERED for i in range(colDim*rowDim)]

#Creating adjLists for each node position

for i in range(rowDim):
    for j in range(colDim):
        nodeWeight = intMaze[i][j]
        loc = (i+1)*colDim - (colDim - j)
    
        if(nodeWeight < 0):
            nodeWeight *= -1

        if(nodeWeight != 0):

            #Right Traversal
            if(j + nodeWeight <= colDim -1):
                mazeGraphHV[loc].append(loc + nodeWeight)

            #Left Traversal
            if(j - nodeWeight >= 0):
                mazeGraphHV[loc].append(loc - nodeWeight)

            #Upwards Traversal
            if(i - nodeWeight >= 0):
                mazeGraphHV[loc].append(loc - nodeWeight * colDim)

            #Downwards Traversal
            if(i + nodeWeight <= rowDim -1):
                mazeGraphHV[loc].append(loc + nodeWeight * colDim)

            #Up+Left Traversal
            if(i - nodeWeight >= 0 and j - nodeWeight >= 0):
                mazeGraphDiag[loc].append((loc - nodeWeight * colDim) - nodeWeight)

            #Up+Right Traversal
            if(i - nodeWeight >= 0 and j + nodeWeight <= colDim -1):
                mazeGraphDiag[loc].append((loc - nodeWeight * colDim) + nodeWeight)

            #Down+Left Traversal
            if(i + nodeWeight <= rowDim -1 and j - nodeWeight >= 0):
                mazeGraphDiag[loc].append((loc + nodeWeight * colDim)- nodeWeight)

            #Down+Right Traversal
            if(i + nodeWeight <= rowDim -1 and j + nodeWeight <= colDim -1):
                mazeGraphDiag[loc].append((loc + nodeWeight * colDim) + nodeWeight)

#Applying Breath-first seach on graph

posList[0] = 0
bfsQueue.put(0)
stateList[0] = State.DISCOVERED
movementList = [-1 for i in range(colDim*rowDim)]

while(not bfsQueue.empty()):
    print(bfsQueue.queue)
    node = bfsQueue.get()
    iLoc = node // rowDim
    jLoc = node % colDim
    
    if(intMaze[iLoc][jLoc] < 0):
        movementList[node] *= -1
    print(movementList)
    if(movementList[node] == -1):

        for adjNode in mazeGraphHV[node]:

            if(stateList[adjNode] == State.UNDISCOVERED):
                
                stateList[adjNode] = State.DISCOVERED
                prevList[adjNode] = node
                posList[adjNode] = posList[node] + 1
                bfsQueue.put(adjNode)
    else:

        for adjNode in mazeGraphDiag[node]:

            if(stateList[adjNode] == State.UNDISCOVERED):

                stateList[adjNode] = State.DISCOVERED
                prevList[adjNode] = node
                posList[adjNode] = posList[node] + 1
                movementList[adjNode] *= -1
                bfsQueue.put(adjNode)
    
    stateList[node] = State.EXPLORED

#Get shortest path
shortestPath = [colDim*rowDim-1]
import pdb; pdb.set_trace()
while(shortestPath[len(shortestPath)-1] != 0):

    shortestPath.append(prevList[shortestPath[len(shortestPath)-1]])

#while(len(shortestPath) != 1

print(shortestPath)
    



