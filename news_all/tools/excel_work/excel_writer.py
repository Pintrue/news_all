# -*- coding: utf-8 -*-
# @File    : excel_writer.py

import xlwt
import os


class ExcelWriter(object):
    """
    读取excel文件,dict_list数据写到表中
    只写Sheet1，有表头
    可指定ExcelHeadMap将字段名改为中文,如： {'know_id':'知识点ID'}
    * 需要保存为xls的后缀名
    """
    ExcelHeadMap = {}

    def write(self, data, save_path):
        if not data:
            print('not data')
            return
        self.check_xls(save_path)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet1')

        headers = self.handle_headers(data)
        self.__write_row(ws, 0, headers)
        for i in range(len(data)):
            self.__write_row(ws, i + 1, list(data[i].values()))
        wb.save(save_path)

    def handle_headers(self, data):
        """处理表头"""
        headers = list(data[0].keys())
        try:
            # ExcelHeadMap，使用指定霍城，或使用data里的key
            change_h_name = lambda x: self.ExcelHeadMap[x] if self.ExcelHeadMap.get(x, None) else x
            return [change_h_name(h) for h in headers]
        except IndexError:
            raise Exception('表头处理有误')

    @staticmethod
    def __write_row(ws, r, r_data):
        """
        写入一行
        :param ws:      obj         Worksheet
        :param r:       int         行号
        :param r_data:  list        行内容
        """
        for i in range(len(r_data)):
            ws.write(r, i, r_data[i])

    @staticmethod
    def check_xls(save_path):
        """检查.xls后缀名"""
        t = os.path.splitext(save_path)
        if t[1] != '.xls':
            raise Exception('需要保存为xls格式的文件名')
