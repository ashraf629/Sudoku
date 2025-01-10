function createBoard(board) {
    const table = document.getElementById('sudoku-board');
    if (table) {
        table.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < 9; j++) {
                const cell = document.createElement('td');
                cell.textContent = board['entries'][i][j] === 0 ? '' : board['entries'][i][j].toString();
                
                if (board['green'].some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-green');
                } else if (board['yellow'].some(([x, y]) => x === i && y === j)) {
                    cell.classList.add('cell-yellow');
                } else if (board['red'].some(([x, y]) => x === i && y === j)) {
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

function solveSudoku() {
    fetch('/solve', {method: 'GET'})
    .then(response => response.json())
    .then(timeline => {
        let frame = 0;
        const interval = setInterval(() => {
            if (frame >= timeline.length) {
                clearInterval(interval);
            } else {
                createBoard(timeline[frame]);
                frame++;
            }
        }, 100);
    });
}

fetch('/get_puzzle', {method: 'GET'})
.then(response => response.json())
.then(data => {
    createBoard(data);
});