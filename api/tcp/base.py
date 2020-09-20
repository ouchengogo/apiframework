# -*- coding: utf-8 -*-
# author: edward
# date: 2020-8-29
# contact: ouchen1989@tom.com


class Base:
    def __init__(self, start_code: int, data_length: int, source_id: int, destination_id: int, command_number: int,
                 command_code: int, version_number: int, attribute_code: int, message_number: int, package_total: int,
                 current_package: int, check_code: int, end_code: int
                 ):
        self.start_code = start_code
        self.data_length = data_length
        self.source_id = source_id
        self.destination_id = destination_id
        self.command_number = command_number
        self.command_code = command_code
        self.version_number = version_number
        self.attribute_code = attribute_code
        self.message_number = message_number
        self.package_total = package_total
        self.current_package = current_package
        self.check_code = check_code
        self.end_code = end_code
        self.headers = ('<HHHHHHHBBHH', self.start_code, self.data_length, self.source_id, self.destination_id,
                        self.command_number, self.command_code, self.version_number, self.attribute_code,
                        self.message_number, self.package_total, self.current_package
                        )
        self.tails = ('HH', self.check_code, self.end_code)
