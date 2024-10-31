import pygame

from src.simulator.simulator import Simulator


class MazeSim(Simulator):
    number_of_collisions_occurred: int = 0

    def __init__(
        self,
        robots,
        map_file: str,
        scaling_factor=1,
        tick=60,
        overlay_fps=True,
        overlay_font_size=15,
        overlays=[],
    ):
        """
        Initialize the MazeSim with map loading and collision detection.
        
        Args:
            robots (list): List of Robot instances.
            map_file (str): The path to the maze map image file (PNG or SVG).
            scaling_factor (float): Scaling factor for display.
            tick (int): Frames per second.
            overlay_fps (bool): Display FPS overlay.
            overlay_font_size (int): Font size for overlays.
            overlays (list): Additional overlays.
        """
        super().__init__(robots, scaling_factor, tick, overlay_fps,
                         overlay_font_size, overlays)

        try:
            self._map_image = pygame.image.load(map_file)
        except Exception as e:
            raise RuntimeError("Unable to load the map\n", e)

        self._map_image.set_colorkey((0, 0, 0))
        self._map_size: list[int] = [min(self.screen.get_size())] * 2
        self._map_position = pygame.Vector2(
            self.screen.get_size()[0] - self._map_size[0],
            self.screen.get_size()[1] - self._map_size[1])
        self._map_image = pygame.transform.scale(
            self._map_image,
            self._map_size,
        )
        self._map_mask = pygame.mask.from_surface(self._map_image)
        self._map_mask.invert()

    def draw(self):
        """
        Draw the map and robots on the screen.
        """
        self.screen.fill((255, 0, 255))

        if self._map_image != None:
            self.screen.blit(
                self._map_image,
                self._map_position,
            )

        for robot in self._robots:
            robot.draw(self.screen)
            if self.detect_collision(robot):
                self.number_of_collisions_occurred += 1
                print(
                    f"Oops you collided! Total number of collisions occurred = {self.number_of_collisions_occurred}"
                )
        self.draw_overlay()

    def detect_collision(self, robot) -> bool:
        """
        Detect collision for a robot with the maze walls.
        
        Args:
            robot: The robot instance for which to check collision.
        
        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        pos: pygame.Vector2 = pygame.Vector2(
            robot.body.position[0] - (robot._size[0] * 1),
            robot.body.position[1] - (robot._size[1] * 1.375))
        if self._map_mask.overlap(
                robot.robot_mask,
            [pos[0] - self._map_position[0], pos[1] - self._map_position[1]
             ]) != None:
            return True
        return False
