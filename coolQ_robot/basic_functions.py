# basic_functions.py

import os


def make_dir(path_name):  # os.mkdir("./输出文件")
    try:
        os.mkdir(path_name)
    except FileExistsError:
        pass


def read_file2list(path_name):  #, encoding='UTF-8'
    try:
        with open(path_name) as source_text:   #, encoding=encoding
            lines_ls = source_text.readlines()
            for i in range(len(lines_ls)):
                lines_ls[i] = lines_ls[i].strip()
        return lines_ls
    except:
        with open(path_name, encoding='ANSI') as source_text:
            lines_ls = source_text.readlines()
            for i in range(len(lines_ls)):
                lines_ls[i] = lines_ls[i].strip()
        print('UNICODE_ERROR')
        return lines_ls

