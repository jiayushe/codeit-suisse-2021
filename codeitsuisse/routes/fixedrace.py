import logging
from flask import request
from codeitsuisse import app
import random

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluateFixedrace():
    data = request.get_data().decode("utf-8") 
    logging.info("data sent for evaluation {}".format(data))
    result = solve(data)
    logging.info("My result :{}".format(result))
    return result

def solve(data):
    weight = {
        "Zada Zynda": 20,
        "Justin Jack": 18,
        "Fabian Fogel": 16,
        "Jared Jinkins": 14,
        "Anibal Abler": 12,
        "Nelson Noss": 10,
        "Shelli Scheuerman": 10,
        "Gilberto Gethers": 10,
        "Vida Veal": 10,
        "Annalee Angert": 10
    }
    arr = data.split(",")
    for i in arr:
        if i not in weight:
            weight[i] = random.randint(0, 10)
    result = sorted(arr, key=lambda x: -weight[x])
    return ','.join(result)
