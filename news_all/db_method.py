#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 10:04
# @Author  : wjq
# @File    : db_method.py


from pymongo import ReturnDocument
from news_all.tools.database_work import MongoBaseRW
from news_all.tools.database_work.db_config import DatabaseConfig


class NewsW(MongoBaseRW):
    db_config = DatabaseConfig.News


class DebugRW(MongoBaseRW):
    """统计数据读写库"""
    db_config = DatabaseConfig.Debug


class SourceR(MongoBaseRW):
    """
     "sourceMeta": {"category_third": ,
                "site_weight": ,
                "content_quality": ,
                "start_url": [,],
                "priority": ,
                "mode":,
                "category_first": ,
                "time_limitation": ,
                "category_second":  ,
                "remove_duplicate": ,
                "media_type": ,
                "content_source": ,
                "rmw_copyright":,
                "sourceType": ,
                "name": ,
                "direct_linkto": ,
                "categories": ,
                "addr": },
    已有媒体类型（media_type）、
        媒体数据（content_source）、

    9月20日增加 暂不上线
    媒体分类（media_category）、
    媒体属性（media_attribute）、
    地域属性：省（province）
    市（city）
    """
    db_config = DatabaseConfig.Source
    source_map = {"source_id": "source_id",
                  "start_url": "url",
                  "site_weight": "site_weight",
                  "content_quality": "content_quality",
                  "priority": "priority",
                  "mode": "mode",
                  "category_first": "category_first",
                  "category_second": "category_second",
                  "category_third": "category_third",
                  "time_limitation": "time_limitation",
                  "remove_duplicate": "remove_duplicate",
                  "media_type": "media_type",
                  "content_source": "content_source",
                  "media_category": "media_category",
                  "media_attribute": "media_attribute",
                  "province": "province",
                  "city": "city",
                  "rmw_copyright": "rmw_copyright",
                  "sourceType": "source_type",
                  "name": "name",
                  "direct_linkto": "direct_link_to",
                  # 数据源管理系统mongo表里没有direct_link_to字段, ETL也没处理direct_linkto字段,
                  # 如果这个字段传空字符导致报错的是imagestore报错, 入imagestore才入库统计
                  "categories": "categories",
                  "addr": "addr",
                  "exempt_review": "exempt_review",  # 增加免审字段
                  "save_audit_database": "save_audit_database"}  # 1入审核库, 0不入审核库, 默认1

    def get_source_meta(self, **kwargs):
        # kwargs.update({"enabled": 1})  # 7月2日修改 爬虫开启1 关闭0  7月29日上线调度版本就不用根据"enabled": 1
        res = self.find_one(kwargs)
        if not res:
            return

        for _, j in self.source_map.items():
            if isinstance(res.get(j), float):
                res[j] = int(res[j])

        categories = res.get('categories', [])
        print(categories)
        for i, j in enumerate(categories):
            categories[i] = int(j)
        # 在从source表获取name时就清洗name, 以前打标有"长城网-新闻热播榜-左侧列表",  "长城网 长城网"
        res['name'] = res['name'].split()[0].split('-')[0]
        return {i: res.get(j) for i, j in self.source_map.items()}  # 允许null但不允许空字符串 不能用get(j, "")

    def update_spider_name(self, source_id, spider_name):
        """
        :param source_id:
        :param spider_name:
        :return:
        db.source.findOneAndUpdate(
   {source_id: 168},
   {'$set': {'spider_name': 'xinhuanet'}}
   )
        """
        self.coll.find_one_and_update({'source_id': source_id}, {'$set': {'spider_name': spider_name}},
                                      return_document=ReturnDocument.AFTER)
