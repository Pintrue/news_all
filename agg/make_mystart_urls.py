#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 15:37
# @Author  : wjq
# @File    : make_mystart_urls.py


from news_all.tools.excel_work.sheet_reader import SheetReader


class MyReader(SheetReader):
    # 表头start_url	title	link_text	depth	parent_url	parent_text		source_id
    ExcelColumnMap = {}
    DataType = {'depth': int, 'source_id': int}


def get_mystart_urls(sheet_num, begin_index=None):
    file = '全站采集网站栏目.xlsx'
    dl = MyReader(file_path=file, sheet_num=sheet_num, has_header=True, auto_increment_num=True).dict_list(
        begin_index=begin_index)

    su = ''
    for i in dl:
        if not i['start_url']:
            continue
        su += "'{surl}':{sid},  # {name}\n".format(surl=i['start_url'], sid=i['source_id'], name=i['title'])

    print(su)


if __name__ == '__main__':
    get_mystart_urls(2)  # 起始页是第1页
