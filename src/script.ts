/**
 * Represents a Sudoku board.
 */
interface Board {
    entries: number[][];
    green: [number, number][];
    yellow: [number, number][];
    red: [number, number][];
}

/**
 * Creates the Sudoku board in the HTML table.
 * @param board - The board object containing entries and color information.
 */
function createBoard(board: Board): void {
    const table = document.getElementById('sudoku-board');
    if (table) {
        table.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < 9; j++) {
                const cell = document.createElement('td');
                cell.textContent = board.entries[i][j] === 0 ? '' : board.entries[i][j].toString();
                
                if (board.green.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-green');
                } else if (board.yellow.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-yellow');
                } else if (board.red.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-red');
                } else {
                    cell.classList.add('cell-default');
                }
                
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    } else {
        console.error('Table element not found');
    }
}

/**
 * Updates the frame based on the slider value.
 * @param value - The value of the slider.
 */
function updateframe(value: number): void {
    createBoard(boardFrames[value]);
}

fetch('/get_puzzle', { method: 'GET' })
    .then(response => response.json())
    .then((data: Board) => {
        createBoard(data);
    });

/* fetch timeline */
let boardFrames: Board[] = [];
fetch('/solve', { method: 'GET' })
    .then(response => response.json())
    .then((timeline: Board[]) => {
        boardFrames = timeline;
        const slider = document.getElementById('frame-slider') as HTMLInputElement;
        slider.max = (timeline.length - 1).toString();
        slider.oninput = () => updateframe(parseInt(slider.value));
    });