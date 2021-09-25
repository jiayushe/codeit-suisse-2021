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
    arr = data.split(",")
    random.shuffle(arr)
    return ','.join(arr)
