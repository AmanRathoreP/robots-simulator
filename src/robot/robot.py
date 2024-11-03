import math

import pygame as pg


class Robot:
    """
    A class to represent a robot in a 2D simulation using Pygame and Pymunk.

    Attributes:
        size (list[int]): The width and height of the robot in pixels.
        position (pygame.Vector2d): The current position of the robot in the simulation, represented as a vector.
        angle (float): The current angle of the robot in degrees, indicating its orientation.
        sensors (list): A list representing the sensors attached to the robot, which can be used for navigation and obstacle detection.
        body (pymunk.Body): The physical body of the robot in the simulation, which interacts with the physics engine.
        shape (pymunk.Poly): The shape of the robot used for collision detection, defining its physical boundaries.
        acceleration_vector (pg.Vector2): The current acceleration vector of the robot, which affects its linear movement.
        velocity (pg.Vector2): The current velocity vector of the robot, indicating its speed and direction of movement.
        angular_acceleration (float): The current angular acceleration of the robot, affecting its rotational speed.
        angular_velocity (float): The current angular velocity of the robot, indicating how fast it is rotating.
        turning_speed (float): The rate at which the robot can turn, measured in radians per second.
        base_color (tuple[int, int, int]): The color of the robot's body.
        outline_color (tuple[int, int, int]): The color of the robot's outline.
    """
    body_surface: pg.Surface = None
    sudo_surface: pg.Surface = None
    """Surface containing area including border"""
    base_colorkey: pg.Surface = (0, 0, 0)
    base_outline_colorkey: pg.Surface = (255, 255, 255)

    # todo center_of_rotation
    def __init__(
            self,
            position: list[int],
            angle: float,
            size: list[int],
            center_of_rotation: list[float] = [0, 0],
            sensors: list = [],
            base_color: tuple[int, int, int] = (0, 128, 255),
            outline_color: tuple[int, int, int] = (0, 0, 0),
            group=1,
    ):
        """
        Initializes the Robot.

        Args:
            position (list[int]): The initial position of the robot as [x, y].
            angle (float): The initial angle of the robot in degrees.
            size (list[int]): The size of the robot as [width, height].
            center_of_rotation (list[float]): Center of rotation w.r.t. robot.
            sensors (dict): A dictionary of sensors associated with the robot.
            base_color (tuple[int, int, int]): The color of the robot's body (default: blue).
            outline_color (tuple[int, int, int]): The color of the robot's outline (default: black).
            group (Any): Robots of the same group doesn't collide with each other.
        """
        self._size = size
        self._position = pg.Vector2(position[0], position[1])
        self._angle = angle
        self._sensors = sensors
        self._center_of_rotation = center_of_rotation

        self._friction = 0.31009

        self.acceleration_vector = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(0, 0)
        self.angular_acceleration = 0
        self.angular_velocity = 0
        self.turning_speed = 0.05

        self.base_color = base_color
        self.outline_color = outline_color

    def set_position(self, position: list[float]):
        """
        Set the position of the robot.

        Args:
            position (list[float]): The new position of the robot as [x, y].

        Example:
            robot.set_position([200, 150])  # Move the robot to (200, 150)
        """
        self._position = pg.Vector2(position)

    def set_angle(self, angle: float):
        """
        Set the angle of the robot.

        Args:
            angle (float): The new angle of the robot in degrees.

        Example:
            robot.set_angle(90)  # Rotate the robot to face 90 degrees
        """
        self._angle = math.radians(angle)

    @property
    def get_position(self) -> pg.Vector2:
        """
        Get the current position of the robot.

        Returns:
            pygame.Vector2d: The current position of the robot.

        Example:
            position = robot.get_position
        """
        return self._position

    @property
    def get_angle(self) -> float:
        """
        Get the current angle of the robot.

        Returns:
            float: The current angle of the robot in degrees.

        Example:
            angle = robot.get_angle
        """
        return math.degrees(self._angle)

    def set_acceleration(self, acceleration: list[float]):
        """
        Set the acceleration vector for the robot.

        Args:
            acceleration (list[float]): The new acceleration vector as [x, y].

        Example:
            robot.set_acceleration([1.0, 0.0])  # Accelerate in the x direction
        """
        self.acceleration_vector = pg.Vector2(acceleration)

    def set_angular_acceleration(self, angular_acceleration: float):
        """
        Set the angular acceleration for the robot.

        Args:
            angular_acceleration (float): The new angular acceleration value.

        Example:
            robot.set_angular_acceleration(0.1)  # Set angular acceleration to 0.1
        """
        self.angular_acceleration = angular_acceleration

    def set_angular_velocity(self, angular_velocity: float):
        """
        Set the angular velocity for the robot.

        Args:
            angular_velocity (float): The new angular velocity value.

        Example:
            robot.set_angular_velocity(0.5)  # Set angular velocity to 0.5
        """
        self.angular_velocity = angular_velocity

    def event_handler(self, events):
        """
        Handle user input events.

        Args:
            events: The list of Pygame events to handle.
        
        This method processes key events to control the robot's movement.
        """
        pass

    def update(self, time_step: float, events):
        """
        Update the robot's position and angle based on the physics simulation.

        Args:
            time_step (float): The time step for the update, usually based on the simulation frame rate.
            events: The list of Pygame events for handling user input.
        
        This method calculates the new position and angle of the robot using its acceleration and velocity.
        """
        self.event_handler(events)

        self.velocity += self.acceleration_vector.rotate_rad(
            self._angle) * time_step
        self.velocity *= (1 - self._friction)

        pos = self.velocity * time_step
        self._position += pos

        self.angular_velocity += self.angular_acceleration * time_step
        self.angular_velocity *= (1 - self._friction)
        angle = self.angular_velocity * time_step
        self._angle += angle

        self._angle %= (2 * math.pi)

        for sensor in self._sensors:
            sensor.update(
                time_step,
                events,
            )

    def draw(self, screen):
        """
        Draw the robot on the Pygame screen.

        Args:
            screen: The Pygame screen surface to draw the robot on.

        This method renders the robot's current shape and position, along with a front marker.
        """
        border_size: float = 3

        self.robot_rect = pg.Rect(0, 0, self._size[0], self._size[1])
        self.robot_rect.center = self._position

        self.body_surface = pg.Surface((self._size[0], self._size[1]))
        self.body_surface.fill(self.base_color)
        self.body_surface.set_colorkey(self.base_colorkey)

        self.body_surface = pg.transform.rotate(
            self.body_surface,
            -math.degrees(self._angle),
        )

        self.sudo_robot_for_border_rect = pg.Rect(0, 0,
                                                  self._size[0] + border_size,
                                                  self._size[1] + border_size)
        self.sudo_robot_for_border_rect.center = self._position

        self.sudo_surface = pg.Surface(
            (self._size[0] + border_size, self._size[1] + border_size))
        self.sudo_surface.fill(self.outline_color)
        self.sudo_surface.set_colorkey(self.base_outline_colorkey)

        self.sudo_surface = pg.transform.rotate(
            self.sudo_surface,
            -math.degrees(self._angle),
        )

        screen.blit(
            self.sudo_surface,
            self.sudo_surface.get_rect(
                center=self.sudo_robot_for_border_rect.center).topleft,
        )

        screen.blit(
            self.body_surface,
            self.body_surface.get_rect(center=self.robot_rect.center).topleft,
        )

        for sensor in self._sensors:
            sensor.draw(
                screen,
                self._position,
                self._angle,
            )  # contains a blit function

    @property
    def robot_mask(self) -> pg.Mask:
        return pg.mask.from_surface(self.body_surface)
