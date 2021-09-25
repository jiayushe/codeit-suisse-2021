import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/encryption', methods=['POST'])
def evaluateSecretMessage():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test_case in data:
        result.append(encrypt(test_case["n"], test_case["text"]))
    logging.info("My result :{}".format(result))
    return jsonify(result)

def encrypt(n, text):
    # removing spaces and non alphanum characters
    processed_text = ""
    for ch in text:
        if ch.isalnum():
            processed_text += ch.upper()

    # encrypt the string
    start = 0
    list_of_substrings = []
    for i in range(n):
        length = len(processed_text) // n
        remainder = len(processed_text) % n
        if i < remainder:
            length += 1
        substring = processed_text[start: start+length]
        list_of_substrings.append(substring)
        start += length

    # generate the encrypted text from list of substring
    result = ""
    for i in range(len(processed_text)):
        str_index_in_list = i % n
        str_index = i // n
        result += list_of_substrings[str_index_in_list][str_index]

    return result
