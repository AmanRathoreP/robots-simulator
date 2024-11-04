import os
import sys
import math

import pygame as pg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot.human_controlled import HumanControlled
from src.simulator.line_follower import LineSim
from src.robot.utils.sensor import IRSensor
import src.utils.helper_functions as hf


def create_ir_sensors() -> list[IRSensor]:
    positions = [-14, -10, -6, -2, 2, 6, 10, 14]
    return [
        IRSensor(f"l{i}", [20, pos]) if pos < 0 else IRSensor(
            f"r{i-4}", [20, pos]) for i, pos in enumerate(positions, 1)
    ]


class PIDController:

    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def calculate(self, error: float, delta_time: float) -> float:
        self.integral += error * delta_time
        self.derivative = (error - self.previous_error) / delta_time
        self.output = (self.kp * error) + (self.ki * self.integral) + (
            self.kd * self.derivative)
        self.previous_error = error
        return self.output


class SimplePIDLineFollower(HumanControlled):
    auto_driving: bool = True

    def __init__(self, *args, kp=2000, ki=0, kd=1500, **kwargs):
        super().__init__(*args, **kwargs)
        self.pid_controller = PIDController(kp, ki, kd)

    def event_handler(self, events):
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_k:
                self.auto_driving = not self.auto_driving

        if not self.auto_driving:
            super().event_handler(events)

    def update(self, time_step: float, events):
        if self.auto_driving:
            correction = self.pid_controller.calculate(
                self.get_error,
                1 / 60 if time_step == 0 else time_step,
            )
            self.set_angular_acceleration(correction / 95000000)
            self.set_acceleration([0.00045, 0])
        super().update(time_step, events)

    @property
    def get_error(self):
        return SimplePIDLineFollower.get_turn_from_ir_sensors(
            [sensor.is_on for sensor in self._sensors])

    @classmethod
    def get_turn_from_ir_sensors(cls, ir_sensors_value: list[bool]) -> float:
        weights = [-1, -1, -1, -1, 1, 1, 1, 1]
        # weights = [-4, -3, -2, -1, 1, 2, 3, 4]
        weighted_sensors = [
            sensor * weight
            for sensor, weight in zip(ir_sensors_value, weights)
        ]
        return sum(weighted_sensors)


if __name__ == "__main__":
    robots = [
        SimplePIDLineFollower(
            position=[1016, 600],
            angle=math.radians(200),
            size=[16, 25],
            center_of_rotation=[30, 15],
            sensors=create_ir_sensors(),
            base_color=(255, 100, 201),
        ),
    ]

    simulator = LineSim(
        robots,
        "assets/line follower track.png",
        scaling_factor=0.7,
        tick=60,
        overlay_fps=True,
        overlay_font_size=30,
        overlays=[
            lambda:
            f"v1*10^3 = {hf.round_vec_2d(robots[0].get_velocity()*1000)}\n",
            lambda:
            f"angular_v1x10^6 = {round(robots[0].get_angular_velocity() * 1000000, 3)}\n",
            lambda: f"pos = {hf.round_vec_2d(robots[0].get_position(), 0)}\n",
            lambda: f"angle1 = {robots[0].get_angle():0.2f}\n",
        ],
    )

    simulator.run()
