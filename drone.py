
import time
import turtle
from turtle import RawTurtle
import math
from numpy import array

STEP_COUNT = 24

# Not a fan of Drone (player) knowing locations of everything in maze and deciding himself what happens; seems backwards.

class Drone(RawTurtle):
    """
    Moves the drone object

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self, walls, keyset, doors, treasures, destructibles, guns, screen):
        RawTurtle.__init__(self, screen)
        screen.register_shape("./image/drone.gif")
        self.reset()
        self.walls = walls
        self.hideturtle()
        self.isdead = False
        self.direction = 'UP'
        # so player knows walls rather than game decides, so will need to know other things.
        self.keys = 0
        self.gold = 0
        self.keyset = keyset
        self.doors = doors
        self.treasures = treasures
        self.delay = 1
        self.destructibles = destructibles
        self.guns = guns
        self.haslaser = False

    def reset(self):
        self.shape("./image/drone.gif")
        self.color("blue")
        self.penup()
        self.delay = 1
        self.gold = 0
        self.direction = 'UP'
        self.isdead = False
        self.keys = 0
        self.haslaser = False

    def processGold(self):
        if (self.gold > 0):
            self.gold -= 1
        if (self.gold <= 0):
            self.delay = 1

    def processMove(self, x, y):
        self.processGold()
        # did we collide with a wall?
        if (x, y) in self.walls:
            return False
        time.sleep(self.delay)
        # this is going to be messy... but make it work first and foremost, refactor later.
        # potential refactor, just stash ALL into one collection of map objects
        # and then act on type?
        # pick up laser.
        for gun in self.guns:
            if (gun.getX() == x and gun.getY() == y and gun.isActive()):
                self.haslaser = True
                gun.destroy()

        #ran into destructible wall?
        for destructible in self.destructibles:
            if (destructible.getX() == x and destructible.getY() == y and destructible.isActive()):
                return False

        for treasure in self.treasures:
            if (treasure.getX() == x and treasure.getY() == y and treasure.isActive()):
                treasure.destroy()
                self.gold += 40 # 20s at 0.5 delay, 40 moves basically... and turns are a move too.
                # depending on map it may take longer to collect and return gold than to ignore it.
                self.delay = 0.5

        for key in self.keyset:
            if (key.getX() == x and key.getY() == y and key.isActive()):
                print("Key coords " + str(key.getX()) + " " + str(key.getY()))
                self.keys += 1
                key.destroy()

        for door in self.doors:
            if (door.getX() == x and door.getY() == y):
                 # could check door locked or not and set open etc instead of destroying door, where destroy for door overrides and changes icon?
                print("Door coords " + str(door.getX()) + " " + str(door.getY()))
                if (self.keys == 0):
                    print('No keys, locked door')
                    return False # locked door no key 
                else:
                    print("Have" + str(self.keys) + " available, using one")
                    self.keys -= 1
                    door.destroy()
        # continue on!
        self.goto(x,y)
        return True

    def go_up(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() + (count * STEP_COUNT)

        #if (move_to_x, move_to_y) not in self.walls:
        #    self.goto(move_to_x, move_to_y)
        #    return True
        return self.processMove(move_to_x, move_to_y)
        #return False

    def go_down(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() - (count * STEP_COUNT)

        #if (move_to_x, move_to_y) not in self.walls:
        #    self.goto(move_to_x, move_to_y)
        #    return True
        return self.processMove(move_to_x, move_to_y)
        #return False

    def go_left(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() - (count * STEP_COUNT)
        move_to_y = self.ycor()

        #if (move_to_x, move_to_y) not in self.walls:
        #    self.goto(move_to_x, move_to_y)
        #    return True
        return self.processMove(move_to_x, move_to_y)
        #return False

    def go_right(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() + (count * STEP_COUNT)
        move_to_y = self.ycor()
        #if (move_to_x, move_to_y) not in self.walls:
        #    self.goto(move_to_x, move_to_y)
        #    return True
        return self.processMove(move_to_x, move_to_y)
        #return False
    
    def addKey(self):
        self.keys += 1

    def hasKey(self):
        return self.keys

    def useKey(self):
        if self.hasKey():
            self.keys -= 1
            return True
        return False

    def shoot(self):
        if (not self.haslaser):
            return 
        blockx = self.xcor()
        blocky = self.ycor()
        if (self.direction == "UP"):
            blocky += 24
        elif (self.direction == "DOWN"):
            blocky -= 24
        elif (self.direction == "RIGHT"):
            blockx += 24
        elif (self.direction == "LEFT"):
            blockx -= 24

        for destructible in self.destructibles:
            if (blockx == destructible.getX() and blocky == destructible.getY() and destructible.isActive()):
                destructible.destroy()

    def turn(self, turn_direction):
        self.processGold()
        """_summary_

        Args:
            turn_direction (_type_): _description_
        """
        print(f" * TURN {turn_direction}")
        # IDEA - could make directions reverse to make it trickier??
        if turn_direction == "RIGHT":
            if self.direction == "UP":
                self.direction = "RIGHT"
            elif self.direction == "RIGHT":
                self.direction = "DOWN"
            elif self.direction == "DOWN":
                self.direction = "LEFT"
            elif self.direction == "LEFT":
                self.direction = "UP"
        elif turn_direction == "LEFT":
            if self.direction == "UP":
                self.direction = "LEFT"
            elif self.direction == "RIGHT":
                self.direction = "UP"
            elif self.direction == "DOWN":
                self.direction = "RIGHT"
            elif self.direction == "LEFT":
                self.direction = "DOWN"
        else:
            print(f"Unknown turn direction {turn_direction}")

    def dead(self):
        screen = self.getscreen()
        screen.register_shape("./image/zombie.gif")
        self.shape("./image/zombie.gif")
        self.isdead = True
        self.gold = 0
        self.delay = 1

    def playerDead(self):
        return self.isdead

    def move(self, steps=1):
        """_summary_

        Args:
            steps (int, optional): _description_. Defaults to 1.
        """
        print(f" * MOVE {steps}")
        if self.direction == "UP":
            moved = self.go_up(steps)
        elif self.direction == "RIGHT":
            moved = self.go_right(steps)
        elif self.direction == "DOWN":
            moved = self.go_down(steps)
        elif self.direction == "LEFT":
            moved = self.go_left(steps)
        else:
            moved = False
            print(f"Unknown direction for {steps} steps")

        if not moved:
            self.dead()
        #wn.update()

        return moved

    # TODO - use collision
    def is_collision(self, other):
        """_summary_

        Args:
            other (_type_): _description_

        Returns:
            _type_: _description_
        """
        pos_x = self.xcor() - other.xcor()
        pos_y = self.ycor() - other.ycor()
        distance = math.sqrt((pos_x**2) + (pos_y**2))
        return distance < 5