import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot.human_controlled import HumanControlled
from src.robot.robot import Robot
from src.simulator.simulator import Simulator

if __name__ == "__main__":
    robots = [
        HumanControlled(
            position=[550, 450],
            angle=0,
            size=[50, 30],
            center_of_rotation=[25, 15],
            sensors={},
            base_color=(255, 100, 201),
        ),
        Robot(
            position=[550, 550],
            angle=0,
            size=[50, 30],
            center_of_rotation=[25, 15],
            sensors={},
            outline_color=(0, 255, 0),
        ),
    ]

    robots[1].set_acceleration([1000, 0])
    robots[1].set_angular_acceleration(-10)

    simulator = Simulator(
        robots,
        scaling_factor=1,
        tick=60,
        overlay_fps=True,
        overlay_font_size=30,
        overlays=[
            lambda: f"v1 = {robots[0].get_velocity()}\n",
            lambda: f"angle1 = {robots[0].get_angle():0.2f}\n",
            lambda: f"v2 = {robots[1].get_velocity()}\n",
            lambda: f"angle2 = {robots[1].get_angle():0.2f}\n",
        ],
    )

    simulator.run()
