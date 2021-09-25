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
        best_for = [-1, -1, -1, -1]
        best_back = [-1, -1, -1, -1]
        for i in range(n):
            for j in range(i, n):
                if arr[i][0] < arr[j][0]:
                    qty = min(capital // arr[i][0], arr[i][1])
                    profit = qty * (arr[j][0] - arr[i][0])
                    if profit > best_for[0]:
                        best_for = [profit, qty, arr[i][2], arr[j][2]]
                elif arr[i][0] > arr[j][0]:
                    qty = min(capital // arr[j][0], arr[j][1])
                    profit = qty * (arr[i][0] - arr[j][0])
                    if profit > best_back[0]:
                        best_back = [profit, qty, arr[j][2], arr[i][2]]
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
        ans.append("j-{}-{}".format(curr_year, best_backward[2]))
        ans.append("b-{}-{}".format(best_backward_stock, best_backward[1]))
        ans.append("j-{}-{}".format(best_backward[2], best_backward[3]))
        ans.append("s-{}-{}".format(best_backward_stock, best_backward[1]))
        curr_year = best_backward[3]
    if best_forward_stock != "":
        ans.append("j-{}-{}".format(curr_year, best_forward[2]))
        ans.append("b-{}-{}".format(best_forward_stock, best_forward[1]))
        ans.append("j-{}-{}".format(best_forward[2], best_forward[3]))
        ans.append("s-{}-{}".format(best_forward_stock, best_forward[1]))
        curr_year = best_forward[3]
    if curr_year != 2037:
        ans.append("j-{}-2037".format(curr_year))

    return ans
