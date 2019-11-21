# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class GwyAllSpider(NewsRCSpider):
    """国务院"""
    name = 'gwy_all'
    mystart_urls = {

        'https://app.www.gov.cn/govdata/gov/columns/column_472_0.json': 1301923,   #  国务院 总理
        'https://app.www.gov.cn/govdata/gov/columns/column_475_0.json': 1301929,   #  国务院-地方
        'https://app.www.gov.cn/govdata/gov/columns/column_473_0.json': 1301924,   #  国务院-政策
        'https://app.www.gov.cn/govdata/gov/columns/column_510_0.json': 1301927,   #  国务院-数据
        'https://app.www.gov.cn/govdata/gov/columns/column_476_0.json': 1301926,   #  国务院-服务
        'https://app.www.gov.cn/govdata/gov/home.json': 1301922,   #  国务院-要闻
        'https://app.www.gov.cn/govdata/gov/columns/column_478_0.json': 1301928,   #  国务院-访谈
        'https://app.www.gov.cn/govdata/gov/columns/column_474_0.json': 1301925,   #  国务院-部门
    }

    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('articles')
        try:
            if result is None:
                sections = rj.get('sections')
                for value in sections.items():
                    item = value[1]
                    recommends = item['recommends']
                    lists = list(recommends.values())
                    for j in lists:
                        article = j.get("article")
                        title = article.get("title")
                        url = article.get("shareUrl")
                        yield Request(
                            url=url,
                            callback=self.parse_item,
                            meta={'source_id': response.meta['source_id'], 'title': title,
                                  
                                  'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                        )
            if isinstance(result, list):
                for i in result:
                    item = result.get(i)
                    title = item.get("title")
                    url = item.get("shareUrl")
                    yield Request(
                        url=url,
                        callback=self.parse_item,
                        meta={'source_id': response.meta['source_id'], 'title': title,
                              
                              'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                    )
        except:
            return self.produce_debugitem(response, 'json error')

    def parse_item(self, response):
        try:
            content_div = response.xpath('.//article[@id="articleins"]/p').extract()
            source_div = response.xpath('.//p[@class="artlabel artlabellftlne"]')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos,
        )

