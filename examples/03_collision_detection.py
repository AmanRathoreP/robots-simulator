import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot.human_controlled import HumanControlled
from src.simulator.maze_solver import MazeSim
from src.robot.utils.sensor import Sensor

if __name__ == "__main__":
    robots = [
        HumanControlled(
            position=[550, 450],
            angle=0,
            size=[14, 10],
            center_of_rotation=[30, 15],
            sensors=[
                Sensor(
                    "sens1",
                    [7, -5],
                    "rectangle",
                    color=(0, 100, 255),
                    size=[5, 5],
                ),
                Sensor(
                    "sens2",
                    [8, 1],
                    "rectangle",
                    color=(111, 0, 188),
                    size=[5, 5],
                ),
                Sensor(
                    "sens3",
                    [7, 7],
                    "rectangle",
                    color=(111, 100, 0),
                    size=[5, 5],
                ),
            ],
            base_color=(255, 100, 201),
        ),
    ]

    simulator = MazeSim(
        robots,
        "assets/16x16 sample maze for testing.svg",
        scaling_factor=0.7,
        tick=60,
        overlay_fps=True,
        overlay_font_size=30,
        overlays=[
            lambda:
            f"v1 = [{round(robots[0].get_velocity().x, 6)}, {round(robots[0].get_velocity().y, 6)}]\n",
            lambda:
            f"angular_v1x10^6 = {round(robots[0].get_angular_velocity() * 1000000, 3)}\n",
            lambda: f"angle1 = {robots[0].get_angle():0.2f}\n",
        ],
    )

    simulator.run()
