# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GxnewsSpider(NewsRCSpider):
    '''广西新闻网'''
    # http://edu.gxnews.com.cn/staticpages/20190618/newgx5d08ee1f-18428430.shtml 图文多页 parse_item_5
    # http://www.gxnews.com.cn/staticpages/20150209/newgx54d8680c-12199025.shtml 多页 parse_item_3
    # http://finance.gxnews.com.cn/staticpages/20190611/newgx5cfedc73-18402445.shtml 多页 parse_item_3
    # http://news.gxnews.com.cn/staticpages/20190624/newgx5d1054a7-18444984.shtml 多页 parse_item_3
    name = 'gxnews'
    mystart_urls = {
        'http://finance.gxnews.com.cn/staticmores/168/33168-1.shtml': 1301390,  # 广西新闻网-保险
        'http://finance.gxnews.com.cn/staticmores/152/33152-1.shtml': 1301391,  # 广西新闻网-广西财经列表
        'http://sports.gxnews.com.cn/staticmores/052/38052-1.shtml': 1301395,  # 广西新闻网_体育-正文列表
        'http://finance.gxnews.com.cn/staticmores/151/33151-1.shtml': 1301392,  # 广西新闻网_国内财经
        'http://www.gxnews.com.cn/staticmores/368/11368-1.shtml': 1301396,  # 广西新闻网_娱乐列表
        'http://edu.gxnews.com.cn/staticmores/608/37608-1.shtml': 1301394,  # 广西新闻网_教育-正文列表
        'http://finance.gxnews.com.cn/staticmores/169/33169-1.shtml': 1301393,  # 广西新闻网_行业
    }
    rules = (
        # gxnews.com.cn/staticpages/20190621/newgx5d0ca411-18439348.shtml
        Rule(LinkExtractor(allow=(r'gxnews.com.cn/staticpages/\d{8}/newgx.*?\.s?html'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='article']/h1/text()").extract_first()
            content_div = xp("//div[@class='article-content']")[0]
            # <span class="xh-highlight">2019年06月18日 12:02&nbsp;&nbsp;来源：广西新闻网</span>
            pubtime = xp("//div[@class='article-info']/span[1]/text()").extract_first().split('\xa0')[0]
            origin_name = xp("//div[@class='article-info']/span[1]/text()").extract_first().split('\xa0')[2]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # http://sports.gxnews.com.cn/staticpages/20190623/newgx5d0f7329-18442969.shtml
        xp = response.xpath
        try:
            title = xp("//h2[@class='fs22 MSYH text-center lh40 ptopc']/text()").extract_first()
            # //div[@class='fs14 lh30  ptop']
            content_div = xp("//div[@class='content aborder']")[0]
            # 【时间：2019年06月20日】【来源：广西新闻网】【作者：许爱梅】【编辑：陆权香】
            pubtime = xp("//p[@class='text-center clist']/text()").extract_first().split('】【')[0].replace('【时间：','').strip()
            origin_name = xp("//p[@class='text-center clist']/text()").extract_first().split('】【')[1]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_3(self, response):
        # http://news.gxnews.com.cn/staticpages/20190624/newgx5d1054a7-18444984.shtml 多页
        # http://finance.gxnews.com.cn/staticpages/20190611/newgx5cfedc73-18402445.shtml 多页
        # http://www.gxnews.com.cn/staticpages/20150209/newgx54d8680c-12199025.shtml 多页
        xp = response.xpath
        try:
            title = xp("//td[@class='title']").extract_first()
            content_div = xp("//td[@id='artContent']")[0]
            # <td align="center" class="fs12">时间：2019年06月24日 12:42&nbsp;&nbsp;&nbsp;&nbsp;来源：中国网娱乐&nbsp;&nbsp;&nbsp;&nbsp;编辑：陈丽婕</td>
            pubtime = xp("//td[@class='fs12']/text()").extract_first().split('\xa0\xa0\xa0\xa0')[0].replace('时间：','').strip()
            origin_name = xp("//td[@class='fs12']/text()").extract_first().split('\xa0\xa0\xa0\xa0')[1]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_4(self, response):
        # http://edu.gxnews.com.cn/staticpages/20160331/newgx56fc73b4-14671027.shtml
        xp = response.xpath
        try:
            title = xp("//h2[@class='m-btt lh50 fs22 ff-msyh']/text()").extract_first()
            content_div = xp("//div[@class='m-bct fs14 lh30']")[0]
            # 【时间：2016年03月31日】【来源：广西新闻网】【作者：谢琳琳 潘麒伊】【编辑：金翔义】
            pubtime = xp("//div[@class='m-doc lh36']/text()").extract_first().split('】【')[0].replace('【时间：','').strip()
            origin_name = xp("//div[@class='m-doc lh36']/text()").extract_first().split('】【')[1]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_5(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_5(self, response):
        # http://edu.gxnews.com.cn/staticpages/20190618/newgx5d08ee1f-18428430.shtml 图文多页 没解析图片
        xp = response.xpath
        try:
            title = xp("//div[@class='title']/text()").extract_first()
            content_div = xp("/html/body/center/div[2]/table[6]/tbody/tr/td[2]")[0]
            # 时间：2019年06月18日 21:58&nbsp;&nbsp;来源：广西新闻网&nbsp;&nbsp;&nbsp;&nbsp;作者：黄玲娜 赵春桃		&nbsp;&nbsp;编辑：陆权香
            pubtime = xp("/html/body/center/div[2]/table[1]/tbody/tr/td/text()").extract_first().split('\xa0\xa0')[0].replace('时间：','').strip()
            origin_name = xp("/html/body/center/div[2]/table[1]/tbody/tr/td/text()").extract_first().split('\xa0\xa0')[1]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )