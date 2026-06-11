import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ping Pong Game", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    overflow: hidden;
    background: black;
}

canvas {
    display: block;
    margin: auto;
    background: #111;
    border: 2px solid white;
}
</style>
</head>
<body>

<canvas id="gameCanvas" width="800" height="500"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 12;
const paddleHeight = 100;

let leftPaddle = {
    x: 20,
    y: canvas.height/2 - paddleHeight/2,
    speed: 7
};

let rightPaddle = {
    x: canvas.width - 32,
    y: canvas.height/2 - paddleHeight/2,
    speed: 5
};

let ball = {
    x: canvas.width/2,
    y: canvas.height/2,
    radius: 10,
    vx: 5,
    vy: 4
};

let playerScore = 0;
let aiScore = 0;

const keys = {};

document.addEventListener("keydown", (e) => {
    keys[e.key] = true;
});

document.addEventListener("keyup", (e) => {
    keys[e.key] = false;
});

function drawRect(x, y, w, h) {
    ctx.fillStyle = "white";
    ctx.fillRect(x, y, w, h);
}

function drawBall() {
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
    ctx.fill();
}

function drawScore() {
    ctx.font = "40px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(playerScore, canvas.width/4, 50);
    ctx.fillText(aiScore, canvas.width*3/4, 50);
}

function resetBall() {
    ball.x = canvas.width/2;
    ball.y = canvas.height/2;
    ball.vx *= -1;
}

function update() {

    // 플레이어 조작
    if (keys["ArrowUp"]) {
        leftPaddle.y -= leftPaddle.speed;
    }
    if (keys["ArrowDown"]) {
        leftPaddle.y += leftPaddle.speed;
    }

    // AI
    if (rightPaddle.y + paddleHeight/2 < ball.y) {
        rightPaddle.y += rightPaddle.speed;
    } else {
        rightPaddle.y -= rightPaddle.speed;
    }

    ball.x += ball.vx;
    ball.y += ball.vy;

    // 위아래 벽
    if (ball.y < ball.radius ||
        ball.y > canvas.height - ball.radius) {
        ball.vy *= -1;
    }

    // 왼쪽 패들 충돌
    if (
        ball.x - ball.radius < leftPaddle.x + paddleWidth &&
        ball.y > leftPaddle.y &&
        ball.y < leftPaddle.y + paddleHeight
    ) {
        ball.vx = Math.abs(ball.vx);
    }

    // 오른쪽 패들 충돌
    if (
        ball.x + ball.radius > rightPaddle.x &&
        ball.y > rightPaddle.y &&
        ball.y < rightPaddle.y + paddleHeight
    ) {
        ball.vx = -Math.abs(ball.vx);
    }

    // 득점
    if (ball.x < 0) {
        aiScore++;
        resetBall();
    }

    if (ball.x > canvas.width) {
        playerScore++;
        resetBall();
    }

    leftPaddle.y = Math.max(
        0,
        Math.min(canvas.height - paddleHeight, leftPaddle.y)
    );

    rightPaddle.y = Math.max(
        0,
        Math.min(canvas.height - paddleHeight, rightPaddle.y)
    );
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawRect(
        leftPaddle.x,
        leftPaddle.y,
        paddleWidth,
        paddleHeight
    );

    drawRect(
        rightPaddle.x,
        rightPaddle.y,
        paddleWidth,
        paddleHeight
    );

    drawBall();
    drawScore();
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>

</body>
</html>
"""

st.title("🏓 Streamlit Ping Pong")

st.write("↑ ↓ 방향키로 조작")

components.html(html_code, height=520)
