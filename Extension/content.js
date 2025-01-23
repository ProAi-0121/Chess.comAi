let previousMoves = [];
let gameStarted = false;
let playerColor = ""; // "white" or "black"
let lastMove = ""; // Track the last move to detect when a new move is made

// Check if the game has started by looking for the "Resign" button
function checkGameStart() {
    const resignButton = document.querySelector('button.small-controls-btn[aria-label="Resign"]');
    return resignButton !== null;
}

// Determine the player's color
function getPlayerColor() {
    const boardOrientation = document.querySelector('.board-board').classList;
    if (boardOrientation.contains('flipped')) {
        return "black";
    }
    return "white";
}

// Get moves from the game by detecting the highlighted squares
function getMoves() {
    const highlightedSquares = document.querySelectorAll('.highlight');
    let currentMoves = [];

    if (highlightedSquares.length === 2) {
        const fromSquare = highlightedSquares[0].classList[1]; // The class name for the square (e.g., square-57)
        const toSquare = highlightedSquares[1].classList[1]; // The class name for the square (e.g., square-55)

        // Detect the new move by comparing with the last move
        const newMove = fromSquare + toSquare;
        if (newMove !== lastMove) {
            currentMoves.push({ color: playerColor, move: newMove });
            lastMove = newMove; // Update last move
        }
    }

    return currentMoves;
}

// Update moves and game status
function updateGameStatus() {
    const isGameStarted = checkGameStart();
    const currentMoves = getMoves();

    // Detect player color only once when the game starts
    if (isGameStarted && !gameStarted) {
        playerColor = getPlayerColor();
    }

    // Only update game data if there is a new move
    if (isGameStarted !== gameStarted || JSON.stringify(currentMoves) !== JSON.stringify(previousMoves)) {
        gameStarted = isGameStarted;
        previousMoves = currentMoves;

        // Only send the data if there is a move
        if (currentMoves.length > 0) {
            const gameData = {
                gameStarted: gameStarted,
                playerColor: playerColor,
                moves: currentMoves, // Only include the detected moves
            };

            // Send the game data to the Flask server
            fetch("http://localhost:5000/update_moves", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(gameData),
            })
            .then((response) => response.json())
            .then((data) => console.log("Server response:", data))
            .catch((err) => console.error("Fetch error:", err));
        }
    }
}

// Continuously monitor game status and moves
setInterval(updateGameStatus, 1000); // Check every second
