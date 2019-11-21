# -*- coding:utf-8 -*-

from scrapy import Request
from news_all.spider_models import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.others import get_sub_str_ex
from datetime import datetime


class CeweekVspider(NewsRCSpider):
    """中国经济周刊 视听 视频"""
    name = "ceweekly_video"

    mystart_urls = {"http://video.ceweekly.cn/video/interview/": 3880}

    custom_settings = {
        'DEPTH_LIMIT': 2,  # 若翻页则需要设置深度为0
    }

    # todo 解析嵌入腾讯视频
    # http://video.ceweekly.cn/2019/0830/266656.shtml
    # http://video.ceweekly.cn/2019/0819/264861.shtml
    rules = (
        # http://video.ceweekly.cn/2019/0805/263303.shtml
        Rule(LinkExtractor(allow=(r'video.ceweekly.cn/%s\d{2}/\d+.s?htm') % datetime.today().strftime('%Y/%m'),),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//*[@class='videoshow-title']/text").extract_first('') or \
                    self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[contains(@class, 'date')]/text()").extract()[0]
            origin_name = xp("//div[@class='tv-infor']/*[contains(@class, 'editors')]/text()").extract_first('')
            content_div = xp("//section[@class='tv-cont']/p") or xp(
                "//div[@class='inner']/div[contains(@class,'article-content')]")
            content, media, _, _ = self.content_clean(content_div)
            x_path = '//*[@class="cmstopVideo" and @data-mce-role="cmstopVideo"]/@src'
            api_url = response.xpath(x_path).extract()[0]
        except:
            return self.produce_debugitem(response, 'xpath error')

        return Request(api_url,
                       callback=self.parse_video,
                       meta={'source_id': response.meta['source_id'],
                             'title': title,
                             'pubtime': pubtime,
                             'origin_name': origin_name,
                             'content': content,
                             'media': media,
                             'news_url': response.url,
                             'start_url_time': response.meta.get('start_url_time'),
                             'schedule_time': response.meta.get('schedule_time')}
                       )

    def parse_video(self, response):
        v_url = next(get_sub_str_ex(response.text, '<source src="', '"', False))
        # v_url = v_url.replace("/sd/", "/ed/")
        v_url = v_url.replace("/hd/", "/ed/")
        print(v_url)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content='<div>#{{1}}#</div>' + response.request.meta['content'],
            media=response.request.meta['media'],
            videos={'1': {'src': v_url}},
            srcLink=response.meta.get('news_url')
        )
