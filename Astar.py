class Node:
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall
        self.parent = 0
        self.g = 0
        self.h = 0

    def __repr__(self):
        return 'Node({},{},{},{},{})'.format(self.x, self.y, self.wall, self.getCost(), self.g)

    def getCost(self):
        return self.g + self.h

def getGrid(grid):
    return [[Node(i, j, grid[j][i].wall) for i in range(len(grid[0]))] for j in range(len(grid))]

def getAzimuth(wall):
    b = format(wall, 'b')
    if len(b) < 4:
        for i in range(4 - len(b)):
            b = '0' + b

    e, w, s, n = b
    return int(n), int(s), int(w), int(e)



def getDirections(grid, startPos, targetPos):
    grid = getGrid(grid)
    startNode = grid[startPos[0]][startPos[1]]
    targetNode = grid[targetPos[0]][targetPos[1]]

    closedList = []
    openList = [startNode]
    nodeList = []
    def appendOpenList(x, y):
        if not (grid[y][x] in closedList):
            nNode = grid[y][x]
            moveCost = nextNode.g + 10
            if moveCost < nNode.g or not (nNode in openList):
                nNode.g = moveCost
                nNode.h = (abs(nNode.x - targetNode.x) + abs(nNode.y - targetNode.y)) * 10
                nNode.parent = nextNode
                openList.append(nNode)

    while True:
        print(openList)
        nextNode = openList[0]
        for i in range(len(openList)):
            if openList[i].getCost() <= nextNode.getCost() and openList[i].h < nextNode.h:
                nextNode = openList[i]
        openList.remove(nextNode)
        closedList.append(nextNode)

        if nextNode == targetNode:
            fNode = nextNode
            while not fNode == startNode:
                nodeList.insert(0, fNode)
                fNode = fNode.parent
            nodeList.insert(0, fNode)
            break

        n,s,w,e = getAzimuth(nextNode.wall)
        if not n:
            appendOpenList(nextNode.x, nextNode.y - 1)
        if not s:
            appendOpenList(nextNode.x, nextNode.y + 1)
        if not w:
            appendOpenList(nextNode.x - 1, nextNode.y)
        if not e:
            appendOpenList(nextNode.x + 1, nextNode.y)
    return nodeList