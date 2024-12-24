import logging

l = logging.getLogger(__name__)


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
