import socket
import os
import select
from threading import Thread
import time


def recv_cmd(epoll):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.setblocking(0)
    file_no = client_socket.fileno()
    epoll.register(file_no, select.EPOLLIN) 
    client_socket.send("Robot connected".encode())
    time.sleep(1)

    while True:
        events = epoll.poll()
        for fileno, event in events:
            if event & select.EPOLLIN:
                # 有新的数据
                data = os.read(fileno, 1024)
                if data:
                    print(data.decode())
                else:
                    # 连接已关闭
                    epoll.unregister(fileno)
                    socket.close(fileno)

if __name__ == "__main__":
    epoll = select.epoll()
    t = Thread(target=recv_cmd, args=(epoll,))
    t.start()
