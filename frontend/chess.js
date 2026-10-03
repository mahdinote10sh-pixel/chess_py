const API = "http://127.0.0.1:8000";

let GAME_ID = null;

const boardElement = document.getElementById("board");
const turnElement = document.getElementById("turn");
const messageElement = document.getElementById("message");

let board = [];
let selectedSquare = null;


// نماد مهره‌ها
const pieces = {

    white: {
        king: "♚",
        queen: "♛",
        rook: "♜",
        bishop: "♝",
        knight: "♞",
        pawn: "♟"
    },
    
    black: {
        king: "♔",
        queen: "♕",
        rook: "♖",
        bishop: "♗",
        knight: "♘",
        pawn: "♙"
    }
};


// گرفتن وضعیت بازی
async function createGame() {

    const response = await fetch(`${API}/game/new`, {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Cannot create game");
    }

    const data = await response.json();

    GAME_ID = data.game_id;

    return data;
}


async function loadGame() {

    try {

        if (!GAME_ID) {
            await createGame();
        }

        const response =
            await fetch(`${API}/game/${GAME_ID}`);

        if (!response.ok) {
            throw new Error("Game not found");
        }

        const data = await response.json();

        board = data.board;

        renderBoard();

        updateTurn(data.turn);

        messageElement.textContent = "";

    } catch (error) {

        console.error(error);

        messageElement.textContent =
            "❌ اتصال به سرور برقرار نشد.";
    }
}



// ساخت صفحه شطرنج
function renderBoard() {

    boardElement.innerHTML = "";

    for (let row = 0; row < 8; row++) {

        for (let col = 0; col < 8; col++) {

            const square = document.createElement("div");

            square.classList.add("square");

            if ((row + col) % 2 === 0) {
                square.classList.add("light");
            } else {
                square.classList.add("dark");
            }

            const piece = board[row][col];

            if (piece) {

                square.textContent =
                    pieces[piece.color][piece.type];
            }

            square.dataset.row = row;
            square.dataset.col = col;

            square.addEventListener(
                "click",
                handleSquareClick
            );

            boardElement.appendChild(square);
        }
    }
}


// کلیک روی خانه
async function handleSquareClick(event) {

    const row =
        Number(event.currentTarget.dataset.row);

    const col =
        Number(event.currentTarget.dataset.col);

    const position =
        indexToPosition(row, col);

    const piece = board[row][col];


    // انتخاب مهره
    if (selectedSquare === null) {

        if (!piece) {
            return;
        }

        selectedSquare = position;

        highlightSelected();

        messageElement.textContent =
            `Selected: ${position}`;

        return;
    }


    // کلیک دوباره روی همان مهره
    if (selectedSquare === position) {

        selectedSquare = null;

        renderBoard();

        messageElement.textContent = "";

        return;
    }


    // تلاش برای حرکت
    await makeMove(
        selectedSquare,
        position
    );

    selectedSquare = null;
}


// ارسال حرکت به Backend

async function makeMove(start, end) {

    try {

        const response = await fetch(
            `${API}/game/move`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    game_id: GAME_ID,

                    start: start,

                    end: end
                })
            }
        );


        const data =
            await response.json();


        if (!data.success) {

            messageElement.textContent =
                "❌ حرکت غیرقانونی است.";

            renderBoard();

            return;
        }


        messageElement.textContent =
            `✅ ${start} → ${end}`;


        await loadGame();


    } catch (error) {

        console.error(error);

        messageElement.textContent =
            "❌ خطا در اتصال به سرور.";
    }
}


// هایلایت مهره انتخاب‌شده

function highlightSelected() {

    const squares =
        document.querySelectorAll(".square");


    squares.forEach(square => {

        const row =
            Number(square.dataset.row);

        const col =
            Number(square.dataset.col);

        const position =
            indexToPosition(row, col);


        if (position === selectedSquare) {

            square.classList.add("selected");
        }
    });
}


// تبدیل index به مختصات شطرنج

function indexToPosition(row, col) {

    const file =
        String.fromCharCode(
            "a".charCodeAt(0) + col
        );

    const rank = 8 - row;

    return file + rank;
}


// نمایش نوبت

function updateTurn(turn) {

    if (turn === "white") {

        turnElement.textContent =
            "Turn: White ♙";

    } else {

        turnElement.textContent =
            "Turn: Black ♟";
    }
}


loadGame();
