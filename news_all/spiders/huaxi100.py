from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRSpider, otherurl_meta, NewsRCSpider
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re
import scrapy
from copy import deepcopy


class Huaxi100(NewsRCSpider):
    name = 'huaxi100'

    # 华西都市报 ==》 补充全站采集
    mystart_urls = {
        'http://news.huaxi100.com/list-253-1.html': 3,  # 华西都市报
        'http://news.huaxi100.com/list-254-1.html': 4,  # 华西都市报
        'http://news.huaxi100.com/list-135-1.html': 5,  # 华西都市报
        'http://news.huaxi100.com/list-227-1.html': 6,  # 华西都市报
        'http://news.huaxi100.com/list-255-1.html': 7,  # 华西都市报
        'http://news.huaxi100.com/list-256-1.html': 8,  # 华西都市报
        'http://news.huaxi100.com/list-257-1.html': 9,  # 华西都市报
        'http://www.huaxi100.com/pic/': 10,  # 华西都市报
        'http://www.huaxi100.com/forum-304-1.html': 11,  # 华西都市报

    }

    rules = (
        # http://news.huaxi100.com/show-254-1028850-1.html
        Rule(LinkExtractor(allow=r'.news.huaxi100.com/.*?\.html', deny=r'/list'),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'.huaxi100.com/.*?\.html', deny=(r'/list', r'/thread', r'/forum', r'/space'),),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        # http://news.huaxi100.com/show-254-1028850-1.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='details_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='details_info']/text()").extract_first())
            content_div = xp("//div[@id='summary']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='details_info']/text()").get().split()[-1]  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )


class Huaxi100_xml(NewsRSpider):
    name = 'huaxi100_xml'

    # 华西都市报 ==》 补充全站采集
    mystart_urls = {
        'http://www.huaxi100.com/': 1,   #  华西都市报
    }

    # http://www.huaxi100.com/a/f74v0o3f8cb
    def parse(self, response):
        hrefs = response.xpath("//div[@class='list']//li/a/@href").extract()
        i = 0
        for href in hrefs:
            try:
                url = re.findall(r'http://www\.huaxi100\.com/\w+/\w+', href)[0]
            except:
                continue
            else:
                try:
                    pubtime = response.xpath("//p[@class='down']/text()").extract()[i]
                    pubtime = re.findall(r'\d+-\d+\s+\d+:\d+', pubtime)[0]
                    title = response.xpath("//p[@class='title']/text()").extract()[i]
                    origin_name = response.xpath("//p[@class='down']/text()").extract()[i].split()[0]
                    i += 1
                except:
                    return self.produce_debugitem(response, "xpath error")

                yield scrapy.Request(url, callback=self.parse_item, meta={'source_id': response.meta.get('source_id'),
                                                                          'first_url': response.url,
                                                                          'pubtime': pubtime,
                                                                          'origin_name': origin_name,
                                                                          'title': title,
                                                                          'start_url_time': response.meta.get('start_url_time'),
                                                                          'schedule_time': response.meta.get('schedule_time')
                                                                          })

    def parse_item(self, response):
        # http://www.huaxi100.com/a/f74v0o3f8cb
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp("//section[@class='sec-content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )



