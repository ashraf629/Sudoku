from flask import Flask, render_template, request, jsonify
from random import randint
import visual

app = Flask(__name__)

PUZZLE = '009065430007000800600108020003090002501403960804000100030509007056080000070240090'

def toDict(board):
    return {'entries':board.entries, 'green':board.green, 'yellow':board.yellow, 'red':board.red}

@app.route('/')
def index():
    global PUZZLE
    lines = open("sudoku.csv").readlines()
    numOfPuzzles = len(lines)-1
    n = randint(1,1+numOfPuzzles)
    PUZZLE = lines[n].split(',')[0]
    return render_template('index.html')

@app.route('/get_puzzle', methods=['GET'])
def send_puzzle():
    puzzle = PUZZLE
    puzzle = [[int(puzzle[9*i+j]) for j in range(9)] for i in range(9)]
    puzzle = visual.board(puzzle,red=visual.findZeros(puzzle))
    return jsonify(toDict(puzzle))

@app.route('/solve', methods=['GET'])
def solve():
    puzzle = PUZZLE
    puzzle = [[int(puzzle[9*i+j]) for j in range(9)] for i in range(9)]
    timeline = [toDict(board) for board in visual.createTimeline(puzzle)]
    return jsonify(timeline)

if __name__ == '__main__':
    app.run(debug=True)