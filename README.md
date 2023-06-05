# Drone Maze Game

A maze game built using `tkinter` and `turtle` which takes a set of commands to navigate a drone around and out of the maze.

## Developer guide

1. Create your virtual environment: `python3 -m venv .venv`
2. Activate the virtual environment: `source ./.venv/bin/activate`
3. Install the dependencies: `pip install -r requirements.txt`
4. Install python-tk: `sudo apt-get install python3-tk`

## Running the game

Run:

1. `source ./.venv/bin/activate`
2. `python maze.py` or `python maze2.py`

## Game Instructions

The area on the left is the input for the drone. Clicking any of the buttons will add a line to the text box wherever the cursor is. **NOTE** This means that if commands are typed or changed then the cursor needs to be manually put at the bottom of the box otherwise new commands will be on the same line as the previous.

The command list can be built up in stages. Kids will find it easier if they just try to get the key and then try to get to the door and then to the lazer etc.

- "Run Commands" button will run all the commands in the box.
- "Clear Commands" will clear all commands from the box.
- "Reset Game" is used while building up commands. This will reset the maze to the inital state while retaining all the commands.
- "New Game" will do both "Clear Commands" and "Reset Game".

## Running this for young kids

There are some things that they'll struggle with initially.

- Turning left or right to them means "Make the drone face left or right" and not rotate the drone. You'll need to explain this to them so they understand that if the drone is facing down then to get it to face right they'll need to click "Turn Left".
- The "FIRE" button will only destroy the wall if it's right in front of the drone.
- There are multiple exits. It's really easy to direct the kids to use the easiest one by pointing out the different end goals and just pointing to the easy one last and lingering on it a second longer.

## Configuration

Edit `messages.py` to configure any URL endpoint which need calling.

## Task List

- Resize for 21" screen (lanscape) assuming 16:9 ratio
- Maze layouts
- REST call on completing game

## Example Command List

- MOVE 2
- TURN LEFT
- MOVE 1
- TURN RIGHT
- MOVE 1
- TURN LEFT
- TURN LEFT
- MOVE 1
- TURN RIGHT
- MOVE 8
- TURN LEFT
- MOVE 2
- TURN RIGHT
- MOVE 6
- TURN RIGHT
- MOVE 2
- TURN LEFT
- MOVE 1
- FIRE
- MOVE 2
