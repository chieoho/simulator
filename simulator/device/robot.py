"""
机器人类
"""

import os
import time
from dataclasses import dataclass

from simpy import RealtimeEnvironment

from simulator.device import Device
from simulator.communication.tcp_client import TcpClient


@dataclass
class RobotInfo:
    """机器人信息"""

    robot_id: int
    server_ip: str = "localhost"
    server_port: int = 12345


class Robot(Device):
    """机器人类"""

    def __init__(
        self, env: RealtimeEnvironment, robot_info: RobotInfo, comm: TcpClient
    ):
        self.env = env
        self.robot_info = robot_info
        self.device_id = robot_info.robot_id
        self.comm = comm

        self.comm.register_device(
            self.device_id,
            (self.robot_info.server_ip, self.robot_info.server_port),
        )

    def update_state(self, event):
        """
        更新机器人状态
        """
        print(
            f"pid:{os.getpid()} Robot{self.device_id}更新状态，模拟器时间: {event.env.now}，现实时间: {time.time()} {event.env.now / (time.monotonic() - event.env.real_start) * 100}%"
        )
        self.comm.response(self.device_id, "OK")

    def handle_cmd(self, cmd):
        """
        处理命令
        """
        return int(cmd) ** 0.5 ** 2

    def process(self):
        while True:
            if cmd := self.comm.get_cmd(self.device_id):
                event = self.env.timeout(self.handle_cmd(cmd))
                event.callbacks.append(self.update_state)
                yield event
            else:
                yield self.env.timeout(0.001)
