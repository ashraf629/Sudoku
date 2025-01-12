"use strict";
/**
 * Creates the Sudoku board in the HTML table.
 * @param board - The board object containing entries and color information.
 */
function createBoard(board) {
    var table = document.getElementById('sudoku-board');
    if (table) {
        table.innerHTML = '';
        var _loop_1 = function (i) {
            var row = document.createElement('tr');
            var _loop_2 = function (j) {
                var cell = document.createElement('td');
                var cellContent = document.createElement('div');
                cellContent.classList.add('cell-content');
                cellContent.textContent = board.entries[i][j] === 0 ? '' : board.entries[i][j].toString();
                if (board.green.some(function (_a) {
                    var x = _a[0], y = _a[1];
                    return x === i && y === j;
                })) {
                    cell.classList.add('cell-green');
                }
                else if (board.yellow.some(function (_a) {
                    var x = _a[0], y = _a[1];
                    return x === i && y === j;
                })) {
                    cell.classList.add('cell-yellow');
                }
                else if (board.red.some(function (_a) {
                    var x = _a[0], y = _a[1];
                    return x === i && y === j;
                })) {
                    cell.classList.add('cell-red');
                }
                else {
                    cell.classList.add('cell-default');
                }
                cell.appendChild(cellContent);
                row.appendChild(cell);
            };
            for (var j = 0; j < 9; j++) {
                _loop_2(j);
            }
            table.appendChild(row);
        };
        for (var i = 0; i < 9; i++) {
            _loop_1(i);
        }
    }
}
/**
 * Adjusts the size of the Sudoku board to ensure it remains square,
 * based on the smaller dimension of the parent container.
 */
function adjustTableSize() {
    var boardContainer = document.querySelector('.board-container');
    var table = document.getElementById('sudoku-board');
    if (boardContainer && table) {
        var containerWidth = boardContainer.clientWidth;
        var containerHeight = boardContainer.clientHeight;
        var tableSize = Math.min(containerWidth, containerHeight) * 0.9;
        table.style.width = "".concat(tableSize, "px");
        table.style.height = "".concat(tableSize, "px");
    }
}
/**
 * Fetches the puzzle and solution from the server and creates the Sudoku board.
 */
function solve() {
    fetch('/get_puzzle', { method: 'GET' })
        .then(function (response) { return response.json(); })
        .then(function (data) {
        createBoard(data);
    });
    /* fetch timeline */
    var boardFrames = [];
    fetch('/solve', { method: 'GET' })
        .then(function (response) { return response.json(); })
        .then(function (timeline) {
        boardFrames = timeline;
        var slider = document.getElementById('frame-slider');
        slider.max = (timeline.length - 1).toString();
        slider.oninput = function () { return createBoard(timeline[parseInt(slider.value)]); };
    });
}
function randomiseBoard() {
    fetch('/randomise', { method: 'GET' })
        .then(function () { solve(); });
}
// Call adjustTableSize on window resize and initial load
window.addEventListener('resize', adjustTableSize);
window.addEventListener('load', adjustTableSize);
solve();
