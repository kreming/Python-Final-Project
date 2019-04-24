import queue

class Pathfinding():

    #                        U        D       R       L
    neighborRelativeVals = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    def __init__(self, mazeOrig, startLocation, solutionLocation):
        self.mazeOrig = mazeOrig
        self.startLocation = startLocation
        self.solutionLocation = solutionLocation

    # Pass the start location to this function
    def fillFirstValue(self, coordinate):
        self.mazePaths[coordinate[0]][coordinate[1]] = 0

    # This function should only be passed valid, empty coordinates
    def fillMazeSpot(self, origCoordinate,emptyCoordinate):
        self.mazePaths[emptyCoordinate[0]][emptyCoordinate[1]] = self.mazePaths[origCoordinate[0]][origCoordinate[1]] + 1

    def isEnd(self, coordinate, neighborCoordinate):
        x = coordinate[0]
        y = coordinate[1]
        neighborX = neighborCoordinate[0]
        neighborY = neighborCoordinate[1]
        end = 0
        # Check for end
        if self.mazePaths[x + neighborX][y + neighborY] == '3':
            # Access solutionLocation as a global variable (You get an error if you don't for some reason)
            #global solutionLocation
            self.solutionLocation += [x + neighborX]
            self.solutionLocation += [y + neighborY]
            end = 1
        return end

    def isValid(self, coordinate, neighborCoordinate):
        x = coordinate[0]
        y = coordinate[1]
        neighborX = neighborCoordinate[0]
        neighborY = neighborCoordinate[1]
        valid = 0

        # Check for out of bounds
        if (x + neighborX < 0) or (y + neighborY < 0) or (x + neighborX > self.colCount) or (y + neighborY > self.rowCount):
            # Keep valid at 0, it's out of bounds
            pass

        # Check for wall
        elif self.mazeOrig[x+neighborX][y+neighborY] == "1":
            # Keep valid at 0, it's a wall
            pass

        # Check if the path maze has already been filled in at this coordinate
        elif self.mazePaths[x+neighborX][y+neighborY] != "0":
            # Keep valid at 0, it's already been filled in
            pass

        # Anything else should be a blank space that needs filled in
        else:
            valid = 1

        return valid

    def findNeighbors(self, coordinate):
        neighborList = []
        x = coordinate[0]
        y = coordinate[1]

        for neighborRelativeVal in self.neighborRelativeVals:
            if self.isEnd(coordinate, neighborRelativeVal):
                self.solutionLocation = [[x+neighborRelativeVal[0], y+neighborRelativeVal[1]]]
                neighborList += [[x + neighborRelativeVal[0], y + neighborRelativeVal[1]]]
            if self.isValid(coordinate, neighborRelativeVal):
                neighborList += [[x+neighborRelativeVal[0], y+neighborRelativeVal[1]]]

        return neighborList

    def makePath(self):
        solutionPath = []
        x = self.solutionLocation[0]
        y = self.solutionLocation[1]
        solutionPath.append([x, y])

        # Begin loop to begin adding
        while solutionPath[-1] != self.startLocation:


            x = solutionPath[-1][0]
            y = solutionPath[-1][1]
            # temp starts at 55
            temp = self.mazePaths[x][y]
            print(x)
            print(y)

            for neighborRelativeVal in self.neighborRelativeVals:
                # if neighbor coordinate is 1 less than current mazePath val
                if self.mazePaths[x+neighborRelativeVal[0]][y+neighborRelativeVal[1]] == temp - 1:
                    solutionPath.append([x+neighborRelativeVal[0], y+neighborRelativeVal[1]])
                    break

            # solutionPath.append(startLocation)

        return solutionPath


    # Declare variables
    def findPath(self):
        self.rowCount = 0
        self.colCount = 0
        self.mazePaths = self.mazeOrig
        neighborsList = []
        finalPath = []

        # Get amount of rows and cols
        for i, row in enumerate(self.mazeOrig):
            for j, column in enumerate(self.mazeOrig[i]):
                if i == 0:
                    self.colCount += 1
            self.rowCount += 1

        # Check if the user did not provide a start location
        if self.startLocation == []:
            print("The start location was not found. Please put a 'O' somewhere in the maze")
            exit()

        neighborsQ = queue.Queue()
        neighborsQ.put(self.startLocation)
        self.fillFirstValue(self.startLocation)

        while self.solutionLocation == []:
            tempCoordinate = neighborsQ.get()
            neighborsList = self.findNeighbors(tempCoordinate)
            for neighbor in neighborsList:
                if self.solutionLocation != []:
                    self.fillMazeSpot(tempCoordinate, neighbor)
                    break
                else:
                    self.fillMazeSpot(tempCoordinate, neighbor)
                    neighborsQ.put(neighbor)

        finalPath = self.makePath()

        #print(solutionLocation)
        #print(finalPath)
        #print(startLocation)
        return finalPath