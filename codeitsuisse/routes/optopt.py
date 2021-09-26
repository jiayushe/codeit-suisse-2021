import logging
from flask import request, jsonify
from codeitsuisse import app
import math
from scipy.stats import truncnorm

logger = logging.getLogger(__name__)

@app.route('/optopt', methods=['POST'])
def evaluateOpt():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = solve(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def solve(data):
    views = data["view"]
    s, w = 0, 0
    for v in views:
        w += v["weight"]
        s += truncnorm.expect(lambda x: x, args=(v["min"], v["max"]), loc=v["min"], scale=math.sqrt(v["var"])) * v["weight"]
    exp = s / w
    options = data["options"]
    m = len(options)
    profit = 0
    sign = 0
    index = -1
    for i in range(m):
        opt = options[i]
        cur_profit = 0
        cur_sign = 0
        if opt["type"] == "call":
            if exp - opt["strike"] - opt["premium"] > 0:
                cur_profit = exp - opt["strike"] - opt["premium"]
                cur_sign = 1
            elif exp - opt["strike"] < 0:
                cur_profit = opt["premium"]
                cur_sign = -1
        else:
            if opt["strike"] - exp - opt["premium"] > 0:
                cur_profit = opt["strike"] - exp - opt["premium"]
                cur_sign = 1
            elif opt["strike"] - exp < 0:
                cur_profit = opt["premium"]
                cur_sign = -1
        if cur_profit > profit:
            profit = cur_profit
            sign = cur_sign
            index = i
    ans = [0 for i in range(m)]
    ans[index] = sign * 100
    return ans
