import os
import sys

import pygame as pg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot.human_controlled import HumanControlled
from src.simulator.maze_solver import MazeSim
from src.robot.utils.sensor import LIDARSensor


class customHumanControlled(HumanControlled):

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
        trigger=lambda: False,
    ):
        super().__init__(position, angle, size, center_of_rotation, sensors,
                         base_color, outline_color)
        self.trigger = trigger

    def event_handler(self, events):
        if self.trigger():
            super().event_handler(events)


class customLIDARSensor(LIDARSensor):
    angle_to_position: dict = {
        0: [7 - 2, 0],
        -45: [7 - 2, -10 / 2 + 2],
        45: [7 - 2, 10 / 2 - 2],
        -22.5: [7 - 2, -10 / 2 + 2],
        22.5: [7 - 2, 10 / 2 - 2],
    }

    def __init__(
        self,
        angle: float = 45,
    ):
        super().__init__(
            f"{angle}",
            self.angle_to_position[angle],
            angle,
            [3, 3],
            color=(255, 0, 0),
        )


if __name__ == "__main__":
    robots = [
        customHumanControlled(
            position=[250, 450],
            angle=0,
            size=[14 * 5, 10 * 5],
            center_of_rotation=[30, 15],
            sensors=[
                LIDARSensor(
                    "sens1",
                    [7 * 5 - 6, -10 * 5 / 2 + 6],
                    angle=-45,
                    color=(0, 100, 255),
                    size=[12, 12],
                ),
                LIDARSensor(
                    "sens2",
                    [7 * 5 - 6, 0],
                    angle=0,
                    color=(111, 0, 188),
                    size=[12, 12],
                ),
                LIDARSensor(
                    "sens3",
                    [7 * 5 - 6, 10 * 5 / 2 - 6],
                    angle=45,
                    color=(111, 100, 0),
                    size=[12, 12],
                ),
            ],
            base_color=(255, 100, 201),
            trigger=lambda: True
            if pg.key.get_pressed()[pg.K_LCTRL] else False,
        ),
        customHumanControlled(
            position=[550, 450],
            angle=0,
            size=[14, 10],
            center_of_rotation=[30, 15],
            sensors=[
                customLIDARSensor(angle=-45),
                customLIDARSensor(angle=-22.5),
                customLIDARSensor(angle=0),
                customLIDARSensor(angle=22.5),
                customLIDARSensor(angle=45),
            ],
            base_color=(10, 100, 88),
            trigger=lambda: False
            if pg.key.get_pressed()[pg.K_LCTRL] else True,
        ),
    ]

    simulator = MazeSim(
        robots,
        "assets/16x16 sample maze for testing.svg",
        scaling_factor=0.7,
        tick=60,
        overlay_fps=True,
        overlay_font_size=20,
        overlays=[
            lambda:
            f"v2 = [{round(robots[1].get_velocity().x, 6)}, {round(robots[1].get_velocity().y, 6)}]\n",
            lambda:
            f"angular_v2x10^6 = {round(robots[1].get_angular_velocity() * 1000000, 3)}\n",
            lambda: f"angle2 = {robots[1].get_angle():0.2f}\n",
            lambda: "LIDAR Front: [" + ", ".join(
                f"{robots[1]._sensors[i].distance}"
                for i in range(len(robots[1]._sensors))) + "]\n",
        ],
    )

    simulator.run()
