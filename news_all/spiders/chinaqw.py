# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.conf import settings
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ChinaqwSpider(NewsRCSpider):
    """中国侨网"""
    name = 'chinaqw'
    mystart_urls = {'http://www.chinaqw.com/hqhr/': 209,  # '华侨华人'
                    
                    # 来自spiders_all
                    'http://channel.chinaqw.com/cns/c/hqly-lyzx.shtml': 5340,  #
                    'http://channel.chinaqw.com/cns/c/hwjy-kzxy.shtml': 5322,  #
                    'http://channel.chinaqw.com/cns/c/jjkj-qstz.shtml': 5323,  #
                    'http://channel.chinaqw.com/cns/c/jjkj-rcyj.shtml': 5324,  #
                    'http://www.chinaqw.com/hqhr/hwqt/': 5325,  # 中国侨网-华侨华人-侨团掠影
                    'http://channel.chinaqw.com/cns/c/hwjy-hjzx.shtml': 5326,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-tsyx-xssd.shtml': 5327,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-whjl.shtml': 5328,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-hrwh.shtml': 5329,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-zyys-zyzhw.shtml': 5330,  #
                    'http://channel.chinaqw.com/u/gqtj.shtml': 5331,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-fyms-fydt.shtml': 5332,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-zhcy-rwz.shtml': 5333,  #
                    'http://channel.chinaqw.com/cns/c/zhwh-zhms.shtml': 5334,  #
                    'http://channel.chinaqw.com/u/jckt-jckt.shtml': 5336,  #
                    'http://channel.chinaqw.com/cns/c/hqly-lyts.shtml': 5338,  #
                    'http://channel.chinaqw.com/cns/c/hqly-zqsq.shtml': 5339,  #
                    'http://channel.chinaqw.com/cns/c/qx-jjkj.shtml': 5341,  #
                    'http://channel.chinaqw.com/cns/c/qx-msly.shtml': 5342,  #
                    'http://channel.chinaqw.com/cns/c/qx-whjy.shtml': 5343,  #
                    'http://channel.chinaqw.com/cns/c/hdfw-cgtx.shtml': 5345,  #
                    'http://channel.chinaqw.com/cns/c/qx-shms.shtml': 5346,  #
                    'http://channel.chinaqw.com/cns/c/qx-qxzw.shtml': 5347,  #
                    'http://channel.chinaqw.com/cns/c/hzzx-jsxw.shtml': 5348,  #
                    'http://www.chinaqw.com/hqhr/hrsh/': 5351,  # 中国侨网-华侨华人-华社动态
                    'http://channel.chinaqw.com/cns/c/hqhr-cglx.shtml': 5353,  #
                    'http://channel.chinaqw.com/cns/c/jjkj-dwhz.shtml': 5354,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hwsh.shtml': 5355,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrry.shtml': 5360,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-ymdx.shtml': 5361,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrgs.shtml': 5362,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-fz.shtml': 5364,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-yz.shtml': 5365,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-nmz.shtml': 5366,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-oz.shtml': 5367,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-dyz.shtml': 5368,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hrsh-hrxw-bmz.shtml': 5373,  #
                    'http://channel.chinaqw.com/cns/c/hqhr-hwqt-qtdt-oz.shtml': 5378,  #
                    }
    custom_settings = {'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))}

    # todo 图集
    # http://www.chinaqw.com/hqhr/hd2011/2019/04-21/32222.shtml
    # http://www.chinaqw.com/qx/hd2011/2019/04-23/32290.shtml
   
    rules = (
             Rule(LinkExtractor(allow=(r'chinaqw.com/[a-z]+/%s-\d{2}/\d{5,}\.s?html' % datetime.today().strftime('%Y/%m'),), ),
                  callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'chinaqw.com.*?\d{5,}\.s?html',), deny=(r'/201[0-8]', )),
             process_request=otherurl_meta, follow=False),
    )
  
    def parse_item(self, response):
        try:
            news_div = response.xpath('.//div[@class="qw_list_left"]/div[@class="content"]')[0]
            head_div = news_div.xpath('.//div[@class="left-time"]/div[@class="left-t"]')[0]
            content_div = news_div.xpath('.//div[@class="left_zw"]')[0]
            origin_names = head_div.re('来源：(\w{2,})')
            time_re = head_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('.//h1/text()').extract())

        kill_xpaths = '//p[contains(text(),"来源：中国侨网微信公众号")]/following-sibling::*'
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=kill_xpaths)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_names[0] if origin_names else '',

            content=content,
            media=media
        )
