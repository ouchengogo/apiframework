# -*- coding: utf-8 -*-


"""

"""
import pytest
import allure
import os
import sys
from protolcol.tcp.tcpfunctiongroup import TcpFunctionGroup
from api.tcp.commandreply import CommandReply


@allure.feature('命令响应报文[0181]接口测试')
class TestCommandReply:
    _host = '127.0.0.1'
    _port = 60020

    def setup(self):
        self.client = TcpFunctionGroup.created_client_base_ipv4(host=self._host, port=self._port)
        self.commandreply = CommandReply()

    @allure.story('测试命令响应报文[0181]参数均为正常值情况')
    @allure.title('命令响应报文[0181]所有参数为正常值，具体为：{start_code}{data_length}')
    @pytest.mark.parametrize(
        'start_code, data_length, source_id, destination_id, command_number,'
        'command_code, version_number, attribute_code, message_number, package_type_and_total,'
        'unit_type_and_data, check_code, end_code', [
            (
                    32382, 1, 15, 4097, 256, 2, 2, 10, 15, ['H', 3], [['HH', 2, 1]], 0, 2573
            )
        ])
    def testcase_1(
            self, start_code, data_length, source_id, destination_id, command_number, command_code,
            version_number, attribute_code, message_number, package_type_and_total, unit_type_and_data,
            check_code, end_code
    ):
        result = self.commandreply.command_reply(
            client=self.client, start_code=start_code, data_length=data_length, source_id=source_id,
            destination_id=destination_id, command_number=command_number, command_code=command_code,
            version_number=version_number, attribute_code=attribute_code, message_number=message_number,
            package_type_and_total=package_type_and_total, unit_type_and_data=unit_type_and_data,
            check_code=check_code, end_code=end_code
        )
        assert result is True

    def teardown(self):
        TcpFunctionGroup.close_client_base_ipv4(client_socket=self.client)


if __name__ == '__main__':
    import sys
    import os
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    print(sys.path)