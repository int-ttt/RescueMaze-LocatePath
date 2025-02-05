from Astar import *



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
    0000 0001 0010 0011
    0100 0101 0110 0111
    1000 1001 1010 1011
    1100 1101 1110 1111
"""


class Node:
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall
        self.color = 0  # color : red; 1 green; 2 blue; 3
        self.parent = 0
        self.g = 0
        self.h = 0

    def __repr__(self):
        return 'Node({},{},{},{},{},{})'.format(self.x, self.y, self.wall, self.color, self.g, self.h)

    def getCost(self):
        return self.g + self.h

    def setColor(self, color):
        self.color = color

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def addXY(self, x, y):
        self.x += x
        self.y += y

dg = [
    [Node(0, 0, 13), Node(1, 0, 1), Node(2, 0, 9), Node(3, 0, 7), Node(4, 0, 9)],
    [Node(0, 1, 4), Node(1, 1, 2), Node(2, 1, 8), Node(3, 1, 5), Node(4, 1, 8)],
    [Node(0, 2, 4), Node(1, 2, 11), Node(2, 2, 2), Node(3, 2, 8), Node(4, 2, 14)],
    [Node(0, 3, 6), Node(1, 3, 3), Node(2, 3, 11), Node(3, 3, 6), Node(4, 3, 11)]
]
""" dg=___.___.___.___.___.
      |   |   .   |   .   |
      | . | . . . |___. . |
      |   .   .   |   .   |
      | . .___. . | . . . |
      |   .   |   .   |   |
      | . .___|___. . |___|
      |   .   .   |   .   |
      |___.___.___|___.___|
"""
startPos = (0, 0)
targetPos = (0, 3)
print(getDirections(dg, startPos, targetPos))