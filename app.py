import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🏓 Pong Game", layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html, body{
    margin:0;
    overflow:hidden;
    background:black;
}

#menu,#gameOver{
    position:absolute;
    top:0; left:0;
    width:100%; height:100%;
    background:black;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    color:white;
}

#gameOver{ display:none; z-index:200; }
#menu{ z-index:100; }

#menu h1,#gameOver h1{
    font-size:48px;
    font-family:Arial,sans-serif;
    font-weight:bold;
    margin-bottom:25px;
}

#menu button,#gameOver button{
    width:220px;
    height:60px;
    margin:10px;
    font-size:24px;
    font-family:Arial,sans-serif;
    font-weight:bold;
    cursor:pointer;
}

#menu p{
    margin-top:20px;
    font-size:24px;
    font-family:Arial,sans-serif;
    font-weight:bold;
    color:white;
}

canvas{
    display:block;
    margin:auto;
    background:black;
    border:2px solid white;
    cursor:default;
}
</style>
</head>
<body>

<div id="menu">
    <h1>Pong Game</h1>
    <button onclick="startGame('normal')">보통</button>
    <button onclick="startGame('hard')">어려움</button>
    <p>난이도를 선택해서 시작하세요</p>
</div>

<div id="gameOver">
    <h1 id="winnerText"></h1>
    <button onclick="returnToMenu()">다시 시작</button>
</div>

<canvas id="gameCanvas" width="900" height="500"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 14;
const paddleHeight = 100;

let BALL_SPEED = 9;
let AI_SPEED = 8;
let MAX_SPEED = 16;

let gameStarted = false;
let playerScore = 0;
let aiScore = 0;

const player = {
    x:20, y:200,
    width:paddleWidth,
    height:paddleHeight
};

const ai = {
    x:860, y:200,
    width:paddleWidth,
    height:paddleHeight,
    speed:AI_SPEED
};

const ball = {
    x:450, y:250,
    radius:10,
    vx:0, vy:0
};

function startGame(mode){
    playerScore = 0;
    aiScore = 0;

    if(mode === "normal"){
        BALL_SPEED = 9;
        AI_SPEED = 8;
        MAX_SPEED = 16;
    } else {
        BALL_SPEED = 11.7;
        AI_SPEED = 12;
        MAX_SPEED = 20;
    }

    ai.speed = AI_SPEED;

    document.getElementById("menu").style.display = "none";
    document.getElementById("gameOver").style.display = "none";

    resetBall();
    gameStarted = true;
}

canvas.addEventListener("mousemove",(e)=>{
    const rect = canvas.getBoundingClientRect();
    const mouseY = e.clientY - rect.top;

    player.y = mouseY - player.height/2;
    player.y = Math.max(0, Math.min(canvas.height-player.height, player.y));
});

function resetBall(){
    ball.x = canvas.width/2;
    ball.y = canvas.height/2;

    const dir = Math.random() > 0.5 ? 1 : -1;

    ball.vx = BALL_SPEED * dir;
    ball.vy = (Math.random()*8)-4;
}

function endGame(winner){
    gameStarted = false;
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOver").style.display = "flex";
}

function returnToMenu(){
    playerScore = 0;
    aiScore = 0;
    ball.vx = 0;
    ball.vy = 0;

    document.getElementById("gameOver").style.display = "none";
    document.getElementById("menu").style.display = "flex";
}

function increaseSpeed(){
    ball.vx *= 1.03;
    ball.vy *= 1.03;

    const speed = Math.sqrt(ball.vx*ball.vx + ball.vy*ball.vy);

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
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
    ctx.fillStyle = "white";
    ctx.fill();
}

function drawNet(){
    for(let i=0;i<canvas.height;i+=30){
        drawRect(canvas.width/2-1,i,2,18);
    }
}

function drawScore(){
    ctx.fillStyle = "white";
    ctx.font = "42px Arial";
    ctx.fillText(playerScore, canvas.width/4, 60);
    ctx.fillText(aiScore, canvas.width*3/4, 60);
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
    const center = ai.y + ai.height/2;

    if(center < ball.y - 15) ai.y += ai.speed;
    else if(center > ball.y + 15) ai.y -= ai.speed;

    ai.y = Math.max(0, Math.min(canvas.height-ai.height, ai.y));

    ball.x += ball.vx;
    ball.y += ball.vy;

    if(ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height){
        ball.vy *= -1;
    }

    if(collision(ball, player)){
        ball.vx = Math.abs(ball.vx);
        const impact = (ball.y - (player.y + player.height/2)) / (player.height/2);
        ball.vy = impact * 8;
        increaseSpeed();
    }

    if(collision(ball, ai)){
        ball.vx = -Math.abs(ball.vx);
        const impact = (ball.y - (ai.y + ai.height/2)) / (ai.height/2);
        ball.vy = impact * 8;
        increaseSpeed();
    }

    if(ball.x < -30){
        aiScore++;
        if(aiScore >= 5) endGame("AI WIN!");
        else resetBall();
    }

    if(ball.x > canvas.width + 30){
        playerScore++;
        if(playerScore >= 5) endGame("YOU WIN!");
        else resetBall();
    }
}

function render(){
    ctx.clearRect(0,0,canvas.width,canvas.height);

    drawNet();
    drawScore();

    drawRect(player.x, player.y, player.width, player.height);
    drawRect(ai.x, ai.y, ai.width, ai.height);

    drawBall();
}

function gameLoop(){
    if(gameStarted) update();
    render();
    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

st.title("🏓 Pong Game")
st.write("🖱️ 마우스로 패들을 움직이세요")

components.html(html, height=540)
