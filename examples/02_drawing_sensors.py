import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot.human_controlled import HumanControlled
from src.simulator.simulator import Simulator
from src.robot.utils.sensor import Sensor

if __name__ == "__main__":
    robots = [
        HumanControlled(
            position=[550, 450],
            angle=0,
            size=[50, 30],
            center_of_rotation=[25, 15],
            sensors=[
                Sensor("sens1", [0, 0],
                       "rectangle",
                       color=(0, 100, 255),
                       size=[10, 10])
            ],
            base_color=(255, 100, 201),
        ),
    ]

    simulator = Simulator(
        robots,
        scaling_factor=1,
        tick=60,
        overlay_fps=True,
        overlay_font_size=30,
        overlays=[
            lambda: f"v1 = {robots[0].velocity}\n",
            lambda: f"angle1 = {robots[0].get_angle:0.2f}\n",
        ],
    )

    simulator.run()
