import logging
from flask import request, jsonify
from codeitsuisse import app
import random

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluateDecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    xs = data["possible_values"]
    m = len(xs)
    n = data["num_slots"]
    hist = data["history"]
    arr = []
    for i in range(n):
        k = random.randint(0, m - 1)
        arr.append(xs[k])
    result = {}
    result["answer"] = arr
    logging.info("My result :{}".format(result))
    return jsonify(result)
