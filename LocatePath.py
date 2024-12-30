from collections import namedtuple
from itertools import dropwhile

azimuth = namedtuple('azimuth', ['n', 's', 'w', 'e'])
direction = namedtuple('direction', ['x', 'y'])

class Node:
    def __init__(self, x, y, originPos, wall):
        self.x = x
        self.y = y
        self.xx = originPos[0]
        self.yy = originPos[1]
        self.wall = wall

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.xx}, {self.yy}, {self.wall})'

    def setXY(self, x, y):
        self.x = x
        self.y = y

class NNode(Node):
    def __init__(self):
        Node.__init__(self, 0, 0, [0, 0], 0)


azimuthList = [
    azimuth(1,1,1,1),azimuth(0,1,1,1),azimuth(1,0,1,1),azimuth(0,0,1,1),
    azimuth(1,1,0,1),azimuth(0,1,0,1),azimuth(1,0,0,1),azimuth(0,0,0,1),
    azimuth(1,1,1,0),azimuth(0,1,1,0),azimuth(1,0,1,0),azimuth(0,0,1,0),
    azimuth(1,1,0,0),azimuth(0,1,0,0),azimuth(1,0,0,0),azimuth(0,0,0,0)
]

"""             ___             ___
    0=      1=      2=      3=
                        ___     ___
                ___             ___
    4= |    5= |    6= |    7= |   
       |       |       |___    |___
                ___             ___
    8=     |9=     |10=    |11=    |
           |       |    ___|    ___|
                ___             ___
    12=|   |13=|   |14=|   |15=|   |
       |   |   |   |   |___|   |___|
    0000 1000 0100 1100
    0010 1010 0110 1110
    0001 1001 0101 1101
    0011 1011 0111 1111
"""

dg = [
   [  7,  1,  9,  7,  9],
   [  5,  2,  8,  5,  8],
   [ 12,  7,  2,  8, 14],
   [  6,  3, 11,  6, 11]
]
""" dg=___.___.___.___.___.
      |   .   .   |   .   |
      |___. . . . |___. . |
      |   .   .   |   .   |
      | . .___. . | . . . |
      |   |   .   .   |   |
      | . |___.___. . |___|
      |   .   .   |   .   |
      |___.___.___|___.___|
"""

openList = []
closedList = []
startPos = [4, 1]

grid = [[Node(0, 0, startPos, dg[startPos[1]][startPos[0]])]]
tGrid = [[NNode()]]
nextNode = grid[0][0]

#### last node  list
#### north 0 south 1 west 2 east 3
lastPos = 1

print(grid)


lastPos = 0

for i in range(3):

    dx, dy = 0, 0
    n, s, w, e = azimuthList[nextNode.wall]

    print(lastPos, (n and lastPos != 1), (s and lastPos != 0))

    if e and lastPos != 2:
        openList.append(direction(1, 0))
        lastPos = 3
    if w and lastPos != 3:
        openList.append(direction(-1, 0))
        lastPos = 2
    if lastPos != 0 and s:
        openList.append(direction(0, 1))
        lastPos = 1
    if n and lastPos != 1:
        openList.append(direction(0, -1))
        lastPos = 0

    print(n, s, w, e, openList, closedList)

    dir = openList[-1]
    if dir in closedList:
        openList.remove(dir)
        dir = openList[-1]
    openList.remove(dir)
    closedList.append(dir)
    nextNode = Node(nextNode.x + dir.x, nextNode.y + dir.y, [nextNode.xx + dir.x, nextNode.yy + dir.y], dg[nextNode.yy + dir.y][nextNode.xx + dir.x])

    print(dir.x, len(grid[0]), nextNode.x + dir[0], nextNode.x + dir[0] < 0, dir[0] == -1 or dir[1] == 0)
    if (dir.x == -1 or dir.x == 1) and (len(grid[0]) < nextNode.x + dir.x + 1 or nextNode.x + dir.x < 0):
        tGrid = [NNode() for i in range(len(grid[0]) + 1)]
        dx = 1
    else:
        tGrid = [NNode() for i in range(len(grid[0]))]

    if (dir.y == -1 or dir.y == 1) and (len(grid) <nextNode.y + dir.y + 1 or nextNode.y + dir.y < 0):
        tGrid = [(tGrid + []) for i in range(len(grid) + 1)]
        dy = 1
    else:
        tGrid = [(tGrid + []) for i in range(len(grid))]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            node = grid[y][x]
            tGrid[y+dy][x+dx] = node

    tGrid[nextNode.y+dy][nextNode.x+dx] = nextNode
    for y in range(len(tGrid)):
        for x in range(len(tGrid[0])):
            node = tGrid[y][x]
            node.setXY(node.x + dx, node.y + dy)
            tGrid[y][x] = node
    grid = tGrid + []
    tOpenList = []
    tClosedList = []
    for e in openList:
        tOpenList.append(direction(e.x + dx * 2, e.y + dy * 2))
    for e in closedList:
        tClosedList.append(direction(e.x + dx * 2, e.y + dy * 2))
    openList = tOpenList
    closedList = tClosedList
    print(tGrid)

