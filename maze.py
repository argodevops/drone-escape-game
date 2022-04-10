import turtle
import math
from time import time, localtime, sleep
import pygame
#from pygame.locals import *
import json
import random
import sys

STEP_COUNT = 24

class Pen(turtle.Turtle):
    """
    Draws the maze

    Args:
        turtle (_type_): turtle object
    """
    def  __init__(self):
        turtle.Turtle.__init__(self)
        v = self.getscreen()
        v.register_shape("./image/block.gif")
        self.shape("./image/block.gif")
        self.color("white")
        self.penup()
        self.speed(3)

class Drone(turtle.Turtle):
    """
    Moves the drone object

    Args:
        turtle (_type_): turtle object
    """
    def __init__(self):
        turtle.Turtle.__init__(self)
        v = self.getscreen()
        v.register_shape("./image/drone.gif")
        self.shape("./image/drone.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self, count=1):
        move_to_x = player.xcor()
        move_to_y = player.ycor() + (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self, count=1):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self, count=1):
        move_to_x = player.xcor() - (count * STEP_COUNT)
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self, count=1):
        move_to_x = player.xcor() + (count * STEP_COUNT)
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    # TODO - use collision
    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    """
    A treasure object

    Args:
        turtle (_type_): turtle object
    """
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        v = self.getscreen()
        v.register_shape("./image/treasure.gif")
        self.shape("./image/treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Button:
    def __init__(self, message: str, x=-500, y=100, w=150, h=50):
        self.message = message
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def render(self, pen: turtle.Turtle):
        pen.penup()
        pen.color("black", "green")
        pen.begin_fill()
        pen.goto(self.x, self.y)
        pen.goto(self.x + self.w, self.y)
        pen.goto(self.x + self.w, self.y + self.h)
        pen.goto(self.x, self.y + self.h)
        pen.goto(self.x, self.y)
        pen.end_fill()
        pen.goto(self.x + 15, self.y + 15)
        pen.write(self.message, font = ('Arial', 15, 'normal'));      

def load_maps():
    with open('./assets/mazes.json') as w:
        return json.load(w)

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            print(f"Parsing position {x}, {y}: {character}")
            maze_x = -288 + (x * 24)
            maze_y = 288 - (y * 24)

            if character == "X":
                pen.goto(maze_x, maze_y)
                pen.stamp()
                walls.append((maze_x, maze_y))
            elif character == "P":
                player.goto(maze_x, maze_y)
            elif character == "T":
                treasures.append(Treasure(maze_x, maze_y))
            elif character == "G":
                # TODO: Make this trigger the win
                print(f"Goal defined at {x}, {y}")
    wn.update()

def button_click():
    pass

# TODO This needs a refactor!! Is it needed...
def start_time():
        treasure.destroy()
        treasures.remove(treasure)
        wn.update()

        pygame.mixer.music.load("./Music/Gameover.wav")
        pygame.mixer.music.play(4)

        start_timer = time()

        struct = localtime(start_timer)


        turtle.onscreenclick(None)
        turtle.speed(0)
        turtle.penup()
        turtle.goto(10,300)
        turtle.color("red")
        turtle.write(" It's a fake gold!!! In to laggy mode!!!",align="left", font=(10))
        turtle.goto(-50,300)
        turtle.write("\nRespawn in 5 seconds",align="right", font=(0.0000001))
        turtle.goto(2000,2000)


        i = 5      
        while i> -1:
                i-=1
                x = turtle.Turtle()
                x.pencolor= ("blue")
                x.goto(0,0)
                x.write(i+1, font=(0.0000001))
                x.penup()
                x.goto(2000,2000)
                sleep(1)
                wn.update()
                x.clear()
        end_timer = time()
        pygame.mixer.music.load("./Music/SoundTest.wav")
        pygame.mixer.music.play(-1)
        turtle.clear()


if __name__ == "__main__":
    
    # Set up window
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Drone commander")
    wn.setup(1700, 700)
    wn.tracer(0)
    wn.bgpic("./image/giphy.gif")

    # Play annoying music
    pygame.mixer.init()
    pygame.mixer.music.load("./Music/SoundTest.wav")
    pygame.mixer.music.play(-1)

    # Initialise stuff
    pen = Pen()
    player = Drone()
    start_button = Button("Start Game", -500, 100, 150, 50).render(pen)
    reset_button = Button("Reset Game", -500, -100, 150, 50).render(pen)
    walls = []
    treasures = []

    # Set up maze    
    maps = load_maps()
    map_index = random.randrange(len(maps))
    print(f"Setting up map using map: {map_index}")
    setup_maze(maps[map_index])
    print("Map has been setup")

    text = 'this text is editable'
    pygame.init()
    print("Game has been initialised")
    sysfont = pygame.font.get_default_font()
    font = pygame.font.SysFont(None, 48)

    img = font.render(text, True, (0, 255, 255))
 
    # TODO turn off keypress and read commands from input
    turtle.listen()
    turtle.onkey(player.go_left,"Left")
    turtle.onkey(player.go_right,"Right")
    turtle.onkey(player.go_up,"Up")
    turtle.onkey(player.go_down,"Down")

    Gold_left = 3

    while True:
        for treasure in treasures:
            if player.is_collision(treasure):
                player.gold += treasure.gold
                Gold_left = Gold_left-1
                print(Gold_left)
                if player.gold == 100:
                    start_time()
                else:
                    turtle.clear()
                    turtle.goto(-50,300)
                    turtle.write("Player Gold:{}".format(player.gold),align="right",font=(0.0000001))
                    turtle.goto(2000,2000)
                    treasure.destroy()
                    wn.update()
            try:
                wn.update()
            except Exception:
                print("Exit game")
                sys.exit(0)
