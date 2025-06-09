import os
import pandas as pd
import json
from typing import Any
from .util.all_path import file_operation_path
if not os.path.exists(file_operation_path):
    os.makedirs(file_operation_path)

class Common_file:

    def __init__(self, file_name: str, mode: str, file_dir: str):
        """

        :param file_name: 需要打开的文件名称。目前支持txt,json
        :param mode: 模式为写入模式，即 mode='w'
        :param file_dir: 文件路径
        """
        file_dir = file_dir[:file_dir.rfind('\\')]
        if mode == 'w':
            print('警告：使用写入模式会清除原文件所有内容！')
            input('请输入任意字符继续：')
        if mode == 'r':
            if os.path.isabs(file_name) is False:
                if os.path.exists(os.path.join(file_operation_path, file_name)):
                    self.file_name = os.path.join(file_operation_path, file_name)
                elif os.path.exists(os.path.join(file_dir, file_name)):
                    self.file_name = os.path.join(file_dir, file_name)
                else:
                    print(f'找不到文件{os.path.join(file_dir, file_name)}')
                    exit()
            else:
                self.file_name = file_name
        elif mode in ['w', 'a']:
            if os.path.isabs(file_name) is False:
                self.file_name = os.path.join(file_dir, file_name)
            else:
                self.file_name = file_name
        self.file = open(self.file_name, mode, encoding='utf-8')

    def close(self):
        """
        关闭文件
        :return:
        """
        self.file.close()
        print(' \n文件已关闭')

    def read_all(self):
        """
        获取文件中所有内容
        :return: 返回文件中的所有内容
        """
        return self.file.read()

    def read_a_line(self):
        """
        获取文件当前行的内容
        :return: 返回文件中当前行的内容
        """
        return self.file.readline()

    def read_random_line(self, num: int):
        """
        返回文件中第某行的内容
        :param num: 选择的第几行，数据类型：int
        :return: 返回第num行全部内容
        """
        num = num - 1
        all_line = self.file.readlines()
        return all_line[num]

    def tell(self):
        """
        返回文件中当前读取位置
        :return:返回文件中当前读取位置
        """
        return self.file.tell()

    def seek(self):
        """
        文件（f）回到初始读取位置
        :return:
        """
        self.file.seek(0)

    def write(self, message: str):
        """
        向文件（f）写入内容（message）
        :param message: 向文件写入的内容
        :return:
        """
        self.file.write(message)

    def write_lines(self, lines: list):
        """
        向文件（f）写入序列（line）
        :param lines: 向文件写入的序列
        :return:
        """
        self.file.writelines(lines)

class Json(Common_file):
    """
    初始化json文件类用于处理json文件
    """

    def load(self):
        """
        加载json文件
        Returns:

        """
        return json.load(self.file)

    def dump(self, message: str):
        """
        向json文件（f）中写入内容（message）
        Args:
            message:

        Returns:

        """
        json.dump(message, self.file)

class CSV:
    """
    赋值（f）为csv文件（example.csv)
    """

    def __init__(self, file_name: str, file_dir: str, mode: str='r'):
        """

        :param file_name: csv文件的名称，通常放置在 ../resources/assets/class/file_operation/内
        :param file_dir: 文件路径
        """
        file_dir = file_dir[:file_dir.rfind('\\')]
        if mode == 'r':
            if os.path.isabs(file_name) is False:
                if os.path.exists(os.path.join(file_operation_path, file_name)):
                    self.file_name = os.path.join(file_operation_path, file_name)
                elif os.path.exists(os.path.join(file_dir, file_name)):
                    self.file_name = os.path.join(file_dir, file_name)
                else:
                    print(f'找不到文件{file_name}')
            else:
                self.file_name = file_name
        elif mode == 'w':
            if os.path.isabs(file_name) is False:
                self.file_name = os.path.join(file_dir, file_name)
            else:
                self.file_name = file_name
        self.csv = pd.read_csv(self.file_name, encoding='utf-8')
        self.shape = self.csv.shape()

    def print_head(self, head: int):
        """
        打印csv文件（f）中前（数字head，默认5）行
        :param head: 打开文件中前面的行数，默认为5行。数据类型：int
        :return:
        """
        print(self.csv.head(head))

    def print_tail(self, tail: int):
        """
        打印csv文件（f）中后（数字tail，默认5）行
        :param tail: 打开文件中后面的行数，默认为5行。数据类型：int
        :return:
        """
        print(self.csv.tail(tail))

    def print_describe(self):
        """
        打印csv文件（f）中的汇总统计
        :return:
        """
        print(self.csv.describe())

    def get_a_row(self, row: int):
        """
        获取csv文件（f）中第（数字row，默认1，下同）行
        :param row: 想要获取行的行数。数据类型：int
        :return:
        """
        row = row - 1
        return self.csv.iloc[row, :]

    def get_a_column(self, column: int):
        """
        csv文件（f）中第（数字column）列
        :param column: 想要获取列的列数。数据类型：int
        :return:
        """
        column = column - 1
        return self.csv.iloc[:, column]

    def get_directory(self, row: int, column: int):
        """
        csv文件（f）中第（数字row）行、第（数字column）列的元素
        :param row: 第几行。数据类型：int
        :param column: 第几列。数据类型：int
        :return: 返回该行该列的元素
        """
        row = row - 1
        column = column - 1
        return self.csv.iloc[row, column]

    def dropna(self):
        """
        删除csv文件（f）中的所有空白值
        :return:
        """
        self.csv.dropna()

    def fillna(self, x: Any):
        """
        用（x）替换csv文件（f）中的所有空白值
        :param x: 用x来替代csv中所有的空白值
        :return:
        """
        self.csv.fillna(x)