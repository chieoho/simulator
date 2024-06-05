""""
模拟器的主要逻辑
"""

from multiprocessing import Process, cpu_count
import time
import os

import simpy

from simulator.device.robot import Robot, RobotInfo
from simulator.communication.tcp_client import TcpClient


class Simulation(Process):
    """模拟器类"""

    def __init__(self, env, device_list):
        self.env = env
        self.device_list = device_list
        print(f"id{sum(self.device_list)} init:{os.getpid()}")
        super().__init__()

    def init_device(self, comm):
        """初始化设备"""
        print(f"id{sum(self.device_list)} init_device:{os.getpid()}")
        for i in self.device_list:
            self.env.process(Robot(self.env, RobotInfo(i), comm).process())

    def run(self):
        print(f"id{sum(self.device_list)} run:{os.getpid()}")
        print(f"run {time.time()}")

        tcp_client = TcpClient()
        tcp_client.start()
        self.init_device(tcp_client)

        self.env.run()


def start_simulation(device_list):
    """启动模拟器"""
    cpu_num = cpu_count()
    batch_size = len(device_list) // cpu_num
    test_env = simpy.RealtimeEnvironment(factor=1, strict=False)

    processes = [
        Simulation(test_env, device_list[i * batch_size : (i + 1) * batch_size])
        for i in range(cpu_num)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
