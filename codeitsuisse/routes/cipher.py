import logging
from flask import request, jsonify
from codeitsuisse import app
from numpy import log
import math
from hashlib import sha256
import random

logger = logging.getLogger(__name__)

@app.route('/cipher-cracking', methods=['POST'])
def evaluateCipher():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test_case in data:
        ans = solve(test_case)
        result.append(ans)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def solve(data):
    d = data["D"]
    x = data["X"]
    y = data["Y"]
    fx = str(round(log(int(x)), 3))
    logging.info("fx {}".format(fx))
    upper = int(math.pow(10, d))
    for i in range(1, upper + 1):
        test = str(i) + "::" + fx
        if sha256(test.encode('utf-8')).hexdigest() == y:
            return i
    return random.randint(1, upper)
