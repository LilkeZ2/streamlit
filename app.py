import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pong Game", layout="centered")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body{
    margin:0;
    background:black;
    overflow:hidden;
}
canvas{
    display:block;
    margin:auto;
    background:black;
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

let playerScore = 0;
let aiScore = 0;

const player = {
    x: 20,
    y: canvas.height/2 - paddleHeight/2,
    width: paddleWidth,
    height: paddleHeight,
    speed: 8
};

const ai = {
    x: canvas.width - 32,
    y: canvas.height/2 - paddleHeight/2,
    width: paddleWidth,
    height: paddleHeight,
    speed: 5
};

const ball = {
    x: canvas.width/2,
    y: canvas.height/2,
    radius: 10,
    vx: 5,
    vy: 3
};

const keys = {};

document.addEventListener("keydown", (e)=>{
    keys[e.key.toLowerCase()] = true;
});

document.addEventListener("keyup", (e)=>{
    keys[e.key.toLowerCase()] = false;
});

function resetBall(){
    ball.x = canvas.width/2;
    ball.y = canvas.height/2;

    let direction = Math.random() > 0.5 ? 1 : -1;

    ball.vx = 5 * direction;
    ball.vy = (Math.random()*4)-2;
}

function drawRect(x,y,w,h){
    ctx.fillStyle = "white";
    ctx.fillRect(x,y,w,h);
}

function drawBall(){
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
    ctx.fillStyle = "white";
    ctx.fill();
}

function drawNet(){
    for(let i=0;i<canvas.height;i+=30){
        drawRect(canvas.width/2-1, i, 2, 18);
    }
}

function drawScore(){
    ctx.fillStyle = "white";
    ctx.font = "40px Arial";

    ctx.fillText(
        playerScore,
        canvas.width/4,
        50
    );

    ctx.fillText(
        aiScore,
        canvas.width*3/4,
        50
    );
}

function collision(ball,paddle){
    return (
        ball.x - ball.radius < paddle.x + paddle.width &&
        ball.x + ball.radius > paddle.x &&
        ball.y - ball.radius < paddle.y + paddle.height &&
        ball.y + ball.radius > paddle.y
    );
}

function update(){

    // 플레이어 이동
    if(keys["w"]){
        player.y -= player.speed;
    }

    if(keys["s"]){
        player.y += player.speed;
    }

    player.y = Math.max(
        0,
        Math.min(canvas.height-player.height, player.y)
    );

    // AI 이동
    let aiCenter = ai.y + ai.height/2;

    if(aiCenter < ball.y - 15){
        ai.y += ai.speed;
    }
    else if(aiCenter > ball.y + 15){
        ai.y -= ai.speed;
    }

    ai.y = Math.max(
        0,
        Math.min(canvas.height-ai.height, ai.y)
    );

    // 공 이동
    ball.x += ball.vx;
    ball.y += ball.vy;

    // 위아래 벽
    if(
        ball.y - ball.radius <= 0 ||
        ball.y + ball.radius >= canvas.height
    ){
        ball.vy *= -1;
    }

    // 왼쪽 패들
    if(collision(ball,player)){

        ball.vx = Math.abs(ball.vx);

        let impact =
        (ball.y - (player.y + player.height/2))
        /(player.height/2);

        ball.vy = impact * 6;
    }

    // 오른쪽 패들
    if(collision(ball,ai)){

        ball.vx = -Math.abs(ball.vx);

        let impact =
        (ball.y - (ai.y + ai.height/2))
        /(ai.height/2);

        ball.vy = impact * 6;
    }

    // 점수 처리
    if(ball.x < -20){
        aiScore++;
        resetBall();
    }

    if(ball.x > canvas.width + 20){
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

    // 플레이어
    drawRect(
        player.x,
        player.y,
        player.width,
        player.height
    );

    // AI
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
st.write("W = 위  |  S = 아래")

components.html(html, height=550)
