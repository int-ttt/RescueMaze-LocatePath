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
    startNode = grid[startPos[1]][startPos[0]]  # 출발 노드
    targetNode = grid[targetPos[1]][targetPos[0]]  # 목표 노드

    openList = []  # 탐색할 노드를 저장하는 우선순위 큐 (힙)
    openSet = set()  # 중복 방지를 위한 set (openList의 빠른 조회용)
    closedSet = set()  # 이미 방문한 노드를 저장하는 set
    nodeList = []  # 최종 경로를 저장하는 리스트

    # 시작 노드를 openList에 추가 (힙 구조 유지)
    heapq.heappush(openList, (startNode.getCost(), startNode))
    openSet.add(startNode)

    def appendOpenList(x, y):
        """
        주어진 (x, y) 위치의 노드를 openList에 추가하는 함수.
        새로운 노드가 더 낮은 비용으로 갱신될 경우 값을 업데이트.

        :param x: 새로운 노드의 x 좌표
        :param y: 새로운 노드의 y 좌표
        """
        # 유효한 좌표인지 검사 (grid 범위를 벗어나지 않도록 체크)
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            nNode = grid[y][x]  # 탐색할 노드

            # 이미 방문한 노드라면 무시
            if nNode in closedSet:
                return

            moveCost = nextNode.g + 10  # G 값(이동 비용) 계산

            # 새로운 경로가 더 최적이거나, 아직 openList에 없는 경우 업데이트
            if moveCost < nNode.g or nNode not in openSet:
                nNode.g = moveCost
                nNode.h = (abs(nNode.x - targetNode.x) + abs(nNode.y - targetNode.y)) * 10  # 맨해튼 거리 계산
                nNode.parent = nextNode  # 부모 노드 설정

                if nNode not in openSet:
                    heapq.heappush(openList, (nNode.getCost(), nNode))  # 우선순위 큐에 삽입
                    openSet.add(nNode)  # openSet에도 추가

    # A* 알고리즘 실행
    while openList:
        # 우선순위 큐에서 가장 비용이 낮은 노드를 꺼냄
        _, nextNode = heapq.heappop(openList)
        openSet.remove(nextNode)  # openSet에서 제거
        closedSet.add(nextNode)  # 방문한 노드 목록에 추가

        # 목표 노드에 도착한 경우 경로를 추적하여 반환
        if nextNode == targetNode:
            fNode = nextNode
            while fNode != startNode:
                nodeList.insert(0, fNode)  # 최단 경로를 nodeList에 저장 (역순으로 삽입)
                fNode = fNode.parent  # 부모 노드를 따라가며 경로 복원
            nodeList.insert(0, fNode)  # 출발 노드 추가
            break

        # 현재 노드의 벽 정보를 가져와 이동 가능한 방향 확인
        n, s, w, e = getAzimuth(nextNode.wall)
        if not n:
            appendOpenList(nextNode.x, nextNode.y - 1)  # 북쪽 이동
        if not s:
            appendOpenList(nextNode.x, nextNode.y + 1)  # 남쪽 이동
        if not w:
            appendOpenList(nextNode.x - 1, nextNode.y)  # 서쪽 이동
        if not e:
            appendOpenList(nextNode.x + 1, nextNode.y)  # 동쪽 이동

    return nodeList  # 최단 경로 반환