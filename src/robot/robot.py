import math

import pygame
import pymunk
import vectormath as vmath

from src.utils.helper_functions import rotate_2d


class Robot:
    """
    A class to represent a robot in a 2D simulation using Pygame and Pymunk.

    Attributes:
        size (list[int]): The width and height of the robot in pixels.
        position (pymunk.Vec2d): The current position of the robot in the simulation, represented as a vector.
        angle (float): The current angle of the robot in degrees, indicating its orientation.
        sensors (list): A list representing the sensors attached to the robot, which can be used for navigation and obstacle detection.
        body (pymunk.Body): The physical body of the robot in the simulation, which interacts with the physics engine.
        shape (pymunk.Poly): The shape of the robot used for collision detection, defining its physical boundaries.
        acceleration_vector (vmath.Vector2): The current acceleration vector of the robot, which affects its linear movement.
        velocity (vmath.Vector2): The current velocity vector of the robot, indicating its speed and direction of movement.
        angular_acceleration (float): The current angular acceleration of the robot, affecting its rotational speed.
        angular_velocity (float): The current angular velocity of the robot, indicating how fast it is rotating.
        turning_speed (float): The rate at which the robot can turn, measured in radians per second.
        base_color (tuple[int, int, int]): The color of the robot's body.
        outline_color (tuple[int, int, int]): The color of the robot's outline.
    """

    # todo center_of_rotation
    def __init__(
            self,
            position: list[int],
            angle: float,
            size: list[int],
            center_of_rotation: list[float],
            sensors: list,
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
        self._position = pymunk.Vec2d(position[0], position[1])
        self._angle = angle
        self._sensors = sensors
        self._center_of_rotation = center_of_rotation

        self.body = pymunk.Body(mass=1, moment=pymunk.moment_for_box(1, size))
        self.body.position = self._position
        self.body.angle = math.radians(self._angle)
        self._friction = 0.1009

        self.shape = pymunk.Poly.create_box(self.body, (size[0], size[1]))
        self.shape.elasticity = 0.5
        self.shape.filter = pymunk.ShapeFilter(group=group)

        self.acceleration_vector = vmath.Vector2(0, 0)
        self.velocity = vmath.Vector2(0, 0)
        self.angular_acceleration = 0
        self.angular_velocity = 0
        self.turning_speed = 0.05

        # New customizable attributes
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
        self.body.position = pymunk.Vec2d(position)

    def set_angle(self, angle: float):
        """
        Set the angle of the robot.

        Args:
            angle (float): The new angle of the robot in degrees.

        Example:
            robot.set_angle(90)  # Rotate the robot to face 90 degrees
        """
        self.body.angle = math.radians(angle)

    @property
    def get_position(self) -> pymunk.Vec2d:
        """
        Get the current position of the robot.

        Returns:
            pymunk.Vec2d: The current position of the robot.

        Example:
            position = robot.get_position
        """
        return self.body.position

    @property
    def get_angle(self) -> float:
        """
        Get the current angle of the robot.

        Returns:
            float: The current angle of the robot in degrees.

        Example:
            angle = robot.get_angle
        """
        return math.degrees(self.body.angle)

    @property
    def get_body(self) -> pymunk.Body:
        """
        Get the physical body of the robot.

        Returns:
            pymunk.Body: The body of the robot.

        Example:
            body = robot.get_body
        """
        return self.body

    @property
    def get_shape(self) -> pymunk.Poly:
        """
        Get the shape of the robot.

        Returns:
            pymunk.Poly: The shape of the robot used for collision detection.

        Example:
            shape = robot.get_shape
        """
        return self.shape

    def set_acceleration(self, acceleration: list[float]):
        """
        Set the acceleration vector for the robot.

        Args:
            acceleration (list[float]): The new acceleration vector as [x, y].

        Example:
            robot.set_acceleration([1.0, 0.0])  # Accelerate in the x direction
        """
        self.acceleration_vector = vmath.Vector2(acceleration[0],
                                                 acceleration[1])

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

        self.velocity += rotate_2d(self.acceleration_vector,
                                   self.body.angle) * time_step
        self.velocity *= (1 - self._friction)

        pos = self.velocity * time_step
        self.body.position += pos

        self.angular_velocity += self.angular_acceleration * time_step
        self.angular_velocity *= (1 - self._friction)
        angle = self.angular_velocity * time_step
        self.body.angle += angle

        self.body.angle %= (2 * math.pi)

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
        vertices = [
            self.body.local_to_world(v) for v in self.shape.get_vertices()
        ]
        points = [(int(vertex.x), int(vertex.y)) for vertex in vertices]

        # Draw the robot's body
        pygame.draw.polygon(screen, self.base_color, points)

        # Draw the outline (if desired)
        pygame.draw.polygon(screen, self.outline_color, points,
                            width=2)  # width can be adjusted as needed

        front_offset = 20
        front_direction = pymunk.Vec2d(math.cos(self.body.angle),
                                       math.sin(self.body.angle))
        front_position = self.body.position + front_direction * front_offset

        marker_size = (6, 6)
        marker_rect = pygame.Rect(0, 0, *marker_size)
        marker_rect.center = (int(front_position.x), int(front_position.y))

        marker_angle = self.body.angle
        marker_surface = pygame.Surface(marker_size)
        marker_surface.fill(
            (255, 0, 0))  # Marker color (can also be made customizable)
        marker_surface.set_colorkey((0, 0, 0))

        rotated_marker = pygame.transform.rotate(marker_surface,
                                                 -math.degrees(marker_angle))
        rotated_rect = rotated_marker.get_rect(center=marker_rect.center)

        screen.blit(rotated_marker, rotated_rect.topleft)

        for sensor in self._sensors:
            sensor.draw(
                screen,
                self.body.position,
                self.body.angle,
            )  # contains a blit function
