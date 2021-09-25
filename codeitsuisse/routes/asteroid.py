import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    test_cases = data.get("test_cases")
    result = []
    for test_case in test_cases:
        logging.info("evaluating {}".format(test_case))
        ans = {}
        ans["input"] = test_case
        solve(ans, test_case)
        result.append(ans)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def score(n):
    if n < 7:
        return n
    elif n < 10:
        return n * 1.5
    else:
        return n * 2

def solve(ans, s):
    n = len(s)
    arr = []
    x = 0
    while x < n:
        let = s[x]
        y = x + 1
        while y < n and let == s[y]:
            y += 1
        arr.append((let, x, y))
        x = y
    m = len(arr)
    best_sum = -1
    best_ori = -1
    for i in range(m):
        let, x, y = arr[i]
        if y - x == 2:
            if best_sum < 1:
                best_sum = 1
                best_ori = x
            continue
        curr_sum = 0
        curr_sum += score(y - x)
        prev, nxt = i - 1, i + 1
        while prev >= 0 and nxt < m:
            prev_let, prev_x, prev_y = arr[prev]
            nxt_let, nxt_x, nxt_y = arr[nxt]
            if prev_let != nxt_let:
                break
            curr_sum += score(prev_y - prev_x + nxt_y - nxt_x)
            prev -= 1
            nxt += 1
        if curr_sum > best_sum:
            best_sum = curr_sum
            best_ori = (x + y) // 2
    if best_sum == int(best_sum):
        best_sum = int(best_sum)
    ans["score"] = best_sum
    ans["origin"] = best_ori
