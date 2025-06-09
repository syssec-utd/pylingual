"""
@author: xuepl
@file: excel_tools.py
@date: 2022/09/04 15:58
"""
import os
import xlrd
from tools.config import Config
'\n给定一个excel的相对路径，\n1、使用root_path 和excel的相对路径进行拼接\n2、读取excel所有sheet中的数据，按照顺序，放入一个列表中\n3、每条用用例数据，都是一个字典\n'

def read_excel(file_path):
    root_path = Config().get_root_path()
    file_path = os.path.join(root_path, file_path)
    excel = xlrd.open_workbook(file_path)
    sheets = excel.sheets()
    case_list = []
    ids = []
    for s in sheets:
        rows = s.nrows
        if rows < 3:
            continue
        keys = s.row_values(1)
        for n in range(2, rows):
            row = s.row_values(n)
            case = dict(zip(keys, row))
            if case['is_run'].strip() == '否' or case['title'] == '':
                continue
            ids.append(case['title'])
            case_list.append(case)
    return (ids, case_list)

def scan_excels(file_path):
    excel_files = []
    files = os.listdir(file_path)
    for f in files:
        file = os.path.join(file_path, f)
        if os.path.isdir(file) and f not in ['.pytest_cache', 'venv', '.idea', '.git', '__pycach__']:
            res = scan_excels(file)
            excel_files.extend(res)
        elif os.path.isfile(file) and file.endswith('.xls'):
            excel_files.append(file)
    return excel_files

def get_cases():
    root_path = Config().get_root_path()
    excel_files = scan_excels(root_path)
    ids = []
    cases = []
    for f in excel_files:
        i, cs = read_excel(f)
        ids.extend(i)
        cases.extend(cs)
    return (ids, cases)
if __name__ == '__main__':
    print(read_excel('ceshi.xls'))