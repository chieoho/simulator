"""
TCP客户端
"""

import os
import select
import socket
from threading import Thread
from collections import deque, defaultdict


class TcpClient(Thread):
    """TCP客户端类"""

    def __init__(self):
        self.epoll = select.epoll()
        self.device_cmds_dict = defaultdict(deque)
        self.fd_device_dict = {}
        self.unconnected_device_queue = deque()
        self.device_client_dict = {}
        self.connected_batch_count = 0
        super().__init__()

    def register_device(self, device_id, server_info):
        """注册设备"""
        self.unconnected_device_queue.append((device_id, server_info))

    def _handle_unconnect(self):
        """处理未连接的设备"""
        while self.unconnected_device_queue:
            device_id, server_info = self.unconnected_device_queue.popleft()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(server_info)
            client_socket.setblocking(0)
            file_no = client_socket.fileno()
            self.epoll.register(file_no, select.EPOLLIN)
            self.fd_device_dict[file_no] = device_id
            client_socket.send(f"Robot{device_id} connected".encode())
            self.device_client_dict[device_id] = client_socket
            self.connected_batch_count += 1
            if self.connected_batch_count >= 64:
                self.connected_batch_count = 0
                break

    def get_cmd(self, device_id):
        """获取命令"""
        if self.device_cmds_dict[device_id]:
            return self.device_cmds_dict[device_id].popleft()
        return None

    def response(self, device_id, msg):
        """响应"""
        self.device_client_dict[device_id].send(msg.encode())

    def _recv_cmd(self):
        """接收命令"""
        events = self.epoll.poll(timeout=0.2)
        for file_no, event in events:
            if event & select.EPOLLIN:
                # 有新的数据
                data = os.read(file_no, 1024)
                if data:
                    # print(data.decode())
                    self.device_cmds_dict[self.fd_device_dict[file_no]].append(
                        data.decode()
                    )
                else:
                    # 连接已关闭
                    self.epoll.unregister(file_no)
                    socket.close(file_no)

    def run(self):
        """接收命令"""
        while True:
            self._handle_unconnect()
            self._recv_cmd()
