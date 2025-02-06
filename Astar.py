class direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'direction(x={},y={})'.format(self.x, self.y)

    def addXY(self, x, y):
        self.x += x
        self.y += y

    def copy(self):
        return direction(self.x, self.y)

    def equals(self, dir):
        return self.x == dir.x and self.y == dir.y

    def getStr(self):
        return 'dir({},{})'.format(self.x, self.y)

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

    def __lt__(self, other):
        """ heapq에서 최소값 정렬을 위해 필요 """
        return self.getCost() < other.getCost()

    def __eq__(self, other):
        """ 노드 비교를 위해 필요 """
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return direction(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return direction(self.x + other.x, self.y + other.y)

    def __hash__(self):
        """ set에 추가할 수 있도록 hash 함수 추가 """
        return hash((self.x, self.y))

def getGrid(grid):
    return [[Node(i, j, grid[j][i].wall) for i in range(len(grid[0]))] for j in range(len(grid))]

def getAzimuth(wall):
    """ 벽 정보를 4자리 바이너리로 변환하여 이동 가능 여부 반환 """
    b = format(wall, '04b')  # 4비트 바이너리 변환
    e, w, s, n = map(int, b)  # 정수 변환 후 언패킹
    return n, s, w, e  # 북, 남, 서, 동

import heapq  # 우선순위 큐를 사용하여 openList를 최적화

def getDirections(grid, startPos, targetPos):
    """
    A* 알고리즘을 사용하여 startPos에서 targetPos까지의 최단 경로를 찾는 함수.

    :param grid: 2D 리스트 형태의 맵
    :param startPos: 출발 지점의 (x, y) 좌표
    :param targetPos: 목표 지점의 (x, y) 좌표
    :return: 최단 경로에 포함된 노드 리스트
    """
    grid = getGrid(grid)  # 노드 객체로 이루어진 새로운 grid 생성
    startNode = grid[startPos[1]][startPos[0]]
    targetNode = grid[targetPos[1]][targetPos[0]]

    openList = []  # 탐색할 노드를 저장하는 우선순위 큐 (힙)
    openSet = set()  # 중복 방지를 위한 set
    closedSet = set()  # 이미 방문한 노드를 저장하는 set
    nodeList = []  # 최종 경로 저장 리스트

    # 시작 노드 초기화 및 추가
    startNode.g = 0
    startNode.h = (abs(startNode.x - targetNode.x) + abs(startNode.y - targetNode.y)) * 10
    heapq.heappush(openList, startNode)
    openSet.add(startNode)

    def appendOpenList(x, y):
        """ 주어진 (x, y) 위치의 노드를 openList에 추가하는 함수 """
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):  # 좌표 유효성 검사
            nNode = grid[y][x]

            if nNode in closedSet:  # 이미 방문한 노드는 무시
                return

            moveCost = nextNode.g + 10  # 이동 비용 계산

            if moveCost < nNode.g or nNode not in openSet:
                nNode.g = moveCost
                nNode.h = (abs(nNode.x - targetNode.x) + abs(nNode.y - targetNode.y)) * 10  # 맨해튼 거리
                nNode.parent = nextNode  # 부모 노드 설정

                heapq.heappush(openList, nNode)  # 우선순위 큐에 삽입
                openSet.add(nNode)  # openSet에도 추가

    # A* 알고리즘 실행
    while openList:
        nextNode = heapq.heappop(openList)  # 최소 비용 노드 가져오기
        openSet.remove(nextNode)  # openSet에서 제거
        closedSet.add(nextNode)  # 방문한 노드 저장

        # 목표 도착 시 경로 반환
        if nextNode == targetNode:
            fNode = nextNode.parent
            while fNode:
                print(fNode, nextNode)
                nodeList.insert(0, nextNode - fNode)  # 경로 역추적
                nextNode = fNode
                fNode = fNode.parent
            return nodeList  # 최종 경로 반환

        # 현재 노드에서 이동 가능한 방향 확인
        n, s, w, e = getAzimuth(nextNode.wall)
        if not n:
            appendOpenList(nextNode.x, nextNode.y - 1)  # 북쪽 이동
        if not s:
            appendOpenList(nextNode.x, nextNode.y + 1)  # 남쪽 이동
        if not w:
            appendOpenList(nextNode.x - 1, nextNode.y)  # 서쪽 이동
        if not e:
            appendOpenList(nextNode.x + 1, nextNode.y)  # 동쪽 이동

    return []  # 경로가 없을 경우 빈 리스트 반환

# def getDirections(grid, startPos, targetPos):
#     grid = getGrid(grid)
#     startNode = grid[startPos[0]][startPos[1]]
#     targetNode = grid[targetPos[0]][targetPos[1]]
#
#     closedList = []
#     openList = [startNode]
#     nodeList = []
#     def appendOpenList(x, y):
#         if not (grid[y][x] in closedList):
#             nNode = grid[y][x]
#             moveCost = nextNode.g + 10
#             if moveCost < nNode.g or not (nNode in openList):
#                 nNode.g = moveCost
#                 nNode.h = (abs(nNode.x - targetNode.x) + abs(nNode.y - targetNode.y)) * 10
#                 nNode.parent = nextNode
#                 openList.append(nNode)
#
#     while True:
#         print(openList)
#         nextNode = openList[0]
#         for i in range(len(openList)):
#             if openList[i].getCost() <= nextNode.getCost() and openList[i].h < nextNode.h:
#                 nextNode = openList[i]
#         openList.remove(nextNode)
#         closedList.append(nextNode)
#
#         if nextNode == targetNode:
#             fNode = nextNode
#             while not fNode == startNode:
#                 nodeList.insert(0, fNode)
#                 fNode = fNode.parent
#             nodeList.insert(0, fNode)
#             break
#
#         n,s,w,e = getAzimuth(nextNode.wall)
#         if not n:
#             appendOpenList(nextNode.x, nextNode.y - 1)
#         if not s:
#             appendOpenList(nextNode.x, nextNode.y + 1)
#         if not w:
#             appendOpenList(nextNode.x - 1, nextNode.y)
#         if not e:
#             appendOpenList(nextNode.x + 1, nextNode.y)
#     return nodeList
