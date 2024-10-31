import pygame
import pymunk
import pygame.freetype as ft

from src.robot.robot import Robot


class Simulator:
    """
    A class to create and run a 2D robot simulation using Pygame and Pymunk.

    Attributes:
        robots (list[Robot]): A list of Robot instances to be simulated.
        scaling_factor (float): A factor to scale the display size.
        tick (int): The number of frames per second for the simulation.
        overlay_fps (bool): If True, display the current frames per second.
        overlay_font_size (int): Font size for overlay text.
        overlays (list): A list of additional overlays to display.
    """

    def __init__(self,
                 robots: list[Robot],
                 scaling_factor: float = 1,
                 tick: int = 60,
                 overlay_fps: bool = True,
                 overlay_font_size: int = 15,
                 overlays: list = []):
        """
        Initializes the Simulator.

        Args:
            robots (list[Robot]): A list of Robot instances to be simulated.
            scaling_factor (float): A factor to scale the display size.
            tick (int): The number of frames per second for the simulation.
            overlay_fps (bool): If True, display the current frames per second.
            overlay_font_size (int): Font size for overlay text.
            overlays (list): A list of additional overlays to display.

        Example:
            robot1 = Robot(position=[100, 100], angle=0, size=[50, 30], center_of_rotation=[25, 15], sensors={})
            simulator = Simulator(robots=[robot1], scaling_factor=1, tick=60, overlay_fps=True)
        """
        pygame.init()
        self._tick = tick
        self._overlays = overlays
        self._overlay_font_size = overlay_font_size
        self.screen = pygame.display.set_mode(
            (int(1600 * scaling_factor), int(900 * scaling_factor)), )
        #! pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = ft.SysFont("Verdana", self._overlay_font_size)

        if overlay_fps:
            self._overlays = [lambda: f"fps = {self.clock.get_fps():.2f}\n"
                              ] + self._overlays

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self._robots = robots

        for robot in self._robots:
            self.space.add(robot.get_body, robot.get_shape)

    def set_tick(self, tick: int):
        """
        Set the tick rate for the simulation.

        Args:
            tick (int): The new tick rate.

        Example:
            simulator.set_tick(30)  # Set the simulation to run at 30 frames per second
        """
        self._tick = tick

    @property
    def get_tick(self) -> int:
        """
        Get the current tick rate.

        Returns:
            int: The current tick rate.

        Example:
            current_tick = simulator.get_tick
        """
        return self._tick

    def draw(self):
        """
        Draw all robots and overlays on the screen.

        This method clears the screen, draws each robot, and then renders the overlays.
        """
        self.screen.fill((255, 255, 255))

        for robot in self._robots:
            robot.draw(self.screen)

        self.draw_overlay()

    def draw_overlay(self):
        """
        Draw the overlay text on the screen.
        
        This method compiles the overlay text and renders it to the screen.
        """
        overlays = ''
        for overlay in self._overlays:
            overlays += overlay()
        _overlays = overlays.split('\n')
        if overlays != '':
            for overlay_number in range(len(_overlays)):
                self.font.render_to(
                    self.screen, (0, self._overlay_font_size * overlay_number),
                    text=_overlays[overlay_number],
                    fgcolor="green",
                    bgcolor="black")

    def event_handler(self, events):
        """
        Handle events from Pygame.

        Args:
            events: The list of events to handle.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            #! if event.type == pygame.VIDEORESIZE:
            #!     self.screen = pygame.display.set_mode(event.size,
            #!                                           pygame.RESIZABLE)

    def run(self):
        """
        Run the simulation loop.

        This method handles event processing, updates the robots, steps the Pymunk space, and draws the screen.
        
        Example:
            simulator.run()  # Start the simulation loop
        """
        self.running = True
        while self.running:
            events = pygame.event.get()
            self.event_handler(events)

            for robot in self._robots:
                robot.update(self.clock.get_fps(), events)

            self.space.step(1 / self._tick)

            self.draw()
            pygame.display.flip()
            self.clock.tick(self._tick)

        pygame.quit()
