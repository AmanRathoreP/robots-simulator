import pygame as pg

from src.simulator.simulator import Simulator


class LineSim(Simulator):

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
        Initialize the LineSim with map loading.
        
        Args:
            robots (list): List of Robot instances.
            map_file (str): The path to the map image file (PNG or SVG).
            scaling_factor (float): Scaling factor for display.
            tick (int): Frames per second.
            overlay_fps (bool): Display FPS overlay.
            overlay_font_size (int): Font size for overlays.
            overlays (list): Additional overlays.
        """
        super().__init__(robots, scaling_factor, tick, overlay_fps,
                         overlay_font_size, overlays)

        try:
            self._map_image = pg.image.load(map_file)
        except Exception as e:
            raise RuntimeError("Unable to load the map\n", e)

        self._map_image.set_colorkey((255, 255, 255, 255))
        self._map_size: list[int] = [min(self.screen.get_size())] * 2
        self._map_position = pg.Vector2(
            self.screen.get_size()[0] - self._map_size[0],
            self.screen.get_size()[1] - self._map_size[1])
        self._map_image = pg.transform.scale(
            self._map_image,
            self._map_size,
        )
        self._map_mask = pg.mask.from_surface(self._map_image)
        self._map_mask.invert()
        #* updating map image to remove the background
        self._map_image: pg.Surface = self._map_mask.to_surface()
        self._map_image.set_colorkey((255, 255, 255, 255))

    def draw(self):
        """
        Draw the map and robots on the screen.
        """
        self.screen.fill((100, 0, 255))

        if self._map_image != None:
            self.screen.blit(
                self._map_image,
                self._map_position,
            )

        for robot in self._robots:
            robot.draw(self.screen)
        self.draw_overlay()
