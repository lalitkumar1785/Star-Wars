import turtle
import math
import random
import  time

# Set up the screen
window = turtle.Screen()
window.setup(width=600, height=600)
window.title("Star Wars Game")
window.bgcolor("black")
window.tracer(0)

# Register shapes
vertex = ((0, 15), (-15, 0), (-18, 5), (-18, -5), (0, 0), (18, -5), (18, 5), (15, 0))
window.register_shape("player", vertex)
asVertex = ((0, 10), (5, 7), (3, 3), (10, 0), (7, 4), (8, -6), (0, -10), (-5, -5), (-7, -7), (-10, 0), (-5, 4), (-1, 8))
window.register_shape("chattan", asVertex)

class Lalit(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()

def lalit1(t1, t2):
    x1 = t1.xcor()
    y1 = t1.ycor()
    x2 = t2.xcor()
    y2 = t2.ycor()
    taauko = math.atan2(y1 - y2, x1 - x2)
    taauko = taauko * 180.0 / 3.14159
    return taauko

def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < 20

# Create player
player = Lalit()
player.color("white")
player.shape("player")
player.score = 0
player.lives = 3

# Create missile
missile = Lalit()
missile.color("red")
missile.shape("arrow")
missile.speed = 20
missile.state = "ready"
missile.hideturtle()

# Cooldown time for firing missiles
cooldown_time = 1 # seconds
last_fire_time = 0

# Create enemies
enemies = []
for _ in range(5):
    enemy = Lalit()
    enemy.color("orange")
    enemy.shape("chattan")
    enemy.speed = random.randint(1, 2)
    enemy.goto(random.randint(-290, 290), random.randint(100, 290))
    enemies.append(enemy)

# Create score pen
pen = Lalit()
pen.color("white")
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0 Lives: 3", False, align="center", font=("Arial", 24, "normal"))

# Define player movement
def move_left():
    x = player.xcor()
    x -= 15
    if x < -290:
        x = -290
    player.setx(x)

def move_right():
    x = player.xcor()
    x += 15
    if x > 290:
        x = 290
    player.setx(x)

def move_up():
    y = player.ycor()
    y += 15
    if y > 290:
        y = 290
    player.sety(y)

def move_down():
    y = player.ycor()
    y -= 15
    if y < -290:
        y = -290
    player.sety(y)

# Define missile firing with cooldown
def fire_missile():
    global last_fire_time
    current_time = time.time()
    if missile.state == "ready" and (current_time - last_fire_time) > cooldown_time:
        missile.state = "fired"
        x = player.xcor()
        y = player.ycor() + 10
        missile.goto(x, y)
        missile.showturtle()
        last_fire_time = current_time

# Update the score display
def update_score():
    pen.clear()
    pen.write(f"Score: {player.score} Lives: {player.lives}", False, align="center", font=("Arial", 24, "normal"))

# Game over
def game_over():
    pen.goto(0, 0)
    pen.write("Game Over", False, align="center", font=("Arial", 36, "normal"))
    for enemy in enemies:
        enemy.hideturtle()
    player.hideturtle()
    missile.hideturtle()
    window.update()
    window.bye()  # Close the window after displaying Game Over message

# Keyboard bindings
window.listen()
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")
window.onkey(fire_missile, "space")

# Start time
start_time = time.time()

# Main game loop
while True:
    window.update()

    # Move the missile
    if missile.state == "fired":
        missile.sety(missile.ycor() + missile.speed)
    if missile.ycor() > 290:
        missile.hideturtle()
        missile.state = "ready"

    # Move the enemies
    for enemy in enemies:
        enemy.sety(enemy.ycor() - enemy.speed)
        if enemy.ycor() < -290:
            enemy.goto(random.randint(-290, 290), random.randint(100, 290))
            player.lives -= 1
            update_score()
            if player.lives == 0:
                game_over()

        # Check for collision between missile and enemy
        if is_collision(missile, enemy):
            missile.hideturtle()
            missile.state = "ready"
            missile.goto(0, -400)
            enemy.goto(random.randint(-290, 290), random.randint(100, 290))
            player.score += 10
            update_score()

        # Check for collision between player and enemy
        if is_collision(player, enemy):
            enemy.goto(random.randint(-290, 290), random.randint(100, 290))
            player.lives -= 1
            update_score()
            if player.lives == 0:
                game_over()

    # Check for game timer
    elapsed_time = time.time() - start_time
    if elapsed_time >= 10:
        game_over()
