from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
import re
import json
from scrapy.conf import settings


class PeopleSpider(NewsRCSpider):
    name = 'wy163'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "https://news.163.com/": 1,
    }

    # https://news.163.com/19/1025/02/ESA5Q1HF0001899O.html
    # https://news.163.com/19/1025/08/ESAPKUO10001899O.html
    # http://war.163.com/photoview/4T8E0001/2301528.html

    rules = (
        Rule(LinkExtractor(allow=(r'163.com/19/%s\d{2}/\d{2}/\w+\.html' % datetime.today().strftime('%m'),)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'163.com/\w+/\w+/\d+\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'163.com/.*\d{6}\.html',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # https://news.163.com/19/1025/08/ESAPKUO10001899O.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@id='epContentLeft']/h1").extract_first("")
            pubtime = Pubtime(xp("//div[@class='post_time_source']/text()").extract_first(""))
            content_div = xp("//div[@id='endText']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@id='ne_article_source']/text()").extract_first("")
        # except Exception as e:
        #      return self.produce_debugitem(response, "xpath error")
        except:
            return self.parse_item_2(response)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):

     # https://news.163.com/19/1021/22/ES1UD2LJ0001982T.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='brief']/h1").extract_first("")
            pubtime = Pubtime(xp("//div[@class='pub_time']/text()").extract_first(""))
            content_div = xp("//div[@id='endText']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = {}
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_3(self, response):

        #  http://news.163.com/photoview/00AO0001/2304841.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='headline']/h1/text()").extract_first("")
            pubtime = Pubtime(xp("//div[@class='headline']/span/text()").extract_first(""))
            content_div = xp("//div[@class='picinfo-text']/p/span[1]")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], )
            origin_name = {}
        except:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_4(self, response):
        # http://travel.163.com/photoview/17KK0006/2144767.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='headline']/h1/text()").extract_first()
            pubtime = xp("//div[@class='headline']/span/text()").get()
            origin_name ={}
            news_div = xp("//textarea[@name='gallery-data']/text()").extract_first().strip()
            content_div = news_div.replace("\r\n","")
            param = re.findall("(?<=list:).*(?=})", content_div)[0]
            news = json.loads(param)
            imgs = news.get("list")
            content, media = make_img_content(imgs)

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )


def make_img_content(img_cons):
    """拼接json中图、文列表为html
    :param img_cons list
    """
    media = {'images': {}}
    content = ''
    for i, j in enumerate(img_cons):
        content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
        img_url = j.get('img')
        media['images'][str(i + 1)] = {"src": img_url}
        if j.get('note'):
            content += '<p>' + j['note'] + '</p>'
    return content, media