from collections import namedtuple

azimuth = namedtuple('azimuth', ['n', 's', 'w', 'e'])



class Node:
    def __init__(self, x, y, xx, yy, wall):
        self.x = x
        self.y = y
        self.xx = xx
        self.yy = yy
        self.wall = wall

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.xx}, {self.yy}, {self.wall})'

    def setXY(self, x, y):
        self.x = x
        self.y = y

class NNode(Node):
    def __init__(self):
        Node.__init__(self, 0, 0, 0, 0, 0)


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

startPos = [4, 3]

grid = [[Node(0, 0, startPos[0], startPos[1], dg[startPos[1]][startPos[0]])]]



