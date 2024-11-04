import pygame as pg
import pygame.freetype as ft

from src.robot.robot import Robot


class Simulator:
    """
    A class to create and run a 2D robot simulation using Pygame.

    Attributes:
        robots (list[Robot]): A list of Robot instances to be simulated.
        scaling_factor (float): A factor to scale the display size.
        tick (int): The number of frames per second for the simulation.
        overlay_fps (bool): If True, display the current frames per second.
        overlay_font_size (int): Font size for overlay text.
        overlays (list): A list of additional overlays to display.
    """
    _map_mask: pg.Mask = None
    """Must be defined in child class"""
    _map_position: pg.Vector2 = None
    """Must be defined in child class"""

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
            simulator.run()
        """
        pg.init()
        self._tick = tick
        self._overlays = overlays
        self._overlay_font_size = overlay_font_size
        self.screen = pg.display.set_mode(
            (int(1600 * scaling_factor), int(900 * scaling_factor)), )
        #! pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.font = ft.SysFont("Verdana", self._overlay_font_size)

        if overlay_fps:
            self._overlays.insert(
                0,
                lambda: f"fps = {self.clock.get_fps():.2f}\n",
            )

        self._robots = robots

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
                    self.screen,
                    (
                        0,
                        self._overlay_font_size * overlay_number,
                    ),
                    text=_overlays[overlay_number],
                    fgcolor="green",
                    bgcolor="black",
                )

    def event_handler(self, events):
        """
        Handle Pygame events, including quitting the simulation.

        Args:
            events: The list of events to handle.
        """
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            #! if event.type == pg.VIDEORESIZE:
            #!     self.screen = pg.display.set_mode(event.size,
            #!                                           pg.RESIZABLE)

    def run(self):
        """
        Run the simulation loop.

        This method handles event processing, updates the robots, and draws the screen.
        
        Example:
            simulator.run()  # Start the simulation loop
        """
        self.running = True
        while self.running:
            events = pg.event.get()
            self.event_handler(events)

            for robot in self._robots:
                robot.update(self.clock.get_fps(), events)
                for sensor in robot._sensors:
                    sensor.calculate_sensor_data(
                        robot.get_position(),
                        robot.get_angle(),
                        self._map_mask,
                        self._map_position,
                    )

            self.draw()
            pg.display.flip()
            self.clock.tick(self._tick)

        pg.quit()
