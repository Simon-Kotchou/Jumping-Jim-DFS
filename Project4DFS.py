#Author: Simon Kotchou

from enum import Enum

class State(Enum):                  #Enum for possible states of nodes in graph
    UNDISCOVERED = 1
    DISCOVERED = 2
    EXPLORED = 3
    
class MazeGraph():                  #A class for the maze graph, holding data and methods to solve the maze

    def __init__(self):
        self.intMaze = []           #2D matrix of maze weights
        self.rowDim = 0
        self.colDim = 0
        self.adjListSize = 0
        self.mazeGraph = None           #The actual graph represented by a list of adj lists
        self.stateList = None           #Highlighting the state of each node
        self.solutionList = []          #List to store solution
        
    def initGraphs(self,fileName):

        with open(fileName, 'r') as inputFile:                      #Reading in input from file
            temp = [int(i) for i in inputFile.readline().split()]
            self.rowDim, self.colDim = temp[0],temp[1]
            for line in inputFile:
                tempList = [int(i) for i in line.split()]
                self.intMaze.append(tempList)
            inputFile.close()

        self.adjListSize = 2*self.colDim*self.rowDim                            #Initializing data
        self.mazeGraph = [[] for x in range(self.adjListSize)]
        self.stateList = [State.UNDISCOVERED for i in range(self.adjListSize)]

    def createAdjLists(self):
        for i in range(self.rowDim):                                #Walking through each tile in maze
            for j in range(self.colDim):
                
                nodeWeight = self.intMaze[i][j]                     #Gets weight at that tile
                loc = (i*self.rowDim + j)                           #Calculates its location and diagonal location in the adj list
                locDiag = loc + self.adjListSize//2

                if(nodeWeight != 0):

                    if(nodeWeight > 0):                     #If the node is positive, movement will not change

                        #Right Traversal
                        if(j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[loc].append(loc + nodeWeight)

                        #Left Traversal
                        if(j - nodeWeight >= 0):
                            self.mazeGraph[loc].append(loc - nodeWeight)

                        #Upwards Traversal
                        if(i - nodeWeight >= 0):
                            self.mazeGraph[loc].append(loc - nodeWeight * self.colDim)

                        #Downwards Traversal
                        if(i + nodeWeight <= self.rowDim -1):
                            self.mazeGraph[loc].append(loc + nodeWeight * self.colDim)

                        #Up+Left Traversal
                        if(i - nodeWeight >= 0 and j - nodeWeight >= 0):
                            self.mazeGraph[locDiag].append((locDiag - nodeWeight * self.colDim) - nodeWeight)

                        #Up+Right Traversal
                        if(i - nodeWeight >= 0 and j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[locDiag].append((locDiag - nodeWeight * self.colDim) + nodeWeight)

                        #Down+Left Traversal
                        if(i + nodeWeight <= self.rowDim -1 and j - nodeWeight >= 0):
                            self.mazeGraph[locDiag].append((locDiag + nodeWeight * self.colDim)- nodeWeight)

                        #Down+Right Traversal
                        if(i + nodeWeight <= self.rowDim -1 and j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[locDiag].append((locDiag + nodeWeight * self.colDim) + nodeWeight)

                    else:                             #Else the node is negative, and the movement will change

                        nodeWeight *= -1         #Making weight positive for calculations

                        #Right Traversal
                        if(j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[locDiag].append(loc + nodeWeight)

                        #Left Traversal
                        if(j - nodeWeight >= 0):
                            self.mazeGraph[locDiag].append(loc - nodeWeight)

                        #Upwards Traversal
                        if(i - nodeWeight >= 0):
                            self.mazeGraph[locDiag].append(loc - nodeWeight * self.colDim)

                        #Downwards Traversal
                        if(i + nodeWeight <= self.rowDim -1):
                            self.mazeGraph[locDiag].append(loc + nodeWeight * self.colDim)

                        #Up+Left Traversal
                        if(i - nodeWeight >= 0 and j - nodeWeight >= 0):
                            self.mazeGraph[loc].append((locDiag - nodeWeight * self.colDim) - nodeWeight)

                        #Up+Right Traversal
                        if(i - nodeWeight >= 0 and j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[loc].append((locDiag - nodeWeight * self.colDim) + nodeWeight)

                        #Down+Left Traversal
                        if(i + nodeWeight <= self.rowDim -1 and j - nodeWeight >= 0):
                            self.mazeGraph[loc].append((locDiag + nodeWeight * self.colDim)- nodeWeight)

                        #Down+Right Traversal
                        if(i + nodeWeight <= self.rowDim -1 and j + nodeWeight <= self.colDim -1):
                            self.mazeGraph[loc].append((locDiag + nodeWeight * self.colDim) + nodeWeight)

                else:                                           #If the node has a weight of 0 (the target), it will point back to itself
                    self.mazeGraph[loc].append(loc)
                    self.mazeGraph[locDiag].append(loc)
                        

    def DFSUtil(self, node):

        targetTile = self.adjListSize - 1                   #Initializing the target tile and node
        targetNode = self.colDim * self.rowDim - 1

        self.stateList[node] = State.DISCOVERED                     #setting initial node to discovered
        
        if(node > self.rowDim * self.colDim - 1):                       #Resetting index of diagonal adj nodes and appending to solution list
            self.solutionList.append(node - self.adjListSize//2)
        else:
            self.solutionList.append(node)

        if(node == targetTile):                                         #if the node is at the end of the maze, will finish DFS recursion                            

            self.stateList[targetNode] = State.DISCOVERED

        for adjNode in self.mazeGraph[node]:                                #for each adjacent node

            if(self.stateList[adjNode] == State.UNDISCOVERED):              #if the node is undiscovered, will recurse with that node

                self.DFSUtil(adjNode)

        if(self.solutionList[-1] != targetNode and self.solutionList[-1] != targetTile):        #if there are no other nodes and is not on goal, will pop back to prev node
            
            self.solutionList.pop(-1)
            

    def outputSolution(self, outFile):              

        with open(outFile, 'a') as out:             #writing solution to file in correct format
            
            for node in self.solutionList:
                iLoc = node // self.rowDim
                jLoc = node % self.colDim
                    
                out.write(str((iLoc+1,jLoc+1)))
                out.write(' ')

    def main(self):

        self.initGraphs('input.txt')                        #Calls methods above to solve maze
        self.createAdjLists()
        self.DFSUtil(0)
        self.outputSolution('output.txt')

if __name__ == '__main__':
    MazeGraph().main()
