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
                const cellContent = document.createElement('div');
                cellContent.classList.add('cell-content');
                cellContent.textContent = board.entries[i][j] === 0 ? '' : board.entries[i][j].toString();
                
                if (board.green.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-green');
                } else if (board.yellow.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-yellow');
                } else if (board.red.some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-red');
                } else {
                    cell.classList.add('cell-default');
                }
                
                cell.appendChild(cellContent);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }
}

/**
 * Adjusts the size of the Sudoku board to ensure it remains square,
 * based on the smaller dimension of the parent container.
 */
function adjustTableSize(): void {
    const boardContainer = document.querySelector('.board-container') as HTMLElement | null;
    const table = document.getElementById('sudoku-board') as HTMLElement;

    if (boardContainer && table) {
        const containerWidth = boardContainer.clientWidth;
        const containerHeight = boardContainer.clientHeight;
        const tableSize = Math.min(containerWidth, containerHeight) * 0.9;
        table.style.width = `${tableSize}px`;
        table.style.height = `${tableSize}px`;
    }
}

/**
 * Fetches the puzzle and solution from the server and creates the Sudoku board.
 */
function solve() {
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
            slider.oninput = () => createBoard(timeline[parseInt(slider.value)]);
        });
}

function randomiseBoard() {
    fetch('/randomise', { method: 'GET' })
    .then(() => {solve();});
}

// Call adjustTableSize on window resize and initial load
window.addEventListener('resize', adjustTableSize);
window.addEventListener('load', adjustTableSize);

solve();