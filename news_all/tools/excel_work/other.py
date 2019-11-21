# -*- coding: utf-8 -*-
# @File    : other.py
import os


def read_excel_folder(folder_path):
    """读取文件excel文件夹，返回excel文件绝对路径列表"""
    file_name_list = os.listdir(folder_path)

    path_list = []
    for file_name in file_name_list:
        if len(file_name) < 5:
            continue
        if file_name[:2] == '~$':  # 防止excel打开创建的临时文件混进来
            continue
        if os.path.splitext(file_name)[1] not in ('.xls', '.xlsx'):
            continue
        path_list.append(os.path.join(folder_path, file_name))
    return path_list





