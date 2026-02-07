import js
import random
from pyodide.ffi import create_proxy


canvas = js.document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")
canvas.width = 400
canvas.height = 600


js.document.getElementById("loading").style.display = "none"

score = 0
game_active = True
frames = 0
obstacles = []

class Player:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = (canvas.width / 2) - (self.width / 2)
        self.y = canvas.height - 60
        self.speed = 7
        self.dx = 0

    def draw(self):
        ctx.shadowBlur = 15
        ctx.shadowColor = "#00f2ff"
        ctx.fillStyle = "#00f2ff"
        ctx.fillRect(self.x, self.y, self.width, self.height)
        ctx.shadowBlur = 0

    def update(self):
        self.x += self.dx
        if self.x < 0: self.x = 0
        if self.x + self.width > canvas.width: self.x = canvas.width - self.width

class Obstacle:
    def __init__(self):
        self.size = random.randint(20, 40)
        self.x = random.random() * (canvas.width - self.size)
        self.y = -self.size
        self.speed = random.uniform(2, 4) + (score / 1000)

    def update(self):
        self.y += self.speed

    def draw(self):
        ctx.shadowBlur = 10
        ctx.shadowColor = "#ff0055"
        ctx.fillStyle = "#ff0055"
        ctx.fillRect(self.x, self.y, self.size, self.size)
        ctx.shadowBlur = 0

player = Player()

def on_keydown(event):
    if event.key in ["ArrowLeft", "a", "A"]: player.dx = -player.speed
    if event.key in ["ArrowRight", "d", "D"]: player.dx = player.speed

def on_keyup(event):
    if event.key in ["ArrowLeft", "ArrowRight", "a", "d", "A", "D"]: player.dx = 0

keydown_proxy = create_proxy(on_keydown)
keyup_proxy = create_proxy(on_keyup)
js.window.addEventListener("keydown", keydown_proxy)
js.window.addEventListener("keyup", keyup_proxy)

def game_loop(timestamp):
    global score, game_active, frames
    if not game_active: return

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    # Сітка
    ctx.strokeStyle = "#111"
    for i in range(0, canvas.width, 40):
        ctx.beginPath()
        ctx.moveTo(i, 0)
        ctx.lineTo(i, canvas.height)
        ctx.stroke()

    player.update()
    player.draw()

    frames += 1
    if frames % 60 == 0:
        obstacles.append(Obstacle())

    for obs in obstacles[:]:
        obs.update()
        obs.draw()
        if (player.x < obs.x + obs.size and
            player.x + player.width > obs.x and
            player.y < obs.y + obs.size and
            player.y + player.height > obs.y):
            game_active = False
            js.document.getElementById("game-over").style.display = "block"
            js.document.getElementById("final-score").innerText = str(score)
        if obs.y > canvas.height:
            obstacles.remove(obs)
            score += 10
            js.document.getElementById("score").innerText = str(score)

    if frames % 10 == 0:
        score += 1
        js.document.getElementById("score").innerText = str(score)

    js.requestAnimationFrame(create_proxy(game_loop))

js.requestAnimationFrame(create_proxy(game_loop))