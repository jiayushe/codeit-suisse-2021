import logging
from flask import request, jsonify
from codeitsuisse import app
from queue import Queue, PriorityQueue
import copy

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test_case in data:
        logging.info("evaluating {}".format(test_case))
        grid = test_case["grid"]
        ind = test_case["interestedIndividuals"]
        ans = {}
        ans["room"] = test_case["room"]
        solve_p1(ans, grid, ind)
        solve_p3(ans, grid)
        solve_p4(ans, grid)
        result.append(ans)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def valid(x, y, row, col):
    return x >= 0 and x < row and y >= 0 and y < col

def solve_p1(ans, ori_grid, ind):
    grid = copy.deepcopy(ori_grid)
    row, col = len(grid), len(grid[0])
    tick = [[-1 for j in range(col)] for i in range(row)]
    q = Queue(maxsize = 10000)
    healthy = 0
    for i in range(row):
        for j in range(col):
            if grid[i][j] == 3:
                tick[i][j] = 0
                q.put((i, j))
            elif grid[i][j] == 1:
                healthy += 1
    dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    max_tick = 0
    while not q.empty():
        x, y = q.get()
        curr_tick = tick[x][y]
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if valid(nx, ny, row, col) and grid[nx][ny] == 1:
                tick[nx][ny] = curr_tick + 1
                grid[nx][ny] = 3
                q.put((nx, ny))
                healthy -= 1
                max_tick = max(max_tick, tick[nx][ny])
    p1 = {}
    for i in ind:
        str_arr = i.split(",")
        x, y = int(str_arr[0]), int(str_arr[1])
        if tick[x][y] == 0:
            p1[i] = -1
        else:
            p1[i] = tick[x][y]
    ans["p1"] = p1
    if healthy > 0:
        ans["p2"] = -1
    else:
        ans["p2"] = max_tick

def solve_p3(ans, ori_grid):
    grid = copy.deepcopy(ori_grid)
    row, col = len(grid), len(grid[0])
    tick = [[-1 for j in range(col)] for i in range(row)]
    q = Queue(maxsize = 10000)
    healthy = 0
    for i in range(row):
        for j in range(col):
            if grid[i][j] == 3:
                tick[i][j] = 0
                q.put((i, j))
            elif grid[i][j] == 1:
                healthy += 1
    dir = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
    max_tick = 0
    while not q.empty():
        x, y = q.get()
        curr_tick = tick[x][y]
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if valid(nx, ny, row, col) and grid[nx][ny] == 1:
                tick[nx][ny] = curr_tick + 1
                grid[nx][ny] = 3
                q.put((nx, ny))
                healthy -= 1
                max_tick = max(max_tick, tick[nx][ny])
    if healthy > 0:
        ans["p3"] = -1
    else:
        ans["p3"] = max_tick

def solve_p4(ans, ori_grid):
    grid = copy.deepcopy(ori_grid)
    row, col = len(grid), len(grid[0])
    INF = 1000000
    pow = [[INF for j in range(col)] for i in range(row)]
    q = PriorityQueue()
    healthy = 0
    for i in range(row):
        for j in range(col):
            if grid[i][j] == 3:
                q.put((0, i, j, []))
                pow[i][j] = 0
            elif grid[i][j] == 1:
                healthy += 1
    dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    tot_pow = 0
    while healthy > 0:
        p, x, y, a = q.get()
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if valid(nx, ny, row, col):
                if grid[nx][ny] == 1:
                    grid[nx][ny] = 3
                    pow[nx][ny] = 0
                    q.put((0, nx, ny, []))
                    for px, py in a:
                        grid[px][py] = 3
                        pow[px][py] = 0
                        q.put((0, px, py, []))
                    healthy -= 1
                    tot_pow += p
                elif (grid[nx][ny] == 0 or grid[nx][ny] == 2) and p + 1 < pow[nx][ny]:
                    pow[nx][ny] = p + 1
                    na = copy.deepcopy(a)
                    na.append((nx, ny))
                    q.put((pow[nx][ny], nx, ny, na))
    ans["p4"] = tot_pow
