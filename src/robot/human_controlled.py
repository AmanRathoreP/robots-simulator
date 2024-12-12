import math

import pygame as pg

from src.robot.robot import Robot


class HumanControlled(Robot):

    def event_handler(self, events):
        """
        Handle user input events.

        Args:
            events: The list of Pygame events to handle.
        
        This method processes key events to control the robot's movement.
        """
        keys = pg.key.get_pressed()  # Get the current state of all keys
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:  # Stop turning
                    self.set_angular_acceleration(0)
                    self.set_angular_velocity(0)

            # Control for acceleration and movement
            if keys[pg.K_UP]:  # Accelerate forward
                self.set_acceleration(
                    [1000,
                     0])  # You can adjust the values for desired acceleration
            elif keys[pg.K_DOWN]:  # Accelerate backward
                self.set_acceleration([-1000,
                                       0])  # Adjust for backward movement
            else:
                self.set_acceleration(
                    [0, 0])  # Stop acceleration when no key is pressed

            # Control for turning
            if keys[pg.K_LEFT]:  # Turn left
                self.set_angular_acceleration(-100)
            elif keys[pg.K_RIGHT]:  # Turn right
                self.set_angular_acceleration(100)
            else:
                self.set_angular_acceleration(
                    0)  # Stop angular acceleration when no key is pressed

            if keys[pg.K_s]:
                self.set_position(self.get_position() + pg.Vector2(0, 1))
            if keys[pg.K_w]:
                self.set_position(self.get_position() - pg.Vector2(0, 1))
            if keys[pg.K_d]:
                self.set_position(self.get_position() + pg.Vector2(1, 0))
            if keys[pg.K_a]:
                self.set_position(self.get_position() - pg.Vector2(1, 0))
            if keys[pg.K_q]:
                self.set_angle(self.get_angle() - 5)
            if keys[pg.K_e]:
                self.set_angle(self.get_angle() + 5)
            if keys[pg.K_1]:
                self.set_angle(self.get_angle() - 1)
            if keys[pg.K_3]:
                self.set_angle(self.get_angle() + 1)
