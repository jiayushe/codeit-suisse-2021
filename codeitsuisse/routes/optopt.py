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
    profit = []
    sign = []
    for opt in options:
        if opt["type"] == "call":
            if exp - opt["strike"] - opt["premium"] > 0.05 * exp:
                sign.append(1)
                profit.append(exp - opt["strike"] - opt["premium"])
            elif exp - opt["strike"] < -0.05 * exp:
                sign.append(-1)
                profit.append(opt["premium"])
            else:
                sign.append(0)
                profit.append(0)
        else:
            if opt["strike"] - exp - opt["premium"] > 0.05 * exp:
                sign.append(1)
                profit.append(opt["strike"] - exp - opt["premium"])
            elif opt["strike"] - exp < -0.05 * exp:
                sign.append(-1)
                profit.append(opt["premium"])
            else:
                sign.append(0)
                profit.append(0)
    s_profit = sum(profit)
    s_cnt = 0
    ans = []
    for i in range(len(options) - 1):
        cnt = int(profit[i] / s_profit * 100)
        s_cnt += cnt
        ans.append(cnt * sign[i])
    ans.append((100 - s_cnt) * sign[-1])
    return ans
