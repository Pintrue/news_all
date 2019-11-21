# -*- coding: utf-8 -*-
# @File    : db_method.py

import xlrd


class ExcelReader(object):
    """
    读取excel文件,转换为类似DictCursor获取的dict_list数据
    * 只取sheet1
    * 必须有表头
    可指定ExcelColumnMap处理表格中文字段,如： {'知识点ID':'know_id'}
    可指定DataType处理数据类型,如： {'know_id':int}
    可以指定是否添加自增序号，参数：auto_increment_num为True时，每条数据会添加{'auto_increment_num':序号}
    """
    ExcelColumnMap = {}
    DataType = {}

    def __init__(self, file_path, need_dict=True, auto_increment_num=False):
        """
        need_dict:            是否将各字段及其值组成字典形式
        """
        print(file_path)
        self.sheet = self.read_excel(file_path)
        self.order_columns = self.handle_headers()
        self.auto_increment_num = auto_increment_num
        if need_dict:
            self.data_list = self.read_rows_return_dict()
        else:
            self.data_list = self.read_rows_return_list()

    @staticmethod
    def read_excel(filepath):
        try:
            print('=====', filepath, '=====')
            xls_obj = xlrd.open_workbook(filepath)
        except FileNotFoundError:
            raise FileNotFoundError('没有找到文件:%s' % filepath)
        return xls_obj.sheet_by_index(0)

    def handle_headers(self):
        """处理表头"""
        self.headers = self.sheet.row_values(0)
        try:
            # 根据表格列的顺序，将字段名称匹配到设置好的名称
            # 如果ExcelColumnMap没有指定，否则使用原表头名
            change_c_name = lambda x: self.ExcelColumnMap[x] if self.ExcelColumnMap.get(x, None) else x
            return {h[0]: change_c_name(h[1]) for h in enumerate(self.headers)}
        except IndexError:
            raise Exception('表格字段设置有误')

    def read_rows_return_list(self):
        """
        读取表格数据并返回数据列表,列表有两个元素
        [当前行数, 当前行数据组成的列表]
        """
        for i in range(1, self.sheet.nrows):
            row_tuple = self.sheet.row_values(i)
            yield [i, list(row_tuple)]

    def read_rows_return_dict(self):
        """读取和处理表格数据,返回表头和数据组成的字典组成的列表"""
        data_list = []
        for i in range(1, self.sheet.nrows):
            row_tuple = self.sheet.row_values(i)
            row_dict = {column: self.change_type(column, row_tuple[order])
                        for order, column in self.order_columns.items()}
            if self.auto_increment_num:
                # 表格内数据自增序号
                row_dict['auto_increment_num'] = i
            row_dict = self.deal_data(row_dict, row_num=i)
            data_list.append(row_dict)
        return data_list

    def deal_data(self, row_dict, row_num=0):
        """处理数据到自己想要的格式"""
        return row_dict

    def change_type(self, column, value):
        """转换数据类型"""
        type_fn = self.DataType.get(column, None)
        # 如果DataType没有指定就使用原数据类型
        if not type_fn:
            return value
        try:
            return type_fn(value)
        except ValueError:
            return None


