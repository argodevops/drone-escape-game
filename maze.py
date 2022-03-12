import turtle
import math
from time import *
import pygame
from pygame.locals import *
import json
import random

pygame.mixer.init()
pygame.mixer.music.load("./Music/SoundTest.wav")
pygame.mixer.music.play(-1)

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Zombie head adventure")
wn.setup(1700, 700)
wn.tracer(0)
wn.bgpic("./image/giphy.gif")

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

class Player(turtle.Turtle):
    """
    Moves the player object

    Args:
        turtle (_type_): turtle object
    """
    def __init__(self):
        turtle.Turtle.__init__(self)
        v = self.getscreen()
        v.register_shape("./image/zombie.gif")
        self.shape("./image/zombie.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = player.xcor() + 24
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

# TODO - add input textbox area
class TextBox:
    def __init__(self, x=250, y=250, w=300, h=50, pen: turtle.Turtle = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if pen is not None:
            self.pen = pen
        else:
            self.pen = turtle.Turtle
            self.pen.hideturtle()
            self.pen.penup()
            self.pen.color("white")
                
        
# TODO add in moving enemy
# class Enemy(turtle.Turtle):
#         def __init__(self,x,y):
#                 turtle.Turtle.__init__(self)
#                 self.shape("square")
#                 self.color("purple")
#                 self.penup()
#                 self.speed(0)
#                 self.gold = 25
#                 self.goto(x, y)
#                 self.direction= random.choice(["up","down","left","right"])

#         def move(self):
#                 if self.direction =="up":
#                         dx = 0
#                         dy= 24
#                 elif self.direction =="down":
#                         dx = 0
#                         dy = -24
#                 elif self.direction =="right":
#                         dx = -24
#                         dy = 0
#                 elif self.direction == "left":
#                         dx= 24
#                         dy= 0
#                 else:
#                         dx = 0
#                         dy = 0

#                 move_to_x = self.xcor() + dx
#                 move_to_y = self.ycor() +dy

#                 if(move_to_x, move_to_y) not in walls:
#                         self.goto(move_to_x,move_to_y)
#                 else:
#                         self.direction = random.choice()["up","down","left","right"]

#                 turtle.ontimer(self.move, t=random.randint (100,300))

#         def destroy(self):
#                 self.goto(2000,2000)
#                 self.hideturtle()

def load_maps():
    with open('./assets/mazes.json') as w:
        return json.load(w)

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
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

# TODO This needs a refactor!! Is it needed...
def Starttime():
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
        turtle.write("\nRespawn in 5 seconds",align="right",font=(0.0000001))
        turtle.goto(2000,2000)


        i = 5      
        while i> -1:
                i-=1
                x = turtle.Turtle()
                x.pencolor= ("blue")
                x.goto(0,0)
                x.write(i+1,font=(0.0000001))
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

    pen = Pen()
    player = Player()
    walls = []
    treasures = []

    # TODO setup a randomly selected maze
    maps = load_maps()
    setup_maze(random.choice(maps))
#     turtle.textinput("title", "prompt")
    text = 'this text is editable'
    pygame.init()
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
    wn.tracer(0)

    while True:
        for treasure in treasures:
            if player.is_collision(treasure):
                player.gold += treasure.gold
                Gold_left = Gold_left-1
                print(Gold_left)
                if player.gold == 100:
                    Starttime()
                else:
                    turtle.clear()
                    turtle.goto(-50,300)
                    turtle.write("Player Gold:{}".format(player.gold),align="right",font=(0.0000001))
                    turtle.goto(2000,2000)
                    treasure.destroy()
                    # treasures.remove(Treasure)
                    wn.update()

            wn.update()
