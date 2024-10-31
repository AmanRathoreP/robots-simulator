import math

import pygame as pg
import pymunk


class Sensor:
    """
    A class representing a customizable sensor attached to a robot.

    Attributes:
        name (str): The name or identifier of the sensor.
        relative_position (list[int]): Position of the sensor relative to the robot.
        shape (str): The shape of the sensor (e.g., "circle", "rectangle").
        size (list[int, int]): The dimensions of the sensor (width, height) for rectangular shapes.
        color (tuple[int, int, int]): The color of the sensor.
    """

    def __init__(self,
                 name: str,
                 relative_position: list[int],
                 shape: str = "circle",
                 size: list[int] = [10, 10],
                 color: tuple[int] = (255, 0, 0)):
        self.name = name
        self.relative_position = pymunk.Vec2d(relative_position[0],
                                              relative_position[1])
        self.shape = shape
        self.size = size
        self.color = color

    def get_data(self):
        #todo
        pass

    def event_handler(self, events):
        """
        Handle user input events.

        Args:
            events: The list of Pygame events to handle.
        
        This method processes key events to control the sensors's properties.
        """
        pass

    def update(self, time_step: float, events):
        self.event_handler(events)

    def draw(self, screen, robot_position, robot_angle):
        """
        Draw the sensor on the screen relative to the robot's position and angle.

        Args:
            screen: The Pygame screen surface.
            robot_position: The position of the robot in the simulation.
            robot_angle: The current angle of the robot in radians.
        """
        offset = self.relative_position.rotated(robot_angle)
        sensor_position = robot_position + offset

        if self.shape == "circle":
            pg.draw.circle(
                screen,
                self.color,
                (int(sensor_position.x), int(sensor_position.y)),
                min(self.size) / 2,
            )
        elif self.shape == "rectangle":
            sensor_surface = pg.Surface(self.size, pg.SRCALPHA)
            pg.draw.rect(sensor_surface, self.color, sensor_surface.get_rect())

            rotated_surface = pg.transform.rotate(sensor_surface,
                                                  -math.degrees(robot_angle))
            rotated_rect = rotated_surface.get_rect(
                center=(int(sensor_position.x), int(sensor_position.y)))

            screen.blit(rotated_surface, rotated_rect)


class LIDARSensor(Sensor):
    pass


class IRSensor(Sensor):
    pass
