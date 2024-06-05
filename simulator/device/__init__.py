"""
设备模块
"""
from abc import ABC, abstractmethod


class Device(ABC):
    """设备的抽象类"""

    @abstractmethod
    def process(self):
        """设备的主要逻辑"""
