"""Maze module."""
from turtle import RawTurtle, TurtleScreen, color
from tkinter import *
from tkinter import scrolledtext
from tkinter.messagebox import askyesno
import threading
import re
import json
import random
from numpy import array
from drone import Drone
from timer import Timer
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
        screen.register_shape("./image/flag.gif")
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

# could have destroyable blocks that the users can destroy with a drones lazer?but that may be a bit... aggressive. But it'd
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


class Lazer(GameObject):
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
            maze_x = -250 + (pos_x * 26)
            maze_y = 230 - (pos_y * 26)
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
                pen.goto(maze_x, maze_y)
                pen.shape("./image/flag.gif")
                pen.stamp()
                pen.shape("./image/block.gif")
                #GAMEEXIT = [maze_x, maze_y]
                GAMEEXIT.append([maze_x, maze_y])
                print(GAMEEXIT)
            elif character == "T":
                treasures.append(Treasure(maze_x, maze_y, turtlescreen))
            elif character == "G":
                lazers.append(Lazer(maze_x, maze_y, turtlescreen))
            elif character == "D":
                destructibles.append(Destructable(maze_x, maze_y, turtlescreen))
            elif character == "W":
                doors.append(Door(maze_x, maze_y, turtlescreen))
            elif character == "K":
                keys.append(DoorKey(maze_x, maze_y, turtlescreen))
    turtlescreen.update()
    # was a debug to check we had correctly destroyed/created turtles.
    print("Turtles " + str(len(turtlescreen.turtles())))


def gameover():
    """_summary_
        Just uses the turtle to write in red on the canvas/screen its attached to
    """
    buttonrun["state"] = DISABLED
    buttonreset["state"] = NORMAL
    stop_timer()
    turtlescreen.bgcolor("tomato")
    turtle.penup()
    turtle.goto(-400, -100)
    turtle.color("navy")
    turtle.write("GAME OVER", align="left", font=("Courier", 110))
    turtle.goto(-300, -350)
    turtle.write("Press \"Reset Game\" to Play Again", align="left", font=("Courier", 24))

    turtle.goto(2000, 2000)

def start_timer():
    buttonrun["state"] = DISABLED
    global timer
    timer = Timer(timerlabel)
    timer_thread = threading.Thread(target = timer.run)
    timer_thread.start()


def stop_timer(reset = False):
    #buttonrun["state"] = NORMAL
    if 'timer' in globals():
        if reset:
            timer.reset()
        else:
            timer.stop()


def move_drone(player: Drone, instructions):
    """_summary_
        Read commands and move drone
    Args:
        player (Drone): _description_
    """
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
                if not player.move():
                    gameover()
                    return False
                for gExit in GAMEEXIT:
                    if player.xcor() == gExit[0] and player.ycor() == gExit[1]:
                        wingame()
                        return
                scorelabel['text'] = 'SCORE: ' + str(player.score)
        else:
            print_executing_text('Unknown command: ' + instruction)
            player.dead()
            gameover()
            return False
        turtlescreen.update()
        scorelabel['text'] = 'SCORE: ' + str(player.score)
    if not GAMEWON:
        gameover()
    return True

# take user input and run commands on the map (clear executingtext textbox first)
# performs check to ensure dead players can't move. Could disable run
# button instead when dead but...


def run():
    # check they're not just re-running commands without resetting after failing.
    if player.player_dead():
        return
    buttonreset["state"] = DISABLED
    clear_executing_text()  # clear textbox
    # "get" apparently adds newline character to end, so get from start to -1 of end; splitlines splits around newline.
    commands_text = inputtext.get('1.0', 'end-1c').splitlines()
    if validate_command_text(commands_text):
        start_timer()
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

def commandText(text):
    inputtext.insert(END, text)

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


def clear(prompt=True):
    """ Just clear out text of commands/output

    Args:
        prompt (_type_): _description_
    """
    if prompt:
        answer = askyesno('Are you sure?', message='Clear all your commands?')
    else:
        answer = True
    if answer:
        inputtext.delete('1.0', END)
        clear_executing_text()


def wingame():
    global GAMEWON
    GAMEWON = True
    stop_timer()
    turtle.penup()
    turtle.goto(-350, -100)
    turtle.color("green")
    turtle.write("YOU WIN!", align="left", font=("Courier", 110))
    turtle.goto(2000, 2000)
    messages.win(player.score)

# Uses global player x/y that's set on the creation of maze to move player to maze start.
# Calls the respawn method on every other turtle (could create on Drone... If it retaind its original xy)
# Respawn moves existing turtles back to their original x/y given at creation. Turtles are just moved out of screen when "destroyed"
# Could therefore create extended class of RawTurtle that keeps x/y original and has these repetitive methods.
# but for quick hacky omitted for now.


def reset():
    buttonrun["state"] = NORMAL
    player.reset()
    scorelabel['text'] = 'SCORE: ' + str(player.score)
    stop_timer(True)
    turtle.clear()
    turtlescreen.bgcolor("cyan")
    player.goto(player_pos[0], player_pos[1])
    for treasure in treasures:
        treasure.respawn()
    for key in keys:
        key.respawn()
    for door in doors:
        door.respawn()
    for lazer in lazers:
        lazer.respawn()
    for destructible in destructibles:
        destructible.respawn()
    global GAMEWON
    GAMEWON = False
    # this is the "game over" pen being cleared of any writing done.

def startnew(prompt = True):
    """
    Should remove commands entered/ran from Textboxes.
    It DESTROYS all turtle objects via calling clear on the screen. This means they need recreating.
    turtlescreen.clear therefore destroys player, treasures, doors, keys, and the wall drawing "pen" turtle.
    Must therefore create player, the turtle to draw the maze (the creation of maze creates treasures/doors/keys turtle)
    Therefore has to clear the lists that are passed to the player/drone
    Turtle prior to creating from map.

    Args:
        prompt (bool, optional): _description_. Defaults to False.
    """
    clear(prompt)
    # clear DELETES all turtles... this includes player/pen turtles.
    turtlescreen.clear()
    turtlescreen.bgcolor("cyan")
    # turn off animation (for insta maze draw)
    turtlescreen.tracer(0)
    # since treasures turtles deleted, clear out globals.
    walls.clear()
    treasures.clear()
    destructibles.clear()
    lazers.clear()
    GAMEEXIT.clear()
    # we need to refer to global pen/player lest fan and x attempt merge, and
    # so create new turtles
    global pen
    global player
    pen = Pen(turtlescreen)
    player = Drone(walls, keys, doors, treasures, destructibles, lazers, turtlescreen)
    canvas.tag_raise(player)
    # set up maze (also creates treasures turtles)
    setup_maze(maps[random.randrange(len(maps))])
    # Game over message printing, perhaps change this to something else.
    global turtle
    # as this is the "game over" message pen, associated with the screen, recreate.
    turtle = RawTurtle(turtlescreen)
    turtle.penup()
    turtle.hideturtle()
    # turn back on the anims (updates).
    turtlescreen.tracer(1)
    global GAMEWON
    GAMEWON = False
    stop_timer(True)
    buttonrun["state"] = NORMAL


# main command?
# TODO extract out the load of map to function
if __name__ == "__main__":
    # set up properties
    root = Tk()
    root.title("Drone Escape Game")
    root.geometry('1750x950')
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
    frameleft.grid(column=0, row=1, rowspan=2, sticky='n')
    frameright.grid(column=2, row=1, sticky='n')

    # create top frame widget
    # nasty padding as i can't find how to right align the timer
    scorelabel = Label(frametop, text="SCORE: 0", font=('Arial', 18), height=2)
    scorelabel.grid(column=0, row=0)
    titlelabel = Label(frametop, text="DRONE ESCAPE", font=('Arial', 26), height=2, fg='black', padx=230)
    titlelabel.grid(column=1, row=0)
    timerlabel = Label(frametop, text="00:00:00", font=('Arial', 18), height=2)
    timerlabel.grid(column=2, row=0)

    # LEGEND -- long winded but...
    legendlabel = Label(frameright, text="Maze Legend", font=('Arial', 15, 'underline'), height=2)
    legendlabel.grid(column=0, row=0)
    legend = Canvas(frameright)
    legend.grid(row=1, column=0, sticky='w')
    legend.config(width=380, height=750)
    # grab images
    droneimage = PhotoImage(file="./image/drone-up.gif")
    wallimage = PhotoImage(file="./image/block.gif")
    keyimage = PhotoImage(file="./image/key.gif")
    doorimage = PhotoImage(file="./image/door.gif")
    opendoorimage = PhotoImage(file="./image/opendoor.gif")
    treasureimage = PhotoImage(file="./image/speedarrow.gif")
    deaddrone = PhotoImage(file="./image/zombie.gif")
    laserimage = PhotoImage(file="./image/laser.gif")
    destructibleimage = PhotoImage(file="./image/pink.gif")
    # place image and associated text
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
    legend.create_text(90, 305, text="Drone Lazer (pickup)", anchor=NW)
    legend.create_image(20, 340, image=destructibleimage, anchor=NW)
    legend.create_text(90, 345, text="Destructible Wall (need lazer)", anchor=NW)

    # Insturctions for the player to type commands are as follows:
    legend.create_text(110, 410, text="Instructions", anchor=NW, font=('Arial', '15', 'underline'))
    legend.create_text(0, 450, text="Starting at the top left navigate the drone to the \nfinish at the botton right.\nOne key will open one door.\nOne lazer will destroy one section of destructable wall.", anchor=NW)
    #legend.create_text(0, 530, text="Commands are NOT case sensitive" , anchor=NW, font=('Arial', '12', 'bold'))
    legend.create_text(0, 530, text="Collect items for more points!" , anchor=NW, font=('Arial', '12', 'bold'))
    legend.create_text(0, 560, text="To Move forward in the direction you are facing,\nuse 'MOVE 'x' where 'x' is the number \nof spaces to move", anchor=NW)
    legend.create_text(0, 630, text="To Turn Left 90" + u'\u00B0' + ", use 'TURN LEFT'", anchor=NW)
    legend.create_text(0, 655, text="To Turn Right 90" + u'\u00B0' + ", use 'TURN RIGHT'", anchor=NW)
    legend.create_text(0, 680, text="To Fire the Laser, use 'FIRE'", anchor=NW)

    # GAME CANVAS
    canvas = Canvas(root)
    canvas.grid(column=1, row=1, sticky='nw')
    canvas.config(width=950, height=800)

    # LEFT FRAME (Commands box + buttons)
    commandslabel = Label(frameleft, text="Commands Entry List", font=('Arial', 15))
    commandslabel.grid(column=0, row=0, sticky="new")
    textlabel = Label(frameleft, text="Type commands in text box, or use buttons below")
    textlabel.grid(row=1, column=0, stick='ews')
    frameButtonsMove = Frame(frameleft)
    frameButtonsMove.grid(row=2, column=0, sticky='ews')

    frameButtonsTurn = Frame(frameleft)
    frameButtonsTurn.grid(row=3, column=0, sticky='ews')

    frameButtonsAction = Frame(frameleft)
    frameButtonsAction.grid(row=4, column=0, sticky='ews')

    buttonMove = Label(frameButtonsMove, text="MOVE", font=('Arial', 12), width=7)
    buttonMove.grid(row=0, column=0)
    buttonOne = Button(frameButtonsMove, text="1", command=lambda: commandText("MOVE 1\n"))
    buttonOne.grid(row=0, column=1)
    buttonTwo = Button(frameButtonsMove, text="2", command=lambda: commandText("MOVE 2\n"))
    buttonTwo.grid(row=0, column=2)
    buttonThree = Button(frameButtonsMove, text="3", command=lambda: commandText("MOVE 3\n"))
    buttonThree.grid(row=0, column=3)
    buttonFour = Button(frameButtonsMove, text="4", command=lambda: commandText("MOVE 4\n"))
    buttonFour.grid(row=0, column=4)
    buttonFive = Button(frameButtonsMove, text="5", command=lambda: commandText("MOVE 5\n"))
    buttonFive.grid(row=0, column=5)
    buttonSeven = Button(frameButtonsMove, text="7", command=lambda: commandText("MOVE 7\n"))
    buttonSeven.grid(row=0, column=6)
    buttonTen = Button(frameButtonsMove, text="10", command=lambda: commandText("MOVE 10\n"))
    buttonTen.grid(row=0, column=7)

    buttonTurn = Label(frameButtonsTurn, text="TURN", font=('Arial', 12), width=7)
    buttonTurn.grid(row=0, column=0)
    buttonLeft = Button(frameButtonsTurn, text="LEFT", command=lambda: commandText("TURN LEFT\n"))
    buttonLeft.grid(row=0, column=1)
    buttonRight = Button(frameButtonsTurn, text="RIGHT", command=lambda: commandText("TURN RIGHT\n"))
    buttonRight.grid(row=0, column=2)

    fireLabel = Label(frameButtonsAction, text="ACTION", font=('Arial', 12), width=7)
    fireLabel.grid(row=0, column=0)
    buttonFire = Button(frameButtonsAction, text="FIRE", command=lambda: commandText("FIRE\n"))
    buttonFire.grid(row=0, column=1)

    inputtext = scrolledtext.ScrolledText(frameleft, height=30, width=40)
    inputtext.grid(row=5, column=0)
    buttonrun = Button(frameleft, text="Run Commands", command=run)
    buttonrun.grid(row=6, column=0, sticky='ews')
    buttonclear = Button(frameleft, text="Clear Commands", command=clear)
    buttonclear.grid(row=7, column=0, sticky='ews')
    buttonreset = Button(frameleft, text='Reset Game (keeps commands)', command=reset)
    buttonreset.grid(row=8, column=0, sticky='esw')
    buttonnewgame = Button(frameleft, text='New Game', command=startnew)
    buttonnewgame.grid(row=9, column=0, sticky='esw')

    # BOTTOM FRAME (scrollable executing command window) -- simply indicates
    # last command incase of errors.
    executingtext = scrolledtext.ScrolledText(framebottom, height=10, width=116, wrap=WORD, state='disabled')
    executingtext.grid(row=0, column=0, sticky='news')

    # Game canvas screen setup.
    turtlescreen = TurtleScreen(canvas)
    turtlescreen.bgcolor("cyan")
    # Turtle that draws "Game over" message ON the game canvas.
    turtle = RawTurtle(turtlescreen)
    # turtle leaves an arrow when visble, so make invisible.
    turtle.hideturtle()

    # Play that funky music ...
    # pygame.mixer.init()
    # pygame.mixer.music.load("./Music/SoundTest.wav")
    # pygame.mixer.music.play(-1)

    # globals -- this is from tutorial, with refactor it'd be better...
    GAMEEXIT = []
    walls = []
    treasures = []
    doors = []
    keys = []
    destructibles = []
    lazers = []
    # player position as [x,y] pair in list; global so we can reset player position.
    player_pos = []
    speed = 1
    GAMEWON = False
    # load maps (global)
    maps = load_maps()
    # do the map setup.
    startnew(False)
    gold_left = 3
    turtlescreen.update()
    root.mainloop()