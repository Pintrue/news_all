# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class YcwbAllSpider(NewsRCSpider):
    """长城网"""
    name = 'hebei_all'

    mystart_urls = {

        'http://finance.hebei.com.cn/qyyw/index.shtml': 1301552,  # 长城网-企业要闻-左侧列表
        'http://health.hebei.com.cn/jksx/': 1301554,  # 长城网-健康-左侧列表
        'http://health.hebei.com.cn/ttxw/': 1301555,  # 长城网-健康头条-左侧列表
        'http://health.hebei.com.cn/jkyw/': 1301556,  # 长城网-健康要闻-左侧列表
        'http://travel.hebei.com.cn/xwbd/index.shtml': 1301558,  # 长城网-新闻报道-旅游频道-左侧列表
        'http://edu.hebei.com.cn/xwrbb/': 1301557,  # 长城网-新闻热播榜-左侧列表
        'http://finance.hebei.com.cn/cjzq/cjtt/index.shtml': 1301551,  # 长城网-财经头条-左侧列表
        'http://finance.hebei.com.cn/cjzq/cjrd/index.shtml': 1301550,  # 长城网-财经热点-左侧列表
        'http://finance.hebei.com.cn/yhzq/yhxw/': 1301553,  # 长城网-银行新闻-左侧列表

    }

    # http://finance.hebei.com.cn/system/2019/06/24/019682761.shtml    http://finance.hebei.com.cn/system/2019/06/24/019682345.shtml
    rules = (
        Rule(LinkExtractor(allow=r'hebei.com.cn/system/%s/\d+/\d+.shtml' % datetime.today().strftime('%Y/%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        # 'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract()[0]
            content_div = xp('//div[@class="text"]')[0]
            head_div = xp('//div[@class="post_source"]')[0]
            pubtime = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
                '//*[starts-with(text(), "长城网教育频道新闻投稿")]'])
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos,
        )