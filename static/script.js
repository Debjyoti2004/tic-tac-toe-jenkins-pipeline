
document.addEventListener("DOMContentLoaded", () => {
    const boardElement = document.querySelector("table");

    boardElement.addEventListener("click", (event) => {
        const cell = event.target.closest("td");
        if (cell && !cell.textContent.trim()) {
            const [row, col] = cell.id.split("-").slice(1).map(Number);
            makeMove(row, col);
        }
    });
});


function makeMove(row, col) {
    const cell = document.getElementById(`cell-${row}-${col}`);
    cell.innerHTML = '<div class="loader"></div>'; 

    fetch("/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ row, col }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            updateBoard(data.board);
            updateMessage(data.winner, data.game_over);
        }
    });
}


function resetGame() {
    fetch("/reset", {
        method: "POST",
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
        updateMessage(null, false);
    });
}


function updateBoard(board) {
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const cell = document.getElementById(`cell-${i}-${j}`);
            cell.textContent = board[i][j] || "";
        }
    }
}


function updateMessage(winner, game_over) {
    const messageDiv = document.getElementById("message");
    if (game_over) {
        if (winner) {
            messageDiv.innerHTML = `<p>Game Over! ${winner} wins!</p>`;
        } else {
            messageDiv.innerHTML = `<p>Game Over! It's a tie!</p>`;
        }
    } else {
        messageDiv.innerHTML = "";
    }
}
