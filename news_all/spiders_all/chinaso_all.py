# -*- coding: utf-8 -*-

from datetime import datetime
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider, otherurl_meta


class ChinaSoAllSpider(NewsRCSpider):
    """中国搜索"""
    name = 'chinaso_all'
    mystart_urls = {
        'http://toutiao.chinaso.com/index.html': 1879,
        'http://toutiao.chinaso.com/list/redian/index.html': 1880,
        'http://toutiao.chinaso.com/zuixin/index.html?channel=3297556&queryId=&pageNo=0&type=title&sourceType=0,2,3,4,5&IsRoll=0,1&tableName=news&date=': 1881,
        'http://toutiao.chinaso.com/list/shizheng/index.html': 1882,
        'http://toutiao.chinaso.com/list/guoji/index.html': 1883,
        'http://toutiao.chinaso.com/list/junshi/index.html': 1884,
        'http://toutiao.chinaso.com/list/caijing/index.html': 1885,
        'http://toutiao.chinaso.com/list/keji/index.html': 1886,
        'http://toutiao.chinaso.com/list/shehui/index.html': 1887,
        'http://toutiao.chinaso.com/list/qiche/index.html': 1888,
        'http://toutiao.chinaso.com/list/jiangkang/index.html': 1889,
        'http://toutiao.chinaso.com/list/yuanchuang/index.html': 1890,
        
        # http://toutiao.chinaso.com/list/gaocengdongtai/index.html  # 新闻可以但没打标
        # http://toutiao.chinaso.com/list/xuexixiaozu/index.html  # 新闻可以但没打标
        #  http://toutiao.chinaso.com/index.html  # 新闻可以但没打标
    }
    
    # http://toutiao.chinaso.com/sh/detail/20190415/1000200033137271555306620146919162_1.html
    rules = (
        # http://toutiao.chinaso.com/tttpxqy//image_detail/20190513/1000200033011321557717543487459893_1.html 图集
        Rule(LinkExtractor(
            allow=(r'chinaso.com.*?/image_detail/%s\d{2}/\w+.html' % datetime.today().strftime('%Y%m')), ),  # \w字母下划线
             callback='parse_images', follow=False),
        Rule(LinkExtractor(allow=(r'chinaso.com.*?/%s\d{2}/\w+.html' % datetime.today().strftime('%Y%m')), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'chinaso.com.*?\w{5,}.html'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/home', r'index.html')),
             process_request=otherurl_meta, follow=False),
    )
    
    # http://toutiao.chinaso.com/sh/detail/20190415/1000200033137271555306620146919162_1.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="detail-content"]')[0]
            source_div = news_div.xpath('.//*/div[@class="detail-time"]')[0]
            content_div = news_div.xpath('.//div[@class="detail-main"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        title = ''.join(i.strip() for i in news_div.xpath('.//*/h1[@class="detail-title"]/text()').extract())
        origin_name = source_div.xpath('./span[2]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=["//em[@class='source-color']",
                                                                              "//div[@class='detail-main']/a"])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_images(self, response):
        
        xp = response.xpath
        try:
            title = xp("//*[@id='imgTitle']/text()").extract_first('') or self.get_page_title(response).split('-')[0]
            """
            <meta name="publishTime" content="1557717913000" id="metaPublishTime">
            <meta property="article:published_time" content="2019-05-13 11:25"/>
            """
            pubtime = xp('//head/meta[@name="publishTime" or @id="metaPublishTime"]/@content')[0].extract()
            script_div = xp('//script[contains(text(), "var imgInfo=")]/text()')[0].extract()
            start = script_div.index('var imgInfo=') + len('var imgInfo=')
            end = script_div.find('};') + 1
            txt = script_div[start: end]
            jd = json.loads(txt)
            totalPage = int(jd.get('info').get('totalPage'))
            img_list = jd.get('list', [])
        except:
            return self.produce_debugitem(response, "xpath error")
        if totalPage != len(img_list):
            self.log("图片数量不符!")
        content, media = make_img_content(img_list)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="",
            content=content,
            media=media
        )


def make_img_content(img_cons):
    """拼接json中图、文列表为html
    :param img_cons list
    """
    media = {'images': {}}
    content = ''
    for i, j in enumerate(img_cons):
        content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
        img_url = j['img']
        media['images'][str(i + 1)] = {"src": img_url}
        
        if j.get('note'):
            content += '<p>' + j['note'] + '</p>'
    return content, media
