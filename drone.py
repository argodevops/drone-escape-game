"""Drone module."""
import time
from turtle import RawTurtle
import math

STEP_COUNT = 24

# Not a fan of Drone (player) knowing locations of everything in maze and
# deciding himself what happens; seems backwards.

class Drone(RawTurtle):
    """
    Moves the drone object

    Args:
        turtle (_type_): turtle object
    """
    # following convention but this is not ideal. Just making it work.

    def __init__(
            self,
            walls,
            keyset,
            doors,
            treasures,
            destructibles,
            guns,
            screen):
        RawTurtle.__init__(self, screen)
        screen.register_shape("./image/drone.gif")
        self.reset()
        self.walls = walls
        self.hideturtle()
        self.isdead = False
        self.direction = 'UP'
        # so player knows walls rather than game decides, so will need to know
        # other things.
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
        """
        Resets everything
        """
        self.shape("./image/drone.gif")
        self.color("blue")
        self.penup()
        self.delay = 1
        self.gold = 0
        self.direction = 'UP'
        self.isdead = False
        self.keys = 0
        self.haslaser = False

    def processgold(self):
        """
        Gold speed up
        """
        if self.gold > 0:
            self.gold -= 1
        if self.gold <= 0:
            self.delay = 1

    def processmove(self, pos_x, pos_y):
        """
        Process move coords

        Args:
            x (_type_): _description_
            y (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.processgold()
        # did we collide with a wall?
        if (pos_x, pos_y) in self.walls:
            return False
        time.sleep(self.delay)
        # this is going to be messy... but make it work first and foremost, refactor later.
        # potential refactor, just stash ALL into one collection of map objects
        # and then act on type?
        # pick up laser.
        for gun in self.guns:
            if (gun.get_x() == pos_x and gun.get_y() == pos_y and gun.isActive()):
                self.haslaser = True
                gun.destroy()

        # ran into destructible wall?
        for destructible in self.destructibles:
            if (destructible.get_x() == pos_x and destructible.get_y()
                    == pos_y and destructible.isActive()):
                return False

        for treasure in self.treasures:
            if (treasure.get_x() == pos_x and treasure.get_y()
                    == pos_y and treasure.isActive()):
                treasure.destroy()
                # 20s at 0.5 delay, 40 moves basically... and turns are a move
                # too.
                self.gold += 40
                # depending on map it may take longer to collect and return
                # gold than to ignore it.
                self.delay = 0.5

        for key in self.keyset:
            if (key.get_x() == pos_x and key.get_y() == pos_y and key.isActive()):
                print("Key coords " + str(key.get_x()) + " " + str(key.get_y()))
                self.keys += 1
                key.destroy()

        for door in self.doors:
            if (door.get_x() == pos_x and door.get_y()
                    == pos_y and door.isActive()):
                # could check door locked or not and set open etc instead of
                # destroying door, where destroy for door overrides and changes
                # icon?
                print("Door coords " + str(door.get_x()) + " " + str(door.get_y()))
                if self.keys == 0:
                    print('No keys, locked door')
                    return False  # locked door no key

                print("Have" + str(self.keys) + " available, using one")
                self.keys -= 1
                door.destroy()
        # continue on!
        self.goto(pos_x, pos_y)
        return True

    def go_up(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() + (count * STEP_COUNT)
        return self.processmove(move_to_x, move_to_y)

    def go_down(self, count=1):
        """_summary_
        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() - (count * STEP_COUNT)
        return self.processmove(move_to_x, move_to_y)

    def go_left(self, count=1):
        """_summary_
        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() - (count * STEP_COUNT)
        move_to_y = self.ycor()
        return self.processmove(move_to_x, move_to_y)

    def go_right(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() + (count * STEP_COUNT)
        move_to_y = self.ycor()
        return self.processmove(move_to_x, move_to_y)

    def shoot(self):
        """
        Shoots block
        """
        if not self.haslaser:
            return
        blockx = self.xcor()
        blocky = self.ycor()
        if self.direction == "UP":
            blocky += 24
        elif self.direction == "DOWN":
            blocky -= 24
        elif self.direction == "RIGHT":
            blockx += 24
        elif self.direction == "LEFT":
            blockx -= 24

        for destructible in self.destructibles:
            if (blockx == destructible.get_x() and blocky ==
                    destructible.get_y() and destructible.isActive()):
                destructible.destroy()

    def turn(self, turn_direction):
        """_summary_

        Args:
            turn_direction (_type_): _description_
        """
        self.processgold()
        turn_direction = turn_direction.upper()
        print(f" * TURN {turn_direction}")
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
        """_summary_
        """
        screen = self.getscreen()
        screen.register_shape("./image/zombie.gif")
        self.shape("./image/zombie.gif")
        self.isdead = True
        self.gold = 0
        self.delay = 1

    def player_dead(self):
        """_summary_

        Returns:
            _type_: _description_
        """
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
        # wn.update()

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
