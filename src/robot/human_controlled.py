import math

import pygame

from src.robot.robot import Robot


class HumanControlled(Robot):

    def event_handler(self, events):
        """
        Handle user input events.

        Args:
            events: The list of Pygame events to handle.
        
        This method processes key events to control the robot's movement.
        """
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Stop turning
                    self.set_angular_acceleration(0)
                    self.set_angular_velocity(0)

            # Control for acceleration and movement
            if keys[pygame.K_UP]:  # Accelerate forward
                self.set_acceleration(
                    [0.0001,
                     0])  # You can adjust the values for desired acceleration
            elif keys[pygame.K_DOWN]:  # Accelerate backward
                self.set_acceleration([-0.0001,
                                       0])  # Adjust for backward movement
            else:
                self.set_acceleration(
                    [0, 0])  # Stop acceleration when no key is pressed

            # Control for turning
            if keys[pygame.K_LEFT]:  # Turn left
                self.set_angular_acceleration(-0.000002)
            elif keys[pygame.K_RIGHT]:  # Turn right
                self.set_angular_acceleration(0.000002)
            else:
                self.set_angular_acceleration(
                    0)  # Stop angular acceleration when no key is pressed

            if keys[pygame.K_s]:
                self.set_position(self.get_position + pygame.Vector2(0, 1))
            if keys[pygame.K_w]:
                self.set_position(self.get_position - pygame.Vector2(0, 1))
            if keys[pygame.K_d]:
                self.set_position(self.get_position + pygame.Vector2(1, 0))
            if keys[pygame.K_a]:
                self.set_position(self.get_position - pygame.Vector2(1, 0))
            if keys[pygame.K_q]:
                self.set_angle(self.get_angle - 5)
            if keys[pygame.K_e]:
                self.set_angle(self.get_angle + 5)
            if keys[pygame.K_1]:
                self.set_angle(self.get_angle - 1)
            if keys[pygame.K_3]:
                self.set_angle(self.get_angle + 1)
