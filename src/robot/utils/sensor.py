import math

import pygame as pg


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
        self.relative_position: pg.Vector2 = pg.Vector2(relative_position)
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
        offset = self.relative_position.rotate_rad(robot_angle)
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

    def calculate_sensor_data(
        self,
        robot_position,
        robot_angle,  #degrees
        map_mask: pg.Mask,
        map_position: pg.Vector2,
    ):
        """
        Override this function in child class as it is called at every frame
        """
        pass


class LIDARSensor(Sensor):

    distance: int = 40

    def __init__(
        self,
        name: str,
        relative_position: list[int],
        angle: float = 45,  #degrees
        size: list[int] = [10, 10],
        color: tuple[int] = (255, 0, 0),
        lidar_ray_color: tuple[int] = (0, 204, 146),
        lidar_ray_thickness: int = 3,
        lidar_max_distance: int = 150,
    ):
        super().__init__(name, relative_position, "rectangle", size, color)
        self.angle = angle
        self.lidar_ray_color = lidar_ray_color
        self.lidar_ray_thickness = lidar_ray_thickness
        self.lidar_max_distance = lidar_max_distance

    def draw(self, screen, robot_position, robot_angle):
        super().draw(screen, robot_position, robot_angle)
        if self.distance != None:
            sensor_position = robot_position + self.relative_position.rotate_rad(
                robot_angle)

            lidar_angle = math.degrees(robot_angle) + self.angle

            end_x = sensor_position.x + self.distance * math.cos(
                math.radians(lidar_angle))
            end_y = sensor_position.y + self.distance * math.sin(
                math.radians(lidar_angle))
            end_position = pg.math.Vector2(end_x, end_y)

            pg.draw.line(
                screen,
                self.lidar_ray_color,
                sensor_position,
                end_position,
                self.lidar_ray_thickness,
            )

    def calculate_sensor_data(
        self,
        robot_position,
        robot_angle,  #degrees
        map_mask: pg.Mask,
        map_position: pg.Vector2,
    ):
        self.calculate_lidar_ray_length(
            robot_position,
            robot_angle,
            map_mask,
            map_position,
        )

    def calculate_lidar_ray_length(
        self,
        robot_position,
        robot_angle,  #degrees
        map_mask: pg.Mask,
        map_position: pg.Vector2,
    ):
        sensor_position = robot_position + self.relative_position.rotate(
            robot_angle)

        lidar_angle = math.radians(robot_angle + self.angle)

        for distance in range(1, self.lidar_max_distance):
            x = sensor_position.x + distance * math.cos(lidar_angle)
            y = sensor_position.y + distance * math.sin(lidar_angle)
            try:
                if map_mask.get_at((int(x - map_position.x),
                                    int(y - map_position.y))) == True:
                    self.distance = distance
                    return
            except:
                self.distance = self.lidar_max_distance

        self.distance = self.lidar_max_distance


class IRSensor(Sensor):

    is_on: bool = False

    def __init__(
            self,
            name: str,
            relative_position: list[int],
            size: list[int] = [4, 4],
            off_color: tuple[int] = (0, 0, 0),
            on_color: tuple[int] = (255, 255, 255),
    ):
        super().__init__(name, relative_position, "circle", size, off_color)
        self.on_color = on_color
        self.off_color = off_color

    def draw(self, screen, robot_position, robot_angle):
        self.color = self.on_color if self.is_on else self.off_color
        super().draw(screen, robot_position, robot_angle)

    def calculate_sensor_data(
        self,
        robot_position,
        robot_angle,  #degrees
        map_mask: pg.Mask,
        map_position: pg.Vector2,
    ):
        self.calculate_ir_value(
            robot_position,
            robot_angle,
            map_mask,
            map_position,
        )

    def calculate_ir_value(
        self,
        robot_position,
        robot_angle,  # degrees
        map_mask: pg.Mask,
        map_position: pg.Vector2,
    ):
        try:
            self.is_on = not map_mask.get_at(
                robot_position + self.relative_position.rotate(robot_angle) -
                map_position)
        except IndexError:
            # If out of bounds, set the sensor as off
            self.is_on = False
