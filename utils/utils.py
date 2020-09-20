"""

"""
import logging
import os
import time
import win32api
import win32con
from tkinter import *


class Utils:
    def __init__(self):
        self.top = Tk()
        self.flag = ''

    @classmethod
    def root_path(cls):
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    @classmethod
    def join_path(cls, *args):
        goal_path = ''
        for i in (0, (len(args) - 1)):
            goal_path = os.path.join(goal_path, args[i])
        return goal_path

    @classmethod
    def time_stamp(cls):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def info(cls, info_string: str):
        logging.basicConfig(level=logging.INFO)
        logging.info(info_string)

    @classmethod
    def debug(cls, debug_string: str):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(debug_string)

    @classmethod
    def error(cls, error_string: str):
        logging.basicConfig(level=logging.ERROR)
        logging.error(error_string)

    def pass_or_fail_window(self):  # TODO 1、窗体居中；2、捕获被点击的按钮，作为测试用例的断言。
        self.top.geometry('500x100')
        self.top.title('用例执行结果判别')
        Label(self.top, text='请给出本条测试用例的执行结果！').pack(fill=Y, expand=1)
        pass_button = Button(
            self.top, text='通过', command=self.pass_command,
            bg='green', fg='black', width=30, height=10
        ).pack(side=LEFT)
        fail_button = Button(
            self.top, text='未通过', command=self.fail_command,
            bg='red', fg='black', width=30, height=10
        ).pack(side=RIGHT)
        mainloop()
        if self.flag is True:
            return True
        else:
            return False  # TODO 在提示窗体里添加一个文本框，文本框内容为失败用例的实测结果

    def pass_command(self):
        self.top.quit()
        self.flag = True

    def fail_command(self):
        self.top.quit()
        self.flag = False


if __name__ == '__main__':
    uu = Utils()
    print(uu.time_stamp())
    print(uu.pass_or_fail_window())