import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test_case in data:
        logging.info("evaluating {}".format(test_case))
        energy = test_case["energy"]
        capital = test_case["capital"]
        timeline = test_case["timeline"]
        ans = solve(energy, capital, timeline)
        result.append(ans)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def roi(c, b):
    return (b - c) / c

def solve(energy, capital, timeline):
    end = 2037
    start = 2037 - energy // 2
    stocks = set()
    for i in range(start, end + 1):
        if str(i) in timeline:
            year = timeline[str(i)]
            for k, v in year.items():
                stocks.add(k)
    best_forwards = {}
    best_backwards = {}
    for s in stocks:
        arr = []
        for i in range(start, end + 1):
            if str(i) in timeline:
                year = timeline[str(i)]
                if s in year:
                    price = year[s]["price"]
                    qty = year[s]["qty"]
                    arr.append([price, qty, i])
        n = len(arr)
        left_min = [[] for i in range(n)]
        left_min[0] = arr[0]
        left_max = [[] for i in range(n)]
        left_max[0] = arr[0]
        for i in range(1, n):
            if arr[i][0] < left_min[i - 1][0] and arr[i][1] > 0 and arr[i][0] < capital:
                left_min[i] = arr[i]
            else:
                left_min[i] = left_min[i - 1]
            if arr[i][0] > left_max[i - 1][0]:
                left_max[i] = arr[i]
            else:
                left_max[i] = left_max[i - 1]
        right_min = [[] for i in range(n)]
        right_min[n - 1] = arr[n - 1]
        right_max = [[] for i in range(n)]
        right_max[n - 1] = arr[n - 1]
        for i in range(n - 2, -1, -1):
            if arr[i][0] < right_min[i + 1][0] and arr[i][1] > 0 and arr[i][0] < capital:
                right_min[i] = arr[i]
            else:
                right_min[i] = right_min[i + 1]
            if arr[i][0] > right_max[i + 1][0]:
                right_max[i] = arr[i]
            else:
                right_max[i] = right_max[i + 1]
        best_for = [roi(left_min[0][0], right_max[0][0]), left_min[0], right_max[0]]
        best_back = [roi(right_min[0][0], left_max[0][0]), right_min[0], left_max[0]]
        for i in range(1, n):
            rf = roi(left_min[i][0], right_max[i][0])
            if rf > best_for[0]:
                best_for = [rf, left_min[i], right_max[i]]
            rb = roi(right_min[i][0], left_max[i][0])
            if rf > best_back[0]:
                best_back = [rb, right_min[i], left_max[i]]
        best_forwards[s] = best_for
        best_backwards[s] = best_back

    best_forward_stock = ""
    best_forward = []
    for k, v in best_forwards.items():
        if v[0] > 0:
            if best_forward_stock == "" or best_forward[0] < v[0]:
                best_forward_stock = k
                best_forward = v
    best_backward_stock = ""
    best_backward = []
    for k, v in best_backwards.items():
        if v[0] > 0:
            if best_backward_stock == "" or best_backward[0] < v[0]:
                best_backward_stock = k
                best_backward = v

    ans = []
    curr_year = 2037
    if best_backward_stock != "":
        backward_qty = min(capital // best_backward[1][0], best_backward[1][1])
        ans.append("j-{}-{}".format(curr_year, best_backward[1][2]))
        ans.append("b-{}-{}".format(best_backward_stock, backward_qty))
        ans.append("j-{}-{}".format(best_backward[1][2], best_backward[2][2]))
        ans.append("s-{}-{}".format(best_backward_stock, backward_qty))
        curr_year = best_backward[2][2]
    if best_forward_stock != "":
        forward_qty = min(capital // best_forward[1][0], best_forward[1][1])
        ans.append("j-{}-{}".format(curr_year, best_forward[1][2]))
        ans.append("b-{}-{}".format(best_forward_stock, forward_qty))
        ans.append("j-{}-{}".format(best_forward[1][2], best_forward[2][2]))
        ans.append("s-{}-{}".format(best_forward_stock, forward_qty))
        curr_year = best_forward[2][2]
    if curr_year != 2037:
        ans.append("j-{}-2037".format(curr_year))

    return ans
