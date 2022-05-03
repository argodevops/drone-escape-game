
import turtle
import math
import time
import json
import random
import re
import sys
import pygame
from numpy import array

STEP_COUNT = 24

class Drone(turtle.Turtle):
    """
    Moves the drone object

    Args:
        turtle (_type_): turtle object
    """

    def __init__(self, walls):
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/drone.gif")
        self.shape("./image/drone.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.direction = 'UP'
        self.walls = walls

    def go_up(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() + (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in self.walls:
            self.goto(move_to_x, move_to_y)
            return True
        
        return False

    def go_down(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() - (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in self.walls:
            self.goto(move_to_x, move_to_y)
            return True
        
        return False

    def go_left(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() - (count * STEP_COUNT)
        move_to_y = self.ycor()

        if (move_to_x, move_to_y) not in self.walls:
            self.goto(move_to_x, move_to_y)
            return True
        
        return False

    def go_right(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = self.xcor() + (count * STEP_COUNT)
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in self.walls:
            self.goto(move_to_x, move_to_y)
            return True
        
        return False

    def turn(self, turn_direction):
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
            print(f"Uknown turn direction {turn_direction}")

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
            screen = self.getscreen()
            screen.register_shape("./image/zombie.gif")
            self.shape("./image/zombie.gif")
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
