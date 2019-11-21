# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.others import to_list
from news_all.spider_models import NewsRCSpider


class DbwSpider(NewsRCSpider):
    """东北网"""
    name = 'dbw'
    mystart_urls = {
        'https://sports.dbw.cn/lq/nba/': 1301364,  # 东北网 NBA-列表
        'https://international.dbw.cn/dycz/': 1301367,  # 东北网 东瀛传真列表
        'https://health.dbw.cn/jrkd/': 1301357,  # 东北网 健康看点
        'https://internal.dbw.cn/wjlb/': 1301370,  # 东北网 国内万象
        'https://internal.dbw.cn/gnxw/': 1301371,  # 东北网 国内要闻列表
        'https://finance.dbw.cn/bxlc/': 1301356,  # 东北网 国内财经-国内列表
        'https://international.dbw.cn/gjxw/': 1301369,  # 东北网 国际新闻列表
        'https://sports.dbw.cn/zq/gjzq/': 1301365,  # 东北网 国际足球
        'https://internal.dbw.cn/dfyw/': 1301366,  # 东北网 地方新闻
        'https://international.dbw.cn/hqlm/': 1301373,  # 东北网 天下博览列表
        'https://society.dbw.cn/qwys/': 1301361,  # 东北网 奇闻异事-列表
        'https://edu.dbw.cn/2014ljjy/2014ljyw/index.shtml': 1301358,  # 东北网 教育要闻-列表
        'https://ms.dbw.cn/jzzz/index.shtml': 1301360,  # 东北网 民生追踪
        'https://auto.dbw.cn/news/': 1301149,  # 东北网 汽车资讯
        'https://internal.dbw.cn/gatxw/': 1301368,  # 东北网 港澳台列表
        'https://society.dbw.cn/shwx/': 1301362,  # 东北网 社会-社会万象列表
        'https://society.dbw.cn/fytx/': 1301363,  # 东北网 社会与法列表
        'https://international.dbw.cn/chbb/': 1301372,  # 东北网 韩朝播报-列表
        'https://tour.dbw.cn/t-hlj/': 1301359,  # 东北网 黑龙江旅游

    }
    rules = (
        # https://internal.dbw.cn/system/2019/06/20/058219310.shtml
        # https://ms.dbw.cn/system/2019/06/19/058218971.shtml
        Rule(LinkExtractor(allow=(r'dbw.cn.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),),
                           ), callback='parse_item',
             follow=False),
    )
    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 若翻页则需要设置深度为0
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))  # 禁止重定向
    }
    
    # https://internal.dbw.cn/system/2019/06/20/058219310.shtml
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='tt_news']/text()").extract_first()
            # source = xp("//div[@class='time-source']")[0]
            content_div = xp("//div[@id='p-detail']")[0]
            pubtime = xp("//div[@class='info']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
        except:
            return self.parse_item_2(response)

        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页" or text()="ÏÂÒ»Ò³"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })

        title, content_div, origin_name = self.trans(title, content_div.extract(), origin_name, response.encoding)
        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
        try:
            content_div = xp("//div[@id='p-detail']")[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
    
        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页" or text()="ÏÂÒ»Ò³"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)

        title = meta_new.get('title')
        origin_name = meta_new.get('origin_name')
        title, content_div, origin_name = self.trans(title, meta_new['content'], origin_name, response.encoding)
        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths='//div[@id="news_more_page_div_id"]')
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=meta_new.get('pubtime'),
            origin_name=origin_name,
            content=content,
            media=media
        )
        
    # https://ms.dbw.cn/system/2019/06/19/058218971.shtml
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='neirong']/h1/text()").extract_first()
            # source = xp("//div[@class='chan_newsInfo_source']")[0]
            content_div = xp("//div[@class='duanluo']")[0]

            pubtime = xp("//div[@class='dizhi hui']/p/span[2]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
        except:
            return self.parse_item_3(response)

        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页" or text()="ÏÂÒ»Ò³"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract()})
        title, content_div, origin_name = self.trans(title, content_div.extract(), origin_name, response.encoding)
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # https: // mp.weixin.qq.com / s / Fdatt7eS6dNsbprgrZOjlg
    def parse_item_3(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@id='activity-name']/text()").extract_first()
            # source = xp("//div[@class='chan_newsInfo_source']")[0]
            content_div = xp("//div[@id='js_content']")[0]

            ps = xp("//em[@id='publish_time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}') or xp("//em[@id='publish_time']").re(
                r'\d+(?:天|小时)前')
            pubtime = ps[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
        except:
            return self.parse_item_4(response)

        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页" or text()="ÏÂÒ»Ò³"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract()})
        title, content_div, origin_name = self.trans(title, content_div.extract(), origin_name, response.encoding)
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # https://m.thepaper.cn/newsDetail_forward_3695599?from=singlemessage
    def parse_item_4(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='t_newsinfo']/text()").extract_first()
            # source = xp("//div[@class='chan_newsInfo_source']")[0]
            content_div = xp("//div[@class='news_part news_part_limit']")[0]

            pubtime = xp("//p[@class='about_news'][2]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')  # <meta name="source" content=" 经济日报">
        except:
            return self.produce_debugitem(response, "xpath error")

        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页" or text()="ÏÂÒ»Ò³"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract()})
        title, content_div, origin_name = self.trans(title, content_div.extract(), origin_name, response.encoding)
        content, media, _, _ = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def trans(self, title, content, origin_name, encoding):
        if encoding != 'utf-8':
            try:
                title = title.encode('ISO-8859-1', errors='ignore').decode('gbk', errors='ignore')
                content = content.encode('ISO-8859-1', errors='ignore').decode('gbk', errors='ignore')
                origin_name = origin_name.encode('ISO-8859-1', errors='ignore').decode('gbk', errors='ignore')
            except Exception as e:  # 'latin-1' codec can't encode character '\u2022' in position 3771: ordinal not in range(256)
                print(e)

        return title, content, origin_name

    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        # 东北网都过滤
        kill_xpaths = to_list(kill_xpaths) + ['//*[contains(text(), "图片版权归原作者所有")]', '//div[@class="gjc"]']
        return super(DbwSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)