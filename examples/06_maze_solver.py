import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import math
import random
import time
import pygame as pg
import numpy as np
import pandas as pd

from src.robot.human_controlled import HumanControlled
from src.simulator.maze_solver import MazeSim
from src.robot.utils.sensor import LIDARSensor
import src.utils.helper_functions as hf
from examples.helpers.micro_mouse_maze import MicroMouseMaze
from examples.helpers.control_systems import PIDController as PID

l = logging.getLogger(__name__)


class MicroMouseController:
    _last_updated_on: float = -1
    commands: pd.DataFrame = pd.DataFrame(
        columns=["command", "argument", "status", "error"])
    maze_data: pd.DataFrame = pd.DataFrame(
        columns=["current_cell", "facing", "right", "front", "left"])
    maze = MicroMouseMaze(size=16)

    save_data_every_n_commands = 10
    commands_stack = []

    stack: list[int] = []

    def __init__(
        self,
        initial_position: list[float],
        initial_angle: float,
        cell_width_height=35,
        wall_width=4,
        starting_cell: int = 0,
    ) -> None:
        self.starting_position: pg.Vector2 = pg.Vector2(initial_position)
        self.position: pg.Vector2 = pg.Vector2(initial_position)
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.angle: float = initial_angle
        self.angular_velocity: float = 0.0
        self.cell_width_height = cell_width_height
        self.wall_width = wall_width
        self.starting_cell = starting_cell
        self.current_cell = self.starting_cell
        
        self.__start_time_stamp = time.strftime("%Y-%m-%d, %H%M%S")

    def update(
        self,
        position: pg.Vector2,
        angle: float,  #degrees
        lidar_data: list[int],
        previous_command_status: bool = False,
    ):
        l.debug("In update of MMC")
        try:
            self.position = position
            angle = angle % 360

            if hf.calculate_error_and_round(
                    hf.map_value(
                        angle,
                        0,
                        360,
                        0,
                        4,
                    ),
                    error_margin=5,
            ) == None:
                #* angle is not near the 0, 90, 180, 270
                l.debug(f"Error in update of MMC due to angles({angle})")
                raise TypeError  #todo

            # Determine facing direction based on the angle
            if 45 <= angle < 135:
                facing_direction = 'south'
            elif 135 <= angle < 225:
                facing_direction = 'west'
            elif 225 <= angle < 315:
                facing_direction = 'north'
            else:
                facing_direction = 'east'

            __x_rel =hf.calculate_error_and_round(hf.map_value(self.position.x, 1102, 515, 0, -15))
            __y_rel = hf.calculate_error_and_round(hf.map_value(self.position.y, 606, 24, 0, 15))
            l.debug(f"476, __x_rel = {__x_rel}, __y_rel = {__y_rel}")
            pos_in_cell_num = pg.Vector2(
                __x_rel[0],
                __y_rel[0],
            ) #* throws type error if calculate_error_and_round returns None
            l.debug("784")

            self.current_cell = abs(pos_in_cell_num.x) + abs(
                pos_in_cell_num.y * 16)

            l.info(f"CURRENT CELL: {self.current_cell}")
            l.info(f"POSITION: {position}")
            l.info(f"ANGLE: {angle}")

            
            if len(self.stack) > 0:
                l.debug("244")
                if self.stack[-1] != self.current_cell:
                    l.debug("987")
                    self.stack.append(self.current_cell)
                    __maze_data = [
                        lidar_data[4] > 35,
                        lidar_data[2] > 35,
                        lidar_data[0] > 35,
                    ]
                    l.info(f"LIDAR INFO: {[
                        lidar_data[4] ,
                        lidar_data[2] ,
                        lidar_data[0] ,
                    ]}")
                    self.maze_data.loc[self.maze_data.shape[0]] = [
                        self.current_cell,
                        facing_direction,
                        __maze_data[0],
                        __maze_data[1],
                        __maze_data[2],
                    ]
                    l.info(f"MAZE DATA: {[
                        self.current_cell,
                        facing_direction,
                        __maze_data[0],
                        __maze_data[1],
                        __maze_data[2],
                    ]}")
                    self.maze.add_edges(
                        current_node=self.current_cell,
                        right=__maze_data[0],
                        front=__maze_data[1],
                        left=__maze_data[2],
                        facing_direction=facing_direction,
                    )

                    if self.current_cell in [118, 119, 134, 135]:
                        self.maze_data.to_csv(
                            f"bin/mazes/maze_data {self.__start_time_stamp}.csv",
                            index=False,
                        )
                        print(f"One of the mid points(118, 119, 134, 135) i.e. {self.current_cell} is reached.")
                        exit()
                        
                    if self.commands.shape[
                            0] % self.save_data_every_n_commands == 0:
                        self.maze_data.to_csv(
                            f"bin/mazes/maze_data {self.__start_time_stamp}.csv",
                            index=False,
                        )
                        self.commands.to_csv(
                            f"bin/commands/commands {self.__start_time_stamp}.csv",
                            index=False,
                        )

            else:
                self.stack.append(self.starting_cell)
                self.maze.add_edges(
                    current_node=self.starting_cell,
                    front=True,
                    facing_direction=facing_direction,
                )
                self.maze_data.loc[self.maze_data.shape[0]] = [
                    self.starting_cell,
                    facing_direction,
                    False,
                    True,
                    False,
                ]
                l.info(f"MAZE DATA: {[
                    self.starting_cell,
                    facing_direction,
                    False,
                    True,
                    False,
                ]}")
            if not previous_command_status:
                # do nothing if previous command is running
                l.debug("Returning as previous command is not finished!")
                
                return -1
            else:
                self.commands.loc[
                    self.commands.shape[0] - 1,
                    "status",
                ] = True
                command_options = []
                command = None
                if len(self.commands_stack) == 0:
                    l.debug(f"471")
                    
                    if lidar_data[0] > 35:
                        command_options.append([
                            'r',
                            hf.normalize_angle_90(angle - 90), False, None
                        ])
                    if lidar_data[4] > 35:
                        command_options.append([
                            'r',
                            hf.normalize_angle_90(angle + 90), False, None
                        ])
                    if lidar_data[2] > 35:
                        command_options.append(['l2', 35 / 2, False, None])
                    if len(command_options) == 0:
                        l.debug("543")
                        self.commands_stack = self.maze.generate_shortest_path_commands(
                            self.stack[-1],
                            self.maze.get_cell_to_explore(self.stack),
                            initial_facing=facing_direction,
                            cell_width_hight=self.cell_width_height,
                        )[::-1]
                        l.debug(f"612, self.commands_stack = {self.commands_stack}")
                        command_options.append([
                            self.commands_stack[-1][0],
                            self.commands_stack[-1][1],
                            False,
                            None,
                        ], )
                        self.commands_stack.pop()
                    l.debug("154")
                    l.debug(f"161{command_options}")
                else:
                    l.debug(f"347, self.commands_stack[-1] = {self.commands_stack[-1]}")
                    command_options.append([
                        self.commands_stack[-1][0],
                        self.commands_stack[-1][1],
                        False,
                        None,
                    ], )
                    self.commands_stack.pop()
                for cm in command_options:
                    if cm[0] == "l2":
                        command = cm
                        break
                # Select a random command from the options
                command = random.choice(
                    command_options) if command == None else command
                self.commands.loc[self.commands.shape[0]] = command
                # print(self.commands)
                l.info(f"COMMAND: {command}")
                # print(command_options, command)
                print(command)
                return command[:2]
        except TypeError:
            # when returns None i.e. when angle or position has a huge offset; im simple words when car is not in a stable state
            l.debug(f"Ending MMC due to error in angle({angle}) or position{position}")
            return -1
        return -1


class customHumanControlled(HumanControlled):
    __log_file_name: str = f"bin/micromouse_data_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    __mm_data = None

    translate_cart: bool = False
    tc_target = None
    tc_accepted_error = 1
    rotate_cart: bool = False
    rc_target = None
    rc_accepted_error = 2
    
    tcPID = PID(10, 0, 0)
    rcPID = PID(0.2, 0, 0)

    current_command = ['n', 0, False, None]

    def __init__(
        self,
        position: list[int],
        angle: float,
        size: list[int],
        center_of_rotation: list[float],
        sensors: list,
        base_color: tuple[int, int, int] = (0, 128, 255),
        outline_color: tuple[int, int, int] = (0, 0, 0),
        trigger=lambda: False,
    ):
        super().__init__(position, angle, size, center_of_rotation, sensors,
                         base_color, outline_color)
        self.trigger = trigger
        self.mouse = MicroMouseController(
            initial_position=position,
            initial_angle=angle,
        )

        self.__acc_values = np.random.binomial(1300, 0.9, size=100000)
        self.__ang_acc_values = np.random.binomial(80, 0.8, size=100000)

    def event_handler(self, events):
        #! pg.key.set_repeat(1)
        if self.trigger():
            super().event_handler(events)
            keys = pg.key.get_pressed()  # Get the current state of all keys
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.set_angular_acceleration(0)
                        self.set_angular_velocity(0)

                if keys[pg.K_UP]:
                    self.set_acceleration(
                        [random.choice(self.__acc_values), 0])
                elif keys[pg.K_DOWN]:
                    self.set_acceleration(
                        [-random.choice(self.__acc_values), 0])
                else:
                    self.set_acceleration([0, 0])

                # Control for turning
                if keys[pg.K_LEFT]:  # Turn left
                    self.set_angular_acceleration(
                        -random.choice(self.__ang_acc_values))
                elif keys[pg.K_RIGHT]:  # Turn right
                    self.set_angular_acceleration(
                        random.choice(self.__ang_acc_values))
                else:
                    self.set_angular_acceleration(0)

                if keys[pg.K_b]:
                    self.__mm_data.to_csv(self.__log_file_name, index=False)

    def update(self, time_step: float, events):
        try:
            dt = 1 / time_step
        except ZeroDivisionError:
            # The simulation is still not started as a whole
            return

        __pos = self.get_position()
        __angle = self.get_angle()
        command = self.mouse.update(
            __pos,
            __angle,
            [self._sensors[i].distance for i in range(len(self._sensors))],
            previous_command_status=(not self.translate_cart)
            and (not self.rotate_cart),
        )
        
        l.debug("217")
        

        if command != -1:
            l.debug(f"546, command = {command}")
            
            self.translate_cart = False
            self.rotate_cart = False
            self.current_command = command
            if command[0] == 'f':
                self.translate_cart = True
                self.tc_target = command[1]
            elif command[0] == 'r':
                self.rotate_cart = True
                self.rc_target = command[1]
            elif command[0][0] == 'l':
                self.translate_cart = True

        l.debug(f"148, self.translate_cart = {self.translate_cart}")
        if self.translate_cart:
            l.debug("570")
            if self.current_command[0][0] == 'l':
                l.debug("470")
                self.set_acceleration([
                    self.tcPID.calculate(
                        self._sensors[int(self.current_command[0][1])].distance
                        - self.current_command[1],
                        dt,
                    ),
                    0,
                ])
                l.debug("157")
                if abs(self.current_command[1] -
                       self._sensors[int(self.current_command[0][1])].distance
                       ) < self.tc_accepted_error:
                    self.translate_cart = False
                    self.set_acceleration([0, 0])
                    l.debug(f"981, {self.current_command[1] -self._sensors[int(self.current_command[0][1])].distance}")
            else:
                self.set_acceleration([
                    self.tcPID.calculate(
                        self.tc_target - __pos[0],
                        dt,
                    ),
                    0,
                ])
                if abs(self.tc_target - __pos[0]) < self.tc_accepted_error:
                    self.set_acceleration([0, 0])
                    self.translate_cart = False

        if self.rotate_cart:
            diff = (__angle - self.rc_target) % 360
            diff -= 360 if diff > 180 else 0  # making sure that it will travel -90 degree left for 270 degree right
            diff *= -1  #direction correction
            self.set_angular_acceleration(self.rcPID.calculate(
                diff,
                dt,
            ), )
            if abs(diff) < self.rc_accepted_error:
                self.rotate_cart = False
                self.set_angular_acceleration(0)

        data = {
            'Time': time.time(),
            'Position_X': __pos.x,
            'Position_Y': __pos.y,
            'Velocity_X': self.get_velocity().x,
            'Velocity_Y': self.get_velocity().y,
            'Acceleration': self.acceleration[0],
            'Angle': math.radians(__angle),
            'Angular_Velocity': self.get_angular_velocity(),
            'Angular_Acceleration': self.get_angular_acceleration(),
        }

        df = pd.DataFrame([data])
        if self.__mm_data is not None:
            self.__mm_data = pd.concat(
                [self.__mm_data, df],
                ignore_index=True,
                sort=False,
            )
        else:
            self.__mm_data = df.copy()

        super().update(time_step, events)


class customLIDARSensor(LIDARSensor):
    angle_to_position: dict = {
        0: [0, 0],
        -45: [7 - 2, -10 / 2 + 2],
        45: [7 - 2, 10 / 2 - 2],
        -90: [0, 0],
        90: [0, 0],
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
            lidar_max_distance=213,
        )


if __name__ == "__main__":
    logging.basicConfig(
        filename=f"bin/logs/{time.strftime('logs %Y-%m-%d, %H%M%S')}.log",
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',
    )

    robots = [
        customHumanControlled(
            position=[1102, 606],
            # position=[515, 606],
            # position=[515, 24],
            # position=[1102, 24],
            angle=math.radians(180),
            size=[14, 10],
            center_of_rotation=[30, 15],
            sensors=[
                customLIDARSensor(angle=-90),
                customLIDARSensor(angle=-22.5),
                customLIDARSensor(angle=0),
                customLIDARSensor(angle=22.5),
                customLIDARSensor(angle=90),
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
            f"position = {hf.round_vec_2d(robots[0].get_position(), 0)}\n",
            lambda: f"v = {hf.round_vec_2d(robots[0].get_velocity())}\n",
            lambda: f"a = {robots[0].acceleration}\n",
            lambda: f"angle = {robots[0].get_angle():0.2f}\n",
            lambda:
            f"angular_v = {round(robots[0].get_angular_velocity(), 3)}\n",
            lambda:
            f"angular_a = {round(robots[0].get_angular_acceleration(), 3)}\n",
            lambda: "LIDAR Front: [" + ", ".join(
                f"{robots[0]._sensors[i].distance}"
                for i in range(len(robots[0]._sensors))) + "]\n",
            lambda:
            f"position = {hf.round_vec_2d(robots[0].mouse.position, 3)}\n",
        ],
    )

    simulator.run()
