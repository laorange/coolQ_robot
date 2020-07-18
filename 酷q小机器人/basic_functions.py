# basic_functions.py

import os


def make_dir(path_name):  # os.mkdir("./输出文件")
    try:
        os.mkdir(path_name)
    except FileExistsError:
        pass


def read_file2list(path_name):
    with open(path_name, encoding='UTF-8') as source_text:
        lines_ls = source_text.readlines()
        for i in range(len(lines_ls)):
            lines_ls[i] = lines_ls[i].strip()
    return lines_ls

