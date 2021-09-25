import logging
from flask import request, jsonify
from codeitsuisse import app
import random

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluateDecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = {}
    result["answer"] = solve(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def solve(data):
    xs = data["possible_values"]
    m = len(xs)
    n = data["num_slots"]
    hist = data["history"]
    while True:
        arr = []
        for i in range(n):
            k = random.randint(0, m - 1)
            arr.append(xs[k])
        found = True
        for h in hist:
            if not score(arr, h):
                found = False
                break
        if found:
            return arr

def score(arr, h):
    guess = h["output_received"]
    s = h["result"]
    n = len(arr)
    match = 0
    mismatch = 0
    origin_set = {}
    guess_set = {}
    for i in range(n):
        if arr[i] == guess[i]:
            match += 1
        else:
            if arr[i] not in origin_set:
                origin_set[arr[i]] = 0
            origin_set[arr[i]] += 1
            if guess[i] not in guess_set:
                guess_set[guess[i]] = 0
            guess_set[guess[i]] += 1
    for k, v in origin_set.items():
        if k in guess_set:
            mismatch += min(v, guess_set[k])
    return match + mismatch * 10 == s
