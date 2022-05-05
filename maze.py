""" Drone Maze Game """
import turtle
import math
import time
import json
import random
import re
import sys
import pygame
from numpy import array
from drone import Drone

class Pen(turtle.Turtle):
    """
    Draws the maze

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self):
        """_summary_
        """
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/block.gif")
        self.shape("./image/block.gif")
        self.color("white")
        self.penup()
        self.speed(3)

class Treasure(turtle.Turtle):
    """
    A treasure object

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/treasure.gif")
        self.shape("./image/treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        """_summary_
        """
        self.goto(2000, 2000)
        self.hideturtle()


class Button:
    """
    A button object
    """

    def __init__(
            self,
            message: str,
            pos_x=-500,
            pos_y=100,
            pos_w=150,
            pos_h=50):
        self.message = message
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_w = pos_w
        self.pos_h = pos_h

    def render(self, turtle: turtle.Turtle):
        """_summary_

        Args:
            turtle (turtle.Turtle): _description_
        """
        turtle.penup()
        turtle.color("black", "green")
        turtle.begin_fill()
        turtle.goto(self.pos_x, self.pos_y)
        turtle.goto(self.pos_x + self.pos_w, self.pos_y)
        turtle.goto(self.pos_x + self.pos_w, self.pos_y + self.pos_h)
        turtle.goto(self.pos_x, self.pos_y + self.pos_h)
        turtle.goto(self.pos_x, self.pos_y)
        turtle.end_fill()
        turtle.goto(self.pos_x + 15, self.pos_y + 15)
        turtle.write(self.message, font=("Courier", 18))


def load_maps():
    """_summary_

    Returns:
        _type_: _description_
    """
    with open('./assets/mazes.json') as maze_file:
        return json.load(maze_file)


def setup_maze(level: array):
    """_summary_

    Args:
        level (array): _description_
    """
    for pos_y in range(len(level)):
        for pos_x in range(len(level[pos_y])):
            character = level[pos_y][pos_x]
            #print(f"Parsing position {pos_x}, {pos_y}: {character}")
            maze_x = -288 + (pos_x * 24)
            maze_y = 288 - (pos_y * 24)

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
                print(f"Goal defined at {pos_x}, {pos_y}")
    wn.update()

    #canvas = turtle.getcanvas()
    #canvas.bind('<Motion>', on_click)


def on_click(event):
    """_summary_

    Args:
        event (_type_): _description_
    """
    pos_x, pos_y = event.x, event.y
    print('x={}, y={}'.format(pos_x, pos_y))
    # TODO capture start/reset button clicks
    # if (x >= 600 and x <= 800) and (  y >= 280 and y <= 300):
    #     turtle.onscreenclick(lambda x, y: turtle.bgcolor('red'))


# def countdown_timer():
#     """_summary_
#     """
#     turtle.speed(0)
#     turtle.penup()
#     turtle.clear()
#     turtle.goto(-500, 150)
#     turtle.write((str(int(time.time() - start))) + " seconds", font=("Courier", 18))

# TODO This needs a refactor!! Is it needed...
def start_time():
    """_summary_
    """

    treasure.destroy()
    treasures.remove(treasure)
    wn.update()

    pygame.mixer.music.load("./Music/Gameover.wav")
    pygame.mixer.music.play(4)

    #start_timer = time()

    #struct = time.localtime(start_timer)

    turtle.speed(0)
    turtle.penup()
    turtle.goto(10, 300)
    turtle.color("red")
    turtle.write(
        " It's a fake gold!!! In to laggy mode!!!",
        align="left",
        font=(10))
    turtle.goto(-50, 300)
    turtle.write("\nRespawn in 5 seconds", align="right", font=(0.0000001))
    turtle.goto(2000, 2000)

    i = 5
    while i > -1:
        i -= 1
        screen = turtle.Turtle()
        screen.pencolor = ("blue")
        screen.goto(0, 0)
        screen.write(i + 1, font=(0.0000001))
        screen.penup()
        screen.goto(2000, 2000)
        time.sleep(1)
        wn.update()
        screen.clear()
    pygame.mixer.music.load("./Music/SoundTest.wav")
    pygame.mixer.music.play(-1)
    turtle.clear()


def move_drone(player: Drone):
    """_summary_
        Read commands and move drone
    Args:
        player (Drone): _description_
    """
    speed = 1
    with open('assets/sample_commands.txt') as instructions:
        for instruction in instructions:
            (command, value) = tuple(re.split(' ', instruction.strip()))
            if command.upper() == 'TURN':
                player.turn(value)
            elif command.upper() == 'MOVE':
                for _ in range(0, int(value)):
                    time.sleep(speed)
                    if not player.move():
                        turtle.penup()
                        turtle.goto(-100, 300)
                        turtle.color("red")
                        turtle.write(
                            "GAME OVER", align="left", font=(
                                "Courier", 18))
                        turtle.goto(2000, 2000)
                        return False
    return True


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
    #pygame.mixer.music.load("./Music/SoundTest.wav")
    #pygame.mixer.music.play(-1)

    # Initialise buttons, timer, etc
    pen = Pen()
    start = time.time()
    start_button = Button("Start Game", -500, 100, 150, 50).render(pen)
    reset_button = Button("Reset Game", -500, 20, 150, 50).render(pen)

    walls = []
    treasures = []

    # Set up maze
    maps = load_maps()
    map_index = random.randrange(len(maps))
    print(f"Setting up map using map: {map_index}")
    player = Drone(walls)
    setup_maze(maps[map_index])
    print("Map has been setup")
    gold_left = 3
    start_game = True

    while True:
        # for treasure in treasures:
        #     if player.is_collision(treasure):
        #         player.gold += treasure.gold
        #         gold_left = gold_left - 1
        #         print(gold_left)
        #         if player.gold == 100:
        #             start_time()
        #         else:
        #             turtle.clear()
        #             turtle.goto(-50, 300)
        #             turtle.write(
        #                 f"Player Gold:{player.gold}",
        #                 font=(0.0000001))
        #             turtle.goto(2000, 2000)
        #             treasure.destroy()
        #             wn.update()
        try:
            wn.update()
            if start_game:
                move_drone(player)
                start_game = False
        except Exception:
            print("Exit game")
            sys.exit(0)
