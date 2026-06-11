import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏓 Pong Game",
    layout="wide"
)

html = """
<!DOCTYPE html>
<html>
<head>
<style>

html, body{
    margin:0;
    overflow:hidden;
    background:black;
}

canvas{
    display:block;
    margin:auto;
    background:black;
    border:2px solid white;
    cursor:none;
}

</style>
</head>

<body>

<canvas id="gameCanvas" width="700" height="500"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 14;
const paddleHeight = 100;

const MAX_SPEED = 16;

let playerScore = 0;
let aiScore = 0;

const player = {
    x: 20,
    y: 200,
    width: paddleWidth,
    height: paddleHeight
};

const ai = {
    x: canvas.width - 30,
    y: 200,
    width: paddleWidth,
    height: paddleHeight,
    speed: 8
};

const ball = {
    x: canvas.width/2,
    y: canvas.height/2,
    radius: 10,
    vx: 9,
    vy: 5
};

// 마우스 조작
canvas.addEventListener("mousemove", (e) => {

    const rect = canvas.getBoundingClientRect();

    const mouseY = e.clientY - rect.top;

    player.y = mouseY - player.height / 2;

    player.y = Math.max(
        0,
        Math.min(
            canvas.height - player.height,
            player.y
        )
    );
});

function resetBall(){

    ball.x = canvas.width/2;
    ball.y = canvas.height/2;

    const dir = Math.random() > 0.5 ? 1 : -1;

    ball.vx = 9 * dir;
    ball.vy = (Math.random() * 6) - 3;
}

function increaseSpeed(){

    ball.vx *= 1.03;
    ball.vy *= 1.03;

    const speed = Math.sqrt(
        ball.vx * ball.vx +
        ball.vy * ball.vy
    );

    if(speed > MAX_SPEED){

        const ratio = MAX_SPEED / speed;

        ball.vx *= ratio;
        ball.vy *= ratio;
    }
}

function drawRect(x,y,w,h){
    ctx.fillStyle = "white";
    ctx.fillRect(x,y,w,h);
}

function drawBall(){

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "white";
    ctx.fill();
}

function drawNet(){

    for(let i=0;i<canvas.height;i+=30){

        drawRect(
            canvas.width/2-1,
            i,
            2,
            18
        );
    }
}

function drawScore(){

    ctx.fillStyle = "white";
    ctx.font = "42px Arial";

    ctx.fillText(
        playerScore,
        canvas.width/4,
        60
    );

    ctx.fillText(
        aiScore,
        canvas.width*3/4,
        60
    );
}

function collision(ball,paddle){

    return (
        ball.x - ball.radius <
        paddle.x + paddle.width &&

        ball.x + ball.radius >
        paddle.x &&

        ball.y - ball.radius <
        paddle.y + paddle.height &&

        ball.y + ball.radius >
        paddle.y
    );
}

function update(){

    // AI 이동

    const center =
        ai.y + ai.height/2;

    if(center < ball.y - 15){
        ai.y += ai.speed;
    }
    else if(center > ball.y + 15){
        ai.y -= ai.speed;
    }

    ai.y = Math.max(
        0,
        Math.min(
            canvas.height-ai.height,
            ai.y
        )
    );

    // 공 이동

    ball.x += ball.vx;
    ball.y += ball.vy;

    // 벽 충돌

    if(
        ball.y - ball.radius <= 0 ||
        ball.y + ball.radius >= canvas.height
    ){
        ball.vy *= -1;
    }

    // 플레이어 충돌

    if(collision(ball,player)){

        ball.vx = Math.abs(ball.vx);

        const impact =
        (ball.y -
        (player.y + player.height/2))
        /(player.height/2);

        ball.vy = impact * 8;

        increaseSpeed();
    }

    // AI 충돌

    if(collision(ball,ai)){

        ball.vx = -Math.abs(ball.vx);

        const impact =
        (ball.y -
        (ai.y + ai.height/2))
        /(ai.height/2);

        ball.vy = impact * 8;

        increaseSpeed();
    }

    // 점수

    if(ball.x < -30){

        aiScore++;
        resetBall();
    }

    if(ball.x > canvas.width + 30){

        playerScore++;
        resetBall();
    }
}

function render(){

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawNet();
    drawScore();

    drawRect(
        player.x,
        player.y,
        player.width,
        player.height
    );

    drawRect(
        ai.x,
        ai.y,
        ai.width,
        ai.height
    );

    drawBall();
}

function gameLoop(){

    update();
    render();

    requestAnimationFrame(gameLoop);
}

resetBall();
gameLoop();

</script>

</body>
</html>
"""

st.title("🏓 Pong Game")
st.write("🖱️ 마우스를 움직여 패들을 조작하세요")

components.html(html, height=540)
