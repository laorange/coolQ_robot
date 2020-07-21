# basic_functions.py

import os
import chardet
import pprint


def make_dir(path_name):  # os.mkdir("./输出文件")
    try:
        os.mkdir(path_name)
    except FileExistsError:
        pass


def read_file2list(path_name):  # , encoding='UTF-8'
    result = chardet.detect(open(path_name, "rb").read())

    char_enc = result['encoding']

    try:
        with open(path_name, encoding=char_enc) as source_text:   # , encoding=encoding
            lines_ls = source_text.readlines()
            for i in range(len(lines_ls)):
                lines_ls[i] = lines_ls[i].strip()
    except Exception as e:
        print(e)

    pprint.pprint(lines_ls)

    return lines_ls

