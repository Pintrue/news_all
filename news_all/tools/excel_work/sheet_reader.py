# -*- coding: utf-8 -*-

# @File    : sheet_reader.py


import xlrd

"""
SheetReader
适用于对excel读取的多种情况
1.普通的有表头的excel表
2.同excel不同sheet的情况,创建多个SheetReader子类对应不同的sheet格式
3.没有表头的情况,设置has_header=False从第1行开始读
"""


class SheetReader(object):
    """
    读取excel文件的1个Sheet
    返回
    类似DictCursor获取的dict_list数据,
    或tuple_list
    或单列的数据list

    * 只取1个sheet
    * 有表头从第2行读，没有表头从第一行读
    可指定ExcelColumnMap处理表格中文字段,转换为英文字段,如： {'知识点ID':'know_id'}
    可指定DataType处理数据类型方法,如： {'know_id':int,'know_name':lambda x:x.split()},
    可以指定是否添加自增序号，参数：auto_increment_num为True时，每条数据会添加{'auto_increment_num':序号}
    """
    ExcelColumnMap = {}
    DataType = {}

    def __init__(self, file_path, sheet_num=1, has_header=True, auto_increment_num=False, begin_index=None):
        """
        :param file_path:           str     文件绝对路径
        :param sheet_num:           int     sheet序号,从1开始
        :param has_header:          bool    是否有表头
        :param auto_increment_num:  bool    是否在dict_list添加自增数字字段,auto_increment_num
        :param begin_index          int    从第几行开始读
        """
        self.file_path = file_path
        self.sheet_num = sheet_num
        self.has_header = has_header
        self.auto_increment_num = auto_increment_num
        self.sheet = None

        if begin_index:  # 根据设定begin_index
            self.begin_index = self.begin_index
        else:
            #  没有设定begin_index 如果has_header=True，有表头，从第2行开始读,否则从第一行开始读
            if self.has_header:
                self.begin_index = 1
            else:
                self.begin_index = 0

        # 读取sheet
        self.sheet = self.read_excel_sheet()

    def dict_list(self, begin_index=None):
        """读取和处理表格数据,返回表头和数据组成的字典组成的列表"""
        if not self.has_header:
            raise Exception('没有表头,不能返回dict_list')
        bi = begin_index if isinstance(begin_index, int) else self.begin_index
        order_column_dict = self.handle_headers()  # 表头顺序字典 {0:'id',1:'question',...}

        d_l = []
        for i in range(bi, self.sheet.nrows):
            row_tuple = self.sheet.row_values(i)
            row_dict = {column: self.change_type(column, row_tuple[order])
                        for order, column in order_column_dict.items()}
            if self.auto_increment_num:
                # 表格内数据自增序号
                row_dict['auto_increment_num'] = i
            self.deal_data(row_dict)  # 处理每行数据中间键
            d_l.append(row_dict)
        return d_l

    def tuple_list(self, begin_index=None):
        """返回tuple_list"""
        bi = begin_index if isinstance(begin_index, int) else self.begin_index

        t_l = []
        for i in range(bi, self.sheet.nrows):
            row_tuple = self.sheet.row_values(i)
            t_l.append(tuple(row_tuple))
        return t_l

    def single_list(self, column_num=1):
        """
        单列数据，直接返回列表
        :param column_num:      int     指定列，从1开始
        """
        begin_index = 1

        # 如果has_header=True，没有表头，从第2行开始读,否则从第一行开始读
        if not self.has_header:
            begin_index = 0
        s_l = []
        for i in range(begin_index, self.sheet.nrows):
            row_tuple = self.sheet.row_values(i)
            s_l.append(row_tuple[column_num - 1])
        return s_l

    def read_excel_sheet(self):
        """读取excel的sheet"""
        try:
            print('=====', self.file_path, '=====')
            xls_obj = xlrd.open_workbook(self.file_path)
        except FileNotFoundError:
            raise FileNotFoundError('没有找到文件:%s' % self.file_path)
        return xls_obj.sheet_by_index(self.sheet_num - 1)

    def handle_headers(self):
        """处理表头"""
        headers = self.sheet.row_values(0)
        try:
            # 根据表格列的顺序，将字段名称匹配到设置好的名称
            # 如果ExcelColumnMap没有指定，否则使用原表头名
            change_c_name = lambda x: self.ExcelColumnMap[x] if self.ExcelColumnMap.get(x, None) else x

            return {h[0]: change_c_name(h[1]) for h in enumerate(headers)}
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

    def deal_data(self, row_dict):
        """处理数据到自己想要的格式,只能处理dict_list的数据"""
        pass

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
