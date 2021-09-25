import logging
from flask import request, jsonify
from codeitsuisse import app
from queue import PriorityQueue

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluateStockHunter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test_case in data:
        logging.info("evaluating {}".format(test_case))
        ans = solve(test_case)
        result.append(ans)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def valid(x, y, row, col):
    return x >= 0 and x < row and y >= 0 and y < col

def solve(data):
    # (Y, X)
    start = [data["entryPoint"]["second"], data["entryPoint"]["first"]]
    target = [data["targetPoint"]["second"], data["targetPoint"]["first"]]
    depth = data["gridDepth"]
    key = data["gridKey"]
    hor = data["horizontalStepper"]
    ver = data["verticalStepper"]
    row, col = target[0] * 3, target[1] * 3
    risk_level = [[0 for j in range(col)] for i in range(row)]
    for i in range(row):
        if start == [i, 0] or target == [i, 0]:
            continue
        risk_level[i][0] = (i * ver + depth) % key
    for i in range(col):
        if start == [0, i] or target == [0, i]:
            continue
        risk_level[0][i] = (i * hor + depth) % key
    for i in range(1, row):
        for j in range(1, col):
            if start == [i, j] or target == [i, j]:
                continue
            risk_level[i][j] = (risk_level[i - 1][j] * risk_level[i][j - 1] + depth) % key
    risk_cost = [[3 - (risk_level[i][j] % 3) for j in range(col)] for i in range(row)]
    grid_map = [["" for j in range(target[1] + 1)] for i in range(target[0] + 1)]
    for i in range(target[0] + 1):
        for j in range(target[1] + 1):
            if risk_cost[i][j] == 3:
                grid_map[i][j] = "L"
            elif risk_cost[i][j] == 2:
                grid_map[i][j] = "M"
            else:
                grid_map[i][j] = "S"
    ans = {}
    ans["gridMap"] = grid_map
    visited = [[0 for j in range(col)] for i in range(row)]
    q = PriorityQueue()
    q.put((0, start[0], start[1]))
    dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while not q.empty():
        c, x, y = q.get()
        if visited[x][y] == 1:
            continue
        visited[x][y] = 1
        if x == target[0] and y == target[1]:
            ans["minimumCost"] = c
            break
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if valid(nx, ny, row, col) and visited[nx][ny] == 0:
                q.put((c + risk_cost[nx][ny], nx, ny))
    return ans
