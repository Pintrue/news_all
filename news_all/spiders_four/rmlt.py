# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class RMLTSpider(NewsRCSpider):
    """人民论坛_第四批"""
    name = 'rmlt'
    mystart_urls = {
                'http://www.rmlt.com.cn/idea/connection/': 537,   #  独家连线
                'http://www.rmlt.com.cn/idea/dongcha/': 538,   #  时事洞察
                 'http://www.rmlt.com.cn/idea/shengyin/': 539,   #  中国声音
                'http://www.rmlt.com.cn/idea/mingrentang/': 540,   # 思想名人堂
                'http://www.rmlt.com.cn/idea/lilun/': 541,   #  前沿理论
                'http://politics.rmlt.com.cn/gaoceng/': 542,   #  高层动态
                'http://politics.rmlt.com.cn/submissions/': 543,   #  基层来稿
                'http://politics.rmlt.com.cn/news/': 544,   #  时政速递
                'http://politics.rmlt.com.cn/guancha/': 545,   #  深度观察
                'http://politics.rmlt.com.cn/minsheng/': 546,   #  民生热点
                'http://politics.rmlt.com.cn/guoji/': 547,   #  国际视野
                'http://politics.rmlt.com.cn/tupian/': 548,   #  图说新闻        图集
                'http://www.rmlt.com.cn/eco/yaowen/': 549,   #  要闻
                'http://www.rmlt.com.cn/eco/lingdao/': 550,   #  领导论经济
                'http://www.rmlt.com.cn/eco/hongguan/': 551,   #  宏观大势
                'http://www.rmlt.com.cn/eco/caijingredian/': 552,   #  热点观察
                'http://www.rmlt.com.cn/eco/guandianku/': 553,   #  名家观点库
                'http://www.rmlt.com.cn/eco/zhengce/': 554,   #  政策解读
                'http://www.rmlt.com.cn/eco/caijingpinglun/': 555,   #  经济评论
                'http://www.rmlt.com.cn/eco/quanqiujingji/': 556,   #  全球经济

    }
    #http://www.rmlt.com.cn/2019/0225/540320.shtml
    rules = (Rule(LinkExtractor(allow=(r'rmlt.com.cn/.*?\d+.shtml',), ), callback='parse_item', follow=False),)

    def parse_item(self, response):
        try:
            title = response.xpath('//h1/text()')[0].extract()
            try:
                sub_title = response.xpath('//h2/text()')[0].extract()
                if sub_title:
                    if sub_title.startswith("——"):
                        title += sub_title
                    else:
                        title += "——" + sub_title
            except:
                pass

            content_div = response.xpath('//div[@class="article-content fontSizeSmall BSHARE_POP"]')[0]
            pubtime = response.xpath('//span[@class="date"]/text()').extract_first("")
        except:
            return self.produce_debugitem(response, "xpath error")

        origin_name = response.xpath('//span[@class="source"]').extract_first('')
        content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

