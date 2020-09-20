# -*- coding: utf-8 -*-
# author: edward
# date: 2020-8-29
# contact: ouchen1989@tom.com


"""

"""
from typing import Union
import struct
from utils.utils import Utils


class Common:
    def __init__(self):
        pass

    @classmethod
    def string_to_bytes(cls, str_value: str, encode_mode: str = 'utf-8') -> Union[bytes, None]:
        """
        字符串转字节码，不是转成16进制数哦！
        :param str_value: 字符串值
        :param encode_mode: 字符串的编码格式，默认是utf-8
        :return: 成功时返回字符串对应的字节码，失败时提示
        """
        try:
            return str_value.encode(encode_mode)
        except BaseException as e:
            Utils.error(error_string='字符串为字节码失败，系统错误提示为{}'.format(e))
            return None

    @classmethod
    def bytes_to_string(cls, bytes_value: bytes, encode_mode: str = 'utf-8') -> Union[str, None]:
        try:
            return bytes_value.decode(encode_mode)
        except BaseException as e:
            Utils.error(error_string='字节码转为字符串失败，系统错误提示为{}'.format(e))
            return None



if __name__ == '__main__':
    hex_string = '编程'
    print(hex_string.encode('utf-8'))
    byte_value = b'Python3\xe7\xbc\x96\xe7\xa8\x8b'
    common = Common()

    common.cycle_data_body(cycle_number=5, )
    # string_value = '编程'
    # com_f = CommonFunction()
    # print('字符串"{}"转字节码为"{}"'.format(string_value, com_f.string_to_bytes(string_value)))
    # print('字节码"{}"转为字符串"{}"'.format(byte_value, com_f.bytes_to_string(byte_value)))
    # hex_value = 0xff
    # print('16进制数"{}"转字节码为"{}"'.format(hex_value, com_f.hex_to_bytes(hex_value=hex_value, format_code='>i')))