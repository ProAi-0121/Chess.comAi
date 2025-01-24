let previousMoves = [];
let gameStarted = false;
let lastMove = ""; 

function checkGameStart() {
    const button1 = document.evaluate('//*[@id="board-layout-sidebar"]/div[2]/div[3]/button[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    const button2 = document.evaluate('//*[@id="board-layout-sidebar"]/div[2]/div[3]/button[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    return button1 !== null || button2 !== null;
}

function getMoves() {
    const highlightedSquares = document.querySelectorAll('.highlight');
    let currentMoves = [];

    if (highlightedSquares.length === 2) {
        const fromSquare = highlightedSquares[0].classList[1];
        const toSquare = highlightedSquares[1].classList[1];
        const newMove = fromSquare + toSquare;
        if (newMove !== lastMove) {
            currentMoves.push({ move: newMove });
            lastMove = newMove; 
        }
    }

    return currentMoves;
}

function updateGameStatus() {
    const isGameStarted = checkGameStart();
    const currentMoves = getMoves();

    if (isGameStarted !== gameStarted || JSON.stringify(currentMoves) !== JSON.stringify(previousMoves)) {
        gameStarted = isGameStarted;
        previousMoves = currentMoves;
        const inputFieldExists = document.querySelector('input[type="text"][maxlength="125"]') !== null;
        const gamestate = inputFieldExists ? gameStarted : false;

        const gameData = {
            gamestate: gamestate,
            moves: currentMoves.length > 0 ? currentMoves : previousMoves,
        };

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

setInterval(updateGameStatus, 1000);
