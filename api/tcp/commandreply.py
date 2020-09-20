# -*- coding: utf-8 -*-
# author: edward
# date: 2020-8-29
# contact: ouchen1989@tom.com
import os
import sys
import struct
import socket
from common.common import Common
from protolcol.tcp.tcpfunctiongroup import TcpFunctionGroup
from utils.utils import Utils


class CommandReply:
    def __init__(self, ):
        self.utils = Utils()

    def send_command_reply(
            self, client: socket.socket, start_code: int, source_id: int, destination_id: int,
            command_number: int, command_code: int, version_number: int, attribute_code: int, message_number: int,
            package_total_list: list, data_body_list: list, check_code: int, end_code: int
    ):
        try:
            data_body = TcpFunctionGroup.cycle_data_body(
                cycle_number=package_total_list,
                unit_data=data_body_list
            )
            fmt_value = '<HHHHHHHBB' + data_body[0] + 'HH'
            args_value = [start_code, struct.calcsize(fmt_value), source_id, destination_id,
                          command_number, command_code, version_number, attribute_code,
                          message_number] + data_body[1:] + [check_code, end_code]
            print('*************************************')
            print(fmt_value, struct.calcsize(fmt_value), args_value)
            print('*************************************')
            TcpFunctionGroup.client_send_message_once(
                client_socket=client,
                message=struct.pack(fmt_value, *args_value)
            )
            return self.utils.pass_or_fail_window()
        except Exception as e:
            Utils.error(error_string='组装并发送命令响应报文失败，失败原因为：{}'.format(e))
            return None


if __name__ == '__main__':
    pass
    # comm = CommandReply()
    # tcpfun = TcpFunctionGroup()
    # client = tcpfun.created_client_base_ipv4(host='127.0.0.1', port=60020)
    # # <HHHHHHHBBHHHHHHHHH 34 [32382, 34, 15, 4097, 256, 2, 2, 10, 15, 3, 1, 2, 3, 4, 5, 6, 0, 2573]
    # comm.send_command_reply(
    #     client=client,
    #     start_code=32382,
    #     source_id=15,
    #     destination_id=4097,
    #     command_number=256,
    #     command_code=2,
    #     version_number=2,
    #     attribute_code=10,
    #     message_number=15,
    #     package_total_list=['H', 3],
    #     # data_body_list=[['HH', 1, 2], ['HH', 3, 4], ['HH', 5, 6]],
    #     data_body_list=[['HH', 1, 2], ['HH', 3, 4], ['HH', 5, 6]],
    #     check_code=0,
    #     end_code=2573)
    # client.close()
    # print(struct.pack('<6H', 1, 2, 3, 4, 5, 6))
    # if isinstance(list_b[i], str) and isinstance(list_b[i + 1], int) and isinstance(list_b[i + 2], list):
    # print(list_b[i], list_b[i + 1], list_b[i + 2])