"""Maze module."""
from turtle import RawTurtle, TurtleScreen
from tkinter import *
from tkinter import scrolledtext
import sys
import time
import threading
import re
import json
import random
import pygame
from numpy import array
from drone import Drone
import messages


class Pen(RawTurtle):
    """
    Draws the maze

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self, screen):
        """_summary_
        """
        RawTurtle.__init__(self, screen)
        screen.register_shape("./image/block.gif")
        self.shape("./image/block.gif")
        self.color("white")
        self.penup()  # don't draw lines as turtle moves.
        self.speed(3)


class GameObject(RawTurtle):
    """
    Base game object.

    Args:
        RawTurtle (_type_): _description_
    """
    def __init__(self, pos_x, pos_y, screen):
        """
        Constructor

        Args:
            pos_x (_type_): _description_
            pos_y (_type_): _description_
            screen (_type_): _description_
        """
        super().__init__(screen)
        self.penup()
        self.speed(0)
        self.goto(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.active = True

    def destroy(self):
        """Destroy game object (but not really)
        """
        self.goto(2000, 2000)
        self.hideturtle()
        self.active = False

    def respawn(self):
        """Respawn and show game object
        """
        self.penup()
        self.goto(self.pos_x, self.pos_y)
        self.active = True
        self.showturtle()

    def get_x(self):
        """Get x coord

        Returns:
            _type_: _description_
        """
        return self.pos_x

    def get_y(self):
        """Get y coord

        Returns:
            _type_: _description_
        """
        return self.pos_y

    def is_active(self):
        """Is game object active

        Returns:
            _type_: _description_
        """
        return self.active


# could have destroyable blocks that the users can destroy with a drones gun?but that may be a bit... aggressive. But it'd
# give even more interesting possibilities.
class DoorKey(GameObject):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        screen.register_shape("./image/key.gif")
        self.shape("./image/key.gif")
        self.color("yellow")


class Door(GameObject):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        screen.register_shape("./image/door.gif")
        screen.register_shape("./image/opendoor.gif")
        self.shape("./image/door.gif")
        self.color("red")

    def destroy(self):
        self.active = False
        self.shape("./image/opendoor.gif")

    def respawn(self):
        self.active = True
        self.shape("./image/door.gif")


class Treasure(GameObject):
    """
    A treasure object

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        screen.register_shape("./image/speedarrow.gif")
        self.shape("./image/speedarrow.gif")
        self.color("gold")
        self.gold = 100


class Destructable(GameObject):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        screen.register_shape("./image/pink.gif")
        self.shape("./image/pink.gif")
        self.color("pink")


class Gun(GameObject):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        screen.register_shape("./image/laser.gif")
        self.shape("./image/laser.gif")
        self.color("grey")


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
    # don't draw lines as you draw the maze... but anim is disabled during
    # maze creation for "insta appear"
    pen.penup()
    player.hideturtle()
    for pos_y in range(len(level)):
        for pos_x in range(len(level[pos_y])):
            character = level[pos_y][pos_x]
            maze_x = -288 + (pos_x * 24)
            maze_y = 288 - (pos_y * 24)
            if character == "X":
                pen.goto(maze_x, maze_y)
                pen.stamp()
                walls.append((maze_x, maze_y))
            elif character == "P":
                player.reset()
                player.goto(maze_x, maze_y)
                player_pos.clear()
                player_pos.append(maze_x)
                player_pos.append(maze_y)
                player.showturtle()
            elif character == "A":
                global GAMEEXIT
                GAMEEXIT = [maze_x, maze_y]
            elif character == "T":
                treasures.append(Treasure(maze_x, maze_y, turtlescreen))
            elif character == "G":
                gun.append(Gun(maze_x, maze_y, turtlescreen))
            elif character == "D":
                destructibles.append(Destructable(
                    maze_x, maze_y, turtlescreen))
            elif character == "W":
                doors.append(Door(maze_x, maze_y, turtlescreen))
            elif character == "K":
                keys.append(DoorKey(maze_x, maze_y, turtlescreen))
            elif character == "G":
                # Now graphic or turtle here? Nor letting player know...
                print(f"Goal defined at {pos_x}, {pos_y}")
    turtlescreen.update()
    # was a debug to check we had correctly destroyed/created turtles.
    print("Turtles " + str(len(turtlescreen.turtles())))

# we aren't actually doing anything clicky but left in.


def on_click(event):
    """
    Event click

    Args:
        event (_type_): _description_
    """
    pos_x, pos_y = event.x, event.y
    print(f'x={pos_x}, y={pos_y}')


def gameover():
    """_summary_
        Just uses the turtle to write in red on the canvas/screen its attached to
    """
    turtle.penup()
    turtle.goto(-400, -100)
    turtle.color("red")
    turtle.write(
        "GAME OVER", align="left", font=(
            "Courier", 110))
    turtle.goto(2000, 2000)


def update_timer():
    print("update timer")
    while start_game:
        timerlabel['text'] = 'update....'
        time.sleep(1)
        print("update timer")


def start_timer():
    print("start timer")
    timer_thread = threading.Thread(target=update_timer)
    timer_thread.start()


def move_drone(player: Drone, instructions):
    """_summary_
        Read commands and move drone
    Args:
        player (Drone): _description_
    """
    start_timer()

    for instruction in instructions:
        if GAMEWON:
            continue
        # quick/dirty check to ignore empty lines. Prevents crash due to
        # players hitting "enter" after last entered command.
        if len(instruction) == 0:
            continue
        commands = tuple(re.split(' ', instruction.strip()))
        # append whatever command is about to be run into the executing box and
        # MOVE the box to end (scrollable box)
        print_executing_text(instruction)
        if commands[0].upper() == 'FIRE':
            player.shoot()
        elif commands[0].upper() == 'TURN':
            player.turn(commands[1])
        elif commands[0].upper() == 'MOVE':
            for _ in range(0, int(commands[1])):
                if player.xcor() == GAMEEXIT[0] and player.ycor(
                ) == GAMEEXIT[1]:
                    wingame()
                    return
                if not player.move():
                    gameover()
                    # could disable button but unnecessary as they don't move if dead.
                    # buttonrun["state"] = DISABLED
                    return False
        else:
            print_executing_text('Unknown command: ' + instruction)
            # could disable run button or highlight text red etc?
            player.dead()
            gameover()
            return False
        turtlescreen.update()
    return True

# take user input and run commands on the map (clear executingtext textbox first)
# performs check to ensure dead players can't move. Could disable run
# button instead when dead but...


def run():
    # check they're not just re-running commands without resetting after
    # failing.
    if player.player_dead():
        return
    clear_executing_text() # clear textbox
    # "get" apparently adds newline character to end, so get from start to -1 of end; splitlines splits around newline.
    commands_text = inputtext.get('1.0', 'end-1c').splitlines()
    if validate_command_text(commands_text):
        move_drone(player, commands_text)

# print executing text to end of list


def print_executing_text(text):
    executingtext.configure(state='normal')
    executingtext.insert(END, text + '\n')
    executingtext.update()
    executingtext.see("end")
    executingtext.configure(state='disabled')

def clear_executing_text():
    executingtext.configure(state='normal')
    executingtext.delete('1.0', END)
    executingtext.configure(state='disabled')

# validate command text. Don't execute commands if not valid.


def validate_command_text(commands_text):
    for command_text in commands_text:
        commands = re.split(' ', command_text.strip())
        command = commands[0].upper()
        if command == 'MOVE':
            if not commands[1].isnumeric():
                print_executing_text('Invalid command: ' + command_text)
                return False
        elif command == 'TURN':
            if commands[1].upper() not in ['RIGHT', 'LEFT']:
                print_executing_text('Invalid command: ' + command_text)
                return False
        elif command == 'FIRE':
            if len(commands) > 1:
                print_executing_text('Invalid Fire Paramteter: ' + command_text)
                return False
        else:
            print_executing_text('Unknown command: ' + command_text)
            return False
    return True

# just clear out text of commands/output


def clear():
    inputtext.delete('1.0', END)
    clear_executing_text()


def wingame():
    global GAMEWON
    GAMEWON = True
    # stop timer
    turtle.penup()
    turtle.goto(-350, -100)
    turtle.color("green")
    turtle.write(
        "YOU WIN!", align="left", font=(
            "Courier", 110))
    turtle.goto(2000, 2000)
    messages.win()

# Uses global player x/y that's set on the creation of maze to move player to maze start.
# Calls the respawn method on every other turtle (could create on Drone... If it retaind its original xy)
# Respawn moves existing turtles back to their original x/y given at creation. Turtles are just moved out of screen when "destroyed"
# Could therefore create extended class of RawTurtle that keeps x/y original and has these repetitive methods.
# but for quick hacky omitted for now.


def reset():
    # buttonrun["state"] = NORMAL # if you disable button, then this is how to
    # re-enable
    player.reset()
    player.goto(player_pos[0], player_pos[1])
    for treasure in treasures:
        treasure.respawn()
    for key in keys:
        key.respawn()
    for door in doors:
        door.respawn()
    for laser in gun:
        laser.respawn()
    for destructible in destructibles:
        destructible.respawn()
    global GAMEWON
    GAMEWON = False
    # this is the "game over" pen being cleared of any writing done.
    turtle.clear()

# Should remove commands entered/ran from Textboxes.
# It DESTROYS all turtle objects via calling clear on the screen. This means they need recreating.
# turtlescreen.clear therefore destroys player, treasures, doors, keys, and the wall drawing "pen" turtle.
# Must therefore create player, the turtle to draw the maze (the creation of maze creates treasures/doors/keys turtle)
# Therefore has to clear the lists that are passed to the player/drone
# Turtle prior to creating from map.


def startnew():
    # buttonrun["state"] = NORMAL
    clear()
    # clear DELETES all turtles... this includes player/pen turtles.
    turtlescreen.clear()
    turtlescreen.bgcolor("cyan")
    # turn off animation (for insta maze draw)
    turtlescreen.tracer(0)
    # since treasures turtles deleted, clear out globals.
    walls.clear()
    treasures.clear()
    destructibles.clear()
    gun.clear()
    # we need to refer to global pen/player lest fan and x attempt merge, and
    # so create new turtles
    global pen
    global player
    pen = Pen(turtlescreen)
    player = Drone(walls, keys, doors, treasures,
                   destructibles, gun, turtlescreen)
    canvas.tag_raise(player)
    # set up maze (also creates treasures turtles)
    setup_maze(maps[random.randrange(len(maps))])
    # Game over message printing, perhaps change this to something else.
    global turtle
    # as this is the "game over" message pen, associated with the screen,
    # recreate.
    turtle = RawTurtle(turtlescreen)
    turtle.penup()
    turtle.hideturtle()
    # turn back on the anims (updates).
    turtlescreen.tracer(1)
    global GAMEWON
    GAMEWON = False

# Incase of button to exit addition for now? Reality is you can just click
# X on window this is unnecessary...


# def exit():
#     sys.exit(0)


# main command?
# TODO extract out the load of map to function
if __name__ == "__main__":
    # set up properties
    root = Tk()
    root.title("Game")
    root.geometry('1650x950')
    # weights supposed to proportion available real-estate appropriately.
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=6)
    root.grid_columnconfigure(2, weight=2)
    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=5)
    root.grid_rowconfigure(2, weight=3)
    # bg colour just to see spaces on resize etc. Can make all uniform.
    frametop = Frame(root, height=50)
    framebottom = Frame(root, bg='orange')
    frameleft = Frame(root, bg='pink')
    frameright = Frame(root)
    frametop.grid(column=0, row=0, columnspan=3)
    framebottom.grid(column=1, row=2, sticky='nw')
    frameleft.grid(column=0, row=1, sticky='n')
    frameright.grid(column=2, row=1, sticky='n')

    # create top frame widget
    titlelabel = Label(frametop, text="Drone Escape", font=('Arial', 25))
    titlelabel.grid(column=0, row=0)
    label = Label(
        frametop, text="Write your commands in text box and click run")
    label.grid(column=0, row=1)

    # LEGEND -- long winded but...
    legendlabel = Label(frameright, text="Maze Legend",
                        font=('Arial', 15), height=2)
    legendlabel.grid(column=0, row=0)
    legend = Canvas(frameright)
    legend.grid(row=1, column=0, sticky='w')
    legend.config(width=350, height=650)
    # grab images
    droneimage = PhotoImage(file="./image/drone.gif")
    wallimage = PhotoImage(file="./image/block.gif")
    keyimage = PhotoImage(file="./image/key.gif")
    doorimage = PhotoImage(file="./image/door.gif")
    opendoorimage = PhotoImage(file="./image/opendoor.gif")
    treasureimage = PhotoImage(file="./image/speedarrow.gif")
    deaddrone = PhotoImage(file="./image/zombie.gif")
    laserimage = PhotoImage(file="./image/laser.gif")
    destructibleimage = PhotoImage(file="./image/pink.gif")
    # place image and associated text.
    legend.create_image(20, 20, image=droneimage, anchor=NW)
    legend.create_text(90, 25, text="Player Drone", anchor=NW)
    legend.create_image(20, 60, image=wallimage, anchor=NW)
    legend.create_text(90, 65, text="Maze Wall", anchor=NW)
    legend.create_image(20, 100, image=doorimage, anchor=NW)
    legend.create_text(90, 105, text="Door (require key)", anchor=NW)
    legend.create_image(20, 140, image=opendoorimage, anchor=NW)
    legend.create_text(90, 145, text="Open Door (can pass)", anchor=NW)
    legend.create_image(20, 180, image=keyimage, anchor=NW)
    legend.create_text(90, 185, text="Door Key", anchor=NW)
    legend.create_image(20, 220, image=treasureimage, anchor=NW)
    legend.create_text(90, 225, text="Speed Boost", anchor=NW)
    legend.create_image(20, 260, image=deaddrone, anchor=NW)
    legend.create_text(90, 265, text="Crashed Drone", anchor=NW)
    legend.create_image(20, 300, image=laserimage, anchor=NW)
    legend.create_text(90, 305, text="Drone Laser (pickup)", anchor=NW)
    legend.create_image(20, 340, image=destructibleimage, anchor=NW)
    legend.create_text(
        90, 345, text="Destructible Wall (need laser)", anchor=NW)

    # GAME CANVAS
    canvas = Canvas(root)
    canvas.grid(column=1, row=1, sticky='nw')
    canvas.config(width=900, height=700)

    # LEFT FRAME (Commands box + buttons)
    commandslabel = Label(
        frameleft, text="Commands Entry List", font=('Arial', 15))
    commandslabel.grid(column=0, row=0, sticky="new")
    inputtext = Text(frameleft, height=30, width=40)
    inputtext.grid(row=1, column=0)
    buttonrun = Button(frameleft, text="Run Commands", command=run)
    buttonrun.grid(row=2, column=0, sticky='ews')
    buttonclear = Button(frameleft, text="Clear Commands", command=clear)
    buttonclear.grid(row=3, column=0, sticky='ews')
    buttonreset = Button(frameleft, text='Reset Game', command=reset)
    buttonreset.grid(row=4, column=0, sticky='esw')
    buttonnewgame = Button(frameleft, text='New Game', command=startnew)
    buttonnewgame.grid(row=5, column=0, sticky='esw')
    timerlabel = Label(frameleft, text="Timer 00:00:00",
                       font=('Arial', 15), height=2)
    timerlabel.grid(row=8, column=0, sticky='esw')

    # BOTTOM FRAME (scrollable executing command window) -- simply indicates
    # last command incase of errors.
    executingtext = scrolledtext.ScrolledText(
        framebottom, height=10, width=112, wrap=WORD, state='disabled')
    executingtext.grid(row=0, column=0, sticky='news')

    # Game canvas screen setup.
    turtlescreen = TurtleScreen(canvas)
    turtlescreen.bgcolor("cyan")
    # Turtle that draws "Game over" message ON the game canvas.
    turtle = RawTurtle(turtlescreen)
    # turtle leaves an arrow when visble, so make invisible.
    turtle.hideturtle()

    # Play that funky music ...
    pygame.mixer.init()
    # pygame.mixer.music.load("./Music/SoundTest.wav")
    # pygame.mixer.music.play(-1)

    # globals -- this is from tutorial, with refactor it'd be better...
    GAMEEXIT = []
    walls = []
    treasures = []
    doors = []
    keys = []
    destructibles = []
    gun = []
    # player position as [x,y] pair in list; global so we can reset player
    # position.
    player_pos = []
    speed = 1
    GAMEWON = False
    # load maps (global)
    maps = load_maps()
    # do the map setup.
    startnew()
    gold_left = 3
    start_game = True
    turtlescreen.update()
    root.mainloop()
