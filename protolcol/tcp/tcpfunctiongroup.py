# -*- coding: utf-8 -*-
# author: edward
# date: 2020-8-29
# contact: ouchen1989@tom.com


"""

"""
import argparse
import time
import socket
import struct
from typing import Union
from protolcol.tcp.tcpdriver import Base
from utils.utils import Utils
from common.common import Common

flag = 0
multipart_dict = {}


class TcpFunctionGroup(Base):
    @classmethod
    def server_receive_message_once(cls, server_socket: socket, buffer_size: int = 8192):
        try:
            while True:
                client_socket, address = server_socket.accept()
                Utils.info('收到来自“客户端 {}:{}”的连接请求，已建立连接'.format(address[0], address[1]))
                rev_data = TcpFunctionGroup.recive_message(sock=client_socket, buffer_size=buffer_size)
                if not rev_data or False is rev_data:
                    break
                else:
                    Utils.info(info_string='接收到“客户端 {}:{}”发送的消息：{}'.format(address[0], address[1], rev_data))
                    break
        except Exception as e:
            Utils.error('服务端与客户端建立连接并开启接收消息状态失败，失败原因为：{}'.format(e))
            server_socket.close()

    @classmethod
    def server_receive_message_forever(cls, server_socket: socket, buffer_size: int = 8192):
        """
        TODO 针对一个客户端连接后假如Utils.info语句后边的语句执行完后，会重新回到 sock, address = server_socket.accept()
        TODO 语句然后需要客户端主动与程序开启的服务端进行连接，才可以进入循环体，不太好
        """
        try:
            while True:
                client_socket, address = server_socket.accept()
                Utils.info('收到来自“客户端 {}:{}”的连接请求，已建立连接'.format(address[0], address[1]))
                while True:
                    rev_data = TcpFunctionGroup.recive_message(sock=client_socket, buffer_size=buffer_size)
                    if not rev_data or False is rev_data:
                        break
                    else:
                        Utils.info(info_string='接收到“客户端 {}:{}”发送的消息：{}'.format(address[0], address[1], rev_data))
        except Exception as e:
            Utils.error('服务端与客户端建立连接并开启接收消息状态失败，失败原因为：{}'.format(e))
            server_socket.close()

    @classmethod
    def server_send_message_once(cls, server_socket: socket, message: bytes):
        try:
            client_socket, address = server_socket.accept()
            Utils.info('收到来自“客户端 {}:{}”的连接请求，已建立连接'.format(address[0], address[1]))
            TcpFunctionGroup.send_message(sock=client_socket, message=message)
        except Exception as e:
            Utils.error('服务端向客户端 {}:{}发送消息失败，失败原因为：{}'.format(address[0], address[1], e))
            server_socket.close()

    @classmethod
    def server_send_message_forever(cls, server_socket: socket, message: bytes, interval: float = 0.1):
        try:
            while True:
                client_socket, address = server_socket.accept()
                Utils.info('收到来自“客户端 {}:{}”的连接请求，已建立连接'.format(address[0], address[1]))
                while True:
                    time.sleep(interval)
                    send_result = TcpFunctionGroup.send_message(sock=client_socket, message=message)
                    if send_result is False:
                        break
                    else:
                        continue
                break
        except Exception as e:
            Utils.error('服务端向客户端 {}:{}发送消息失败，失败原因为：{}'.format(address[0], address[1], e))
            server_socket.close()

    @classmethod
    def client_receive_message_once(cls, client_socket: socket, buffer_size: int = 8192):
        try:
            rev_data = TcpFunctionGroup.recive_message(sock=client_socket, buffer_size=buffer_size)
            if not rev_data or False is rev_data:
                Utils.error('客户端未接收到消息，服务端是否关闭了？')
            else:
                Utils.info(info_string='接收到服务端发送的消息：{}'.format(rev_data))
        except Exception as e:
            Utils.error('客户端与服务端建立连接并开启接收消息状态失败，失败原因为：{}'.format(e))
            client_socket.close()

    @classmethod
    def client_receive_message_forever(cls, client_socket: socket, buffer_size: int = 8192):
        try:
            while True:
                rev_data = TcpFunctionGroup.recive_message(sock=client_socket, buffer_size=buffer_size)
                if not rev_data or False is rev_data:
                    Utils.error('客户端未接收到消息，服务端是否关闭了？')
                    break
                else:
                    Utils.info(info_string='接收到服务端发送的消息：{}'.format(rev_data))
        except Exception as e:
            Utils.error('客户端与服务端建立连接并开启接收消息状态失败，失败原因为：{}'.format(e))
            client_socket.close()

    @classmethod
    def client_send_message_once(cls, client_socket: socket, message: bytes):
        try:
            TcpFunctionGroup.send_message(sock=client_socket, message=message)
        except Exception as e:
            Utils.error('客户端向服务端发送消息失败，失败原因为：{}'.format(e))
            client_socket.close()

    @classmethod
    def client_send_meaasge_forever(cls, client_socket, message: bytes, interval: float = 0.1):
        try:
            while True:
                time.sleep(interval)
                send_result = TcpFunctionGroup.send_message(sock=client_socket, message=message)
                if send_result is True:
                    continue
                else:
                    break
        except Exception as e:
            Utils.error('客户端向服务端发送消息失败，失败原因为：{}'.format(e))
            client_socket.close()

    @classmethod
    def send_message(cls, sock: socket.socket, message: bytes):
        try:
            sock.sendall(message)
            Utils.info(info_string='消息发送成功！')
            return True
        except Exception as e:
            Utils.error(error_string='消息发送失败，失败原因为：{}'.format(e))
            return False

    @classmethod
    def recive_message(cls, sock: socket.socket, buffer_size: int = 8192):
        try:
            Utils.info(info_string='消息接收成功！')
            return sock.recv(buffer_size)
        except Exception as e:
            Utils.error(error_string='消息接收失败，失败原因为：{}'.format(e))
            return False

    @classmethod
    def cycle_data_body(
            cls, cycle_number_and_unit_data: list, determine_data_string_length_enable: bool = True
    ) -> Union[list, None]:
        # 要求列表为二维的，每个数据单元的第一个值为c语言struct的字段类型
        # FIXME 20200917 将传入两个列表改成了一个
        if determine_data_string_length_enable is True:
            try:
                end_result = []
                data_type = cycle_number_and_unit_data[0]
                data_body = [cycle_number_and_unit_data[1]]
                if cycle_number_and_unit_data[1] == len(cycle_number_and_unit_data[2]):
                    for i in range(len(cycle_number_and_unit_data[2])):  # TODO 改造的简洁些
                        data_type += cycle_number_and_unit_data[2][i][0]
                        data_body += cycle_number_and_unit_data[2][i][1:]
                    end_result.append(data_type)
                    for j in data_body:
                        end_result.append(j)
                    return end_result
                elif 1 < len(cycle_number_and_unit_data[2]) < cycle_number_and_unit_data[1]:
                    for i in range(len(cycle_number_and_unit_data[2])):
                        data_type += cycle_number_and_unit_data[2][i][0]
                        data_body += cycle_number_and_unit_data[2][i][1:]
                    for j in range(len(cycle_number_and_unit_data[2]), cycle_number_and_unit_data[1]):
                        data_type += cycle_number_and_unit_data[2][0][0]
                        data_body += cycle_number_and_unit_data[2][0][1:]
                    end_result.append(data_type)
                    for j in data_body:
                        end_result.append(j)
                    return end_result
                elif 1 == len(cycle_number_and_unit_data[2]) < cycle_number_and_unit_data[1]:
                    data_type = ''.join(cycle_number_and_unit_data[2][0][0]) * cycle_number_and_unit_data[1]
                    end_result.append(cycle_number_and_unit_data[0] + data_type)
                    i = 0
                    while i < cycle_number_and_unit_data[1]:
                        i += 1
                        data_body += cycle_number_and_unit_data[2][0][1:]
                    for j in data_body:
                        end_result.append(j)
                    return end_result
                else:
                    Utils.error(
                        error_string='循环数量小于提供的数据素材量，请增加循环值！循环要求的值为{}，实际'
                                     '填写的列表长度为{}'.format(cycle_number_and_unit_data[1], len(cycle_number_and_unit_data[2]))
                    )
                    return None
            except Exception as e:
                Utils.error(error_string='循环数据体构造失败，具体原因为：{}'.format(e))
                return None
        else:
            try:
                end_result = []
                data_type = cycle_number_and_unit_data[0]
                data_body = [cycle_number_and_unit_data[1]]
                for i in range(len(cycle_number_and_unit_data[2])):
                    data_type += cycle_number_and_unit_data[2][i][0]
                    data_body += cycle_number_and_unit_data[2][i][1:]
                end_result.append(data_type)
                for j in data_body:
                    end_result.append(j)
                return end_result
            except Exception as e:
                Utils.error(error_string='循环数据体构造失败，具体原因为：{}'.format(e))
                return None

    @classmethod
    def split_multipart_databody(cls, list_value: list):
        global flag
        global multipart_dict
        temp_list = []
        for i in range(0, len(list_value)):
            if isinstance(list_value[i], list) and (list_value[-1] != list_value[i]):
                for j in list_value[i:]:
                    temp_list.append(j)
                multipart_dict[flag] = temp_list
                flag += 1
                return TcpFunctionGroup.split_multipart_databody(list_value[i])
            elif isinstance(list_value[i], list) and (list_value[-1] == list_value[i]):
                temp_list.append(list_value[i])
                multipart_dict[flag] = temp_list
                flag += 1
                return TcpFunctionGroup.split_multipart_databody(list_value[i])
            else:
                temp_list.append(list_value[i])
        multipart_dict[flag] = temp_list

    @classmethod
    def receive_message_parse(cls, thread, message):
        # TODO
        pass


if __name__ == '__main__':
    # test server
    # a = 'a'
    # b = 'b'
    # print(a + b)
    tcpfun_1 = TcpFunctionGroup()
    # server = tcpfun_1.created_server_base_ipv4(host='127.0.0.1', port=60003)
    # tcpfun_1.server_connection_single(server_socket=server)
    # time.sleep(20)
    # print(1)
    # tcpfun_1.send_message(sock=server,message=b'\x01\x02\x03')
    # server.close()
    # print(1)
    # tcpfun_1.server_receive_forever(server_socket=server)
    # test client
    # tcpfun_1 = TcpFunctionGroup()
    # client = tcpfun_1.created_client_base_ipv4(host='127.0.0.1', port=60020)
    # tcpfun_1.client_connection_forever(client_socket=client)
    # print(tcpfun_1.cstruct_to_byte(
    #     cstruct_list=[
    #         ['<H', 32382], ['<H', 1], ['<H', 15], ['<H', 4097],
    #         ['<H', 256], ['<H', 2], ['<H', 2], ['<B', 10], ['<B', 15],
    #         ['<H', 3], ['<H', 1], ['<H', 0], ['<H', 2573]
    #     ]
    # )
    # )
    # a_1 = tcpfun_1.cycle_data_body(
    #     cycle_number=3,
    #     unit_data=[
    #         ['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
    #         ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
    #         ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]
    #     ],
    #     determine_data_string_length_enable=True
    # )
    # print(a_1)
    a_2 = tcpfun_1.cycle_data_body(
        cycle_number_and_unit_data=
        ['a', 4,
            [['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
            ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
            ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]]
        ],
        determine_data_string_length_enable=True
    )
    print(a_2)
    a_3 = tcpfun_1.cycle_data_body(
        cycle_number_and_unit_data=
        ['a', 3,
            [['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
            ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
            ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]]
        ],
        determine_data_string_length_enable=True
    )
    print(a_3)
    a_4 = tcpfun_1.cycle_data_body(
        cycle_number_and_unit_data=['a', 3, [['ABCDEFG', 0, 1, 2, 3, 4, 5, 6]]],
        determine_data_string_length_enable=True
    )
    print(a_4)
    a_5 = tcpfun_1.cycle_data_body(
        cycle_number_and_unit_data=['a', 3, [['ABCDEFG', 0, 1, 2, 3, 4, 5, 6]]],
        determine_data_string_length_enable=False
    )
    print(a_5)
    # a_4 = tcpfun_1.cycle_data_body(
    #     cycle_number=3,
    #     unit_data=[
    #         ['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
    #         ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
    #         ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]
    #     ],
    #     determine_data_string_length_enable=False
    # )
    # print(a_4)
    # a_5 = tcpfun_1.cycle_data_body(
    #     cycle_number=5,
    #     unit_data=[
    #         ['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
    #         ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
    #         ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]
    #     ],
    #     determine_data_string_length_enable=False
    # )
    # print(a_5)
    # a_6 = tcpfun_1.cycle_data_body(
    #     cycle_number=2,
    #     unit_data=[
    #         ['ABCDEFG', 0, 1, 2, 3, 4, 5, 6],
    #         ['HIJKLMN', 7, 8, 9, 10, 11, 12, 13],
    #         ['OPQRSTUV', 14, 15, 16, 17, 18, 19, 20, 21]
    #     ],
    #     determine_data_string_length_enable=False
    # )
    # print(a_6)

    # bytes_value = tcpfun_1.cstruct_to_bytes(
    #     cstruct_list=[
    #         ['<H', 32382], ['<H', 1], ['<H', 15], ['<H', 4097],
    #         ['<H', 256], ['<H', 2], ['<H', 2], ['<B', 10], ['<B', 15],
    #         ['<H', 3], ['<H', 1], ['<H', 0], ['<H', 2573]
    #     ]
    # )
    # print('***********************')
    # print(struct.pack('<HHHHHHHBBHHHH', 32382, 1, 15, 4097, 256, 2, 2, 10, 15, 3, 1, 0, 2573))
    # print('************************')
    # bytes_value = tcpfun_1.cstruct_to_bytes(
    #     cstruct_list=[
    #         ['<HHHHHHHBBHHHH', 32382, 1, 15, 4097, 256, 2, 2, 10, 15, 3, 1, 0, 2573]
    #     ]
    # # )
    # print(bytes_value)
    # print(tcpfun_1.bytes_to_cstruct(cstruct_format_stream='<HHHHHHHBBHHHH', bytes_value=bytes_value))
    # client = tcpfun_1.created_client_base_ipv4(host='127.0.0.1', port=60020)
    # tcpfun_1.client_send_message_once(client_socket=client, message=tcpfun_1.cstruct_to_bytes(
    #     cstruct_list=[
    #         ['<H', 32382], ['<H', 1], ['<H', 15], ['<H', 4097],
    #         ['<H', 256], ['<H', 2], ['<H', 2], ['<B', 10], ['<B', 15],
    #         ['<H', 3], ['<H', 1], ['<H', 0], ['<H', 2573]
    #     ]
    # )
    # )
    # tcpfun_1.close_client_base_ipv4(client_socket=client)