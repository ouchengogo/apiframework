# -*- coding: utf-8 -*-
# author: edward
# date: 2020-8-29
# contact: ouchen1989@tom.com


"""

"""
import argparse
import time
import socket

from utils.utils import Utils
from common.common import Common


class Base:
    def __init__(self):
        pass

    @classmethod
    def created_server_base_ipv4(cls, host: str, port: int, num_connections: int = 5, timeout: int = 30):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(num_connections)
            server_socket.settimeout(timeout)  # 超时时间
            Utils.info(info_string='服务端开启监听,服务地址为：{}:{}'.format(host, port))
            return server_socket
        except Exception as e:
            Utils.error(error_string='服务端创建失败，失败原因为：{}'.format(e))
            server_socket.close()
            return None

    @classmethod
    def created_client_base_ipv4(cls, host, port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            Utils.info(info_string='TCP_IPV4客户端创建成功，其名称为：{}'.format(client_socket.getsockname()))
            return client_socket
        except Exception as e:
            Utils.error(error_string='TCP_IPV4客户端创建失败，失败原因为：{}'.format(e))
            client_socket.close()
            return None

    @classmethod
    def close_client_base_ipv4(cls, client_socket: socket):
        try:
            client_socket.close()
            Utils.info(info_string='TCP_IPV4客户端关闭成功！')
        except BaseException as e:
            Utils.error(error_string='TCP_IPV4客户端关闭失败！')

    @classmethod
    def close_server_base_ipv4(cls, server_socket: socket):
        try:
            server_socket.close()
            Utils.info(info_string='TCP_IPV4服务端关闭成功！')
        except BaseException as e:
            Utils.error(error_string='TCP_IPV4服务端关闭失败！')


if __name__ == "__main__":
    bb1 = Base()
    client = bb1.created_client_base_ipv4(host='127.0.0.1', port=60002)
    client.sendall(b'\xe6\x01')
    time.sleep(1)
    client.sendall(b'\xe6\x02')
    time.sleep(1)
    client.sendall(b'\xe6\x03')
    time.sleep(3)
    client.sendall(b'\xe6\x04')
    time.sleep(6)
    client.sendall(b'\xe6\x05')
    bb1.close_client_base_ipv4(sock=client)