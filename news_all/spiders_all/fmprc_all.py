# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class FmprcAllSpider(NewsRCSpider):
    """外交部网站"""
    name = 'fmprc_all'
    mystart_urls = {
        'https://www.fmprc.gov.cn/web/wjbz_673089/zyhd_673091/': 2074,
         'https://www.fmprc.gov.cn/web/wjbz_673089/xghd_673097/': 2075,
         'https://www.fmprc.gov.cn/web/wjbz_673089/zyjh_673099/': 2076,
         'https://www.fmprc.gov.cn/web/wjdt_674879/gjldrhd_674881/': 2077,
         'https://www.fmprc.gov.cn/web/wjdt_674879/wsrc_674883/': 2078,
         'https://www.fmprc.gov.cn/web/wjdt_674879/wjbxw_674885/': 2079,
         'https://www.fmprc.gov.cn/web/wjdt_674879/sjxw_674887/': 2080,
         'https://www.fmprc.gov.cn/web/wjdt_674879/fyrbt_674889/': 2081,
         'https://www.fmprc.gov.cn/web/wjdt_674879/zwbd_674895/': 2082,
         'https://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/': 2083,
         'https://www.fmprc.gov.cn/web/ziliao_674904/1179_674909/': 2084,
    }
    # https://www.fmprc.gov.cn/web/wjbz_673089/zyhd_673091/t1652836.shtml
    # https://www.fmprc.gov.cn/web/ziliao_674904/1179_674909/t1653294.shtml
    rules = (
        Rule(LinkExtractor(allow=r'www.fmprc.gov.cn/web/.*?/t\d{6,}.shtml',
                           restrict_xpaths=r'//div[@class="rebox_news"]/ul/li[contains(text(), "%s")]/a' % datetime.today().strftime(
                               '%Y-%m')
                           ),
             callback='parse_item',
             follow=False),
    )

    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            # https://www.fmprc.gov.cn/web/wjdt_674879/wsrc_674883/t1650627.shtml 标题有多行
            title = xp('//div[@id="News_Body_Title"]')[0].extract()
            cv = xp('//div[contains(@id, "News_Body_Txt")]')[0]
            content, media, video, cover = self.content_clean(cv)

            pubtime = xp('//*[@id="News_Body_Time"]/text()')[0].extract().strip()
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="",
            content=content,
            media=media,
        )