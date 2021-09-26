import logging
from flask import request, jsonify
from codeitsuisse import app
import math
import random
import asyncio
import aiohttp
from aiosseclient import aiosseclient
import requests
import json

logger = logging.getLogger(__name__)

endpoint = "https://cis2021-arena.herokuapp.com/"

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateTTT():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    play(data.get("battleId"))
    return jsonify("")

def play(id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(game(id))

async def game(id):
    start_endpoint = endpoint + "tic-tac-toe/start/" + id
    play_endpoint = endpoint + "tic-tac-toe/play/" + id

    self, oppo = "", ""
    self_val, oppo_val = 1, -1
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def wins(state, player):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        return [player, player, player] in win_state
    
    def ends(state):
        return wins(state, self_val) or wins(state, oppo_val)

    def eval(state):
        if wins(state, self_val):
            score = 1
        elif wins(state, oppo_val):
            score = -1
        else:
            score = 0
        return score

    def empty_cells(state):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def valid(x, y):
        return board[x][y] == 0

    def minimax(state, depth, player):
        if player == self_val:
            best = [-1, -1, -math.inf]
        else:
            best = [-1, -1, math.inf]
        if depth == 0 or ends(state):
            score = eval(state)
            return [-1, -1, score]
        for cell in empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y
            if player == self_val:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best
    
    def set_move(x, y, player):
        if valid(x, y):
            board[x][y] = player
            return True
        else:
            return False

    def send_move(x, y):
        pos_rev_map = {
            0: "NW", 1: "N", 2: "NE",
            3: "W", 4: "C", 5: "E",
            6: "SW", 7: "S", 8: "SE"
        }
        data = {
            "action": "putSymbol",
            "position": pos_rev_map[x * 3 + y]
        }
        requests.post(play_endpoint, data = data)

    def flip_table():
        requests.post(play_endpoint, data = {"action": "(╯°□°)╯︵ ┻━┻"})

    def my_turn():
        depth = len(empty_cells(board))
        if depth == 0 or ends(board):
            flip_table()
            return False
        if depth == 9:
            x = random.choice([0, 1, 2])
            y = random.choice([0, 1, 2])
        else:
            move = minimax(board, depth, self_val)
            x, y = move[0], move[1]
        set_move(x, y, self_val)
        send_move(x, y)
        return True

    def oppo_turn(pos):
        depth = len(empty_cells(board))
        if depth == 0 or ends(board):
            flip_table()
            return False
        pos_map = {
            "NW": [0, 0], "N": [0, 1], "NE": [0, 2],
            "W": [1, 0], "C": [1, 1], "E": [1, 2],
            "SW": [2, 0], "S": [2, 1], "SE": [2, 2],
        }
        if pos in pos_map:
            coord = pos_map[pos]
            if not set_move(coord[0], coord[1], oppo_val):
                flip_table()
                return False
            else:
                return True
        else:
            flip_table()
            return False

    async for event in aiosseclient(start_endpoint):
        print("event", event)
        data = json.loads(event.data)
        if "youAre" in data:
            self = data["youAre"]
            oppo = "O" if self == "X" else "O"
            if self == "O":
                my_turn()
        elif "player" in data:
            player = data["player"]
            if player == self:
                continue
            action = data["action"]
            if action == "putSymbol":
                pos = data["position"]
                if not oppo_turn(pos):
                    return
                if not my_turn():
                    return
            else:
                flip_table()
                return
        else:
            return
