import turtle
import random
import time

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 600, 400
DELAY = 0.1

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


# ---------------- SCOREBOARD ----------------
class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.color("white")
        self.writer.goto(0, HEIGHT // 2 - 40)
        self.update()

    def increase(self):
        self.score += 1
        self.update()

    def update(self):
        self.writer.clear()
        self.writer.write(
            f"Score: {self.score}",
            align="center",
            font=("Arial", 16, "bold")
        )

    def reset(self):
        self.score = 0
        self.update()


# ---------------- FOOD ----------------
class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.speed(0)
        self.spawn()

    def spawn(self):
        x = random.randint(-WIDTH // 20 + 1, WIDTH // 20 - 1) * 20
        y = random.randint(-HEIGHT // 20 + 1, HEIGHT // 20 - 1) * 20
        self.food.goto(x, y)


# ---------------- SNAKE ----------------
class Snake:
    def __init__(self):
        self.segments = []
        self.direction = RIGHT
        self.create()

    def create(self):
        for i in range(3):
            self.add_segment(-i * 20, 0)

    def add_segment(self, x, y):
        seg = turtle.Turtle()
        seg.shape("square")
        seg.color("green")
        seg.penup()
        seg.goto(x, y)
        self.segments.append(seg)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].goto(
                self.segments[i - 1].xcor(),
                self.segments[i - 1].ycor()
            )

        head = self.segments[0]

        if self.direction == UP:
            head.sety(head.ycor() + 20)
        elif self.direction == DOWN:
            head.sety(head.ycor() - 20)
        elif self.direction == LEFT:
            head.setx(head.xcor() - 20)
        elif self.direction == RIGHT:
            head.setx(head.xcor() + 20)

    def grow(self):
        tail = self.segments[-1]
        self.add_segment(tail.xcor(), tail.ycor())

    def set_direction(self, d):
        opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if d != opposite[self.direction]:
            self.direction = d

    def hit_wall(self):
        h = self.segments[0]
        return (
            h.xcor() < -WIDTH // 2
            or h.xcor() > WIDTH // 2 - 20
            or h.ycor() < -HEIGHT // 2
            or h.ycor() > HEIGHT // 2 - 20
        )

    def hit_self(self):
        h = self.segments[0]
        return any(h.distance(s) < 20 for s in self.segments[1:])


# ---------------- GAME ----------------
class SnakeGame:
    def __init__(self, player_name):
        self.player_name = player_name

        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title(f"Snake Game - {player_name}")
        self.screen.tracer(0)

        self.snake = Snake()
        self.food = Food()
        self.score = ScoreBoard()
        self.running = True

        # controls
        self.screen.listen()
        self.screen.onkey(lambda: self.snake.set_direction(UP), "Up")
        self.screen.onkey(lambda: self.snake.set_direction(DOWN), "Down")
        self.screen.onkey(lambda: self.snake.set_direction(LEFT), "Left")
        self.screen.onkey(lambda: self.snake.set_direction(RIGHT), "Right")

    def check_food(self):
        h = self.snake.segments[0]
        if h.distance(self.food.food) < 20:
            self.snake.grow()
            self.food.spawn()
            self.score.increase()

    def game_over(self):
        self.running = False
        self.screen.clear()
        self.screen.bgcolor("black")

        msg = turtle.Turtle()
        msg.hideturtle()
        msg.color("red")

        msg.penup()
        msg.goto(0, 80)
        msg.write("GAME OVER", align="center", font=("Arial", 30, "bold"))

        msg.goto(0, 30)
        msg.color("white")
        msg.write(f"Player: {self.player_name}", align="center", font=("Arial", 16, "normal"))

        msg.goto(0, 0)
        msg.write(f"Score: {self.score.score}", align="center", font=("Arial", 16, "normal"))

        msg.goto(0, -120)
        msg.write("Choose an option", align="center", font=("Arial", 14, "italic"))

        # ---------------- BUTTONS ----------------
        try_btn = turtle.Turtle()
        try_btn.shape("square")
        try_btn.color("green")
        try_btn.shapesize(2, 6)
        try_btn.penup()
        try_btn.goto(-100, -60)

        try_txt = turtle.Turtle()
        try_txt.hideturtle()
        try_txt.color("white")
        try_txt.penup()
        try_txt.goto(-100, -70)
        try_txt.write("TRY AGAIN", align="center", font=("Arial", 12, "bold"))

        exit_btn = turtle.Turtle()
        exit_btn.shape("square")
        exit_btn.color("red")
        exit_btn.shapesize(2, 6)
        exit_btn.penup()
        exit_btn.goto(100, -60)

        exit_txt = turtle.Turtle()
        exit_txt.hideturtle()
        exit_txt.color("white")
        exit_txt.penup()
        exit_txt.goto(100, -70)
        exit_txt.write("EXIT", align="center", font=("Arial", 12, "bold"))

        # ---------------- ACTIONS ----------------
        def restart(x, y):
            self.screen.bye()
            time.sleep(0.3)
            main_menu()

        def exit_game(x, y):
            self.screen.bye()

        try_btn.onclick(restart)
        exit_btn.onclick(exit_game)

        self.screen.mainloop()

    def run(self):
        while self.running:
            self.screen.update()
            self.snake.move()
            self.check_food()

            if self.snake.hit_wall() or self.snake.hit_self():
                self.game_over()

            time.sleep(DELAY)


# ---------------- MAIN MENU ----------------
def main_menu():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Snake Game Menu")

    title = turtle.Turtle()
    title.hideturtle()
    title.color("white")
    title.write(
        "SNAKE GAME\nPress ENTER to Start",
        align="center",
        font=("Arial", 18, "bold")
    )

    screen.listen()

    def start():
        screen.clear()
        name = screen.textinput("Player Name", "Enter your name:")
        if not name:
            name = "Player"

        game = SnakeGame(name)
        game.run()

    screen.onkey(start, "Return")
    screen.mainloop()


# ---------------- RUN ----------------
if __name__ == "__main__":
    main_menu()