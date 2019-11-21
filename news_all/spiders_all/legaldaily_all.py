# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class LegalDailyAllSpider(NewsRCSpider):
    """法制网"""
    name = 'legaldaily_all'
    mystart_urls = {

        'http://www.legaldaily.com.cn/index_article/node_100191.htm': 1690,
        'http://www.legaldaily.com.cn/leader/node_34072.htm': 1691,
        'http://www.legaldaily.com.cn/leader/node_34077.htm': 1692,
        'http://www.legaldaily.com.cn/leader/node_34073.htm': 1693,
        'http://www.legaldaily.com.cn/leader/node_34079.htm': 1694,
        'http://www.legaldaily.com.cn/leader/node_34075.htm': 1695,
        'http://www.legaldaily.com.cn/leader/node_34080.htm': 1696,
        'http://www.legaldaily.com.cn/zfzz/node_81120.htm': 1697,
        'http://www.legaldaily.com.cn/zfzz/node_81121.htm': 1698,
        'http://www.legaldaily.com.cn/zfzz/node_81122.htm': 1699,
        'http://www.legaldaily.com.cn/zfzz/node_81131.htm': 1700,
        'http://www.legaldaily.com.cn/zfzz/node_81130.htm': 1701,
        'http://www.legaldaily.com.cn/zfzz/node_81132.htm': 1702,
        'http://www.legaldaily.com.cn/zfzz/node_81127.htm': 1703,
        'http://www.legaldaily.com.cn/judicial/node_80533.html': 1704,
        'http://www.legaldaily.com.cn/judicial/node_80534.html': 1705,
        'http://www.legaldaily.com.cn/judicial/node_80535.html': 1706,
        'http://www.legaldaily.com.cn/judicial/node_80536.html': 1707,
        'http://www.legaldaily.com.cn/judicial/node_80540.html': 1708,
        'http://www.legaldaily.com.cn/judicial/node_80541.html': 1709,
        'http://www.legaldaily.com.cn/judicial/node_80542.html': 1710,
        'http://www.legaldaily.com.cn/judicial/node_80543.html': 1711,
        'http://www.legaldaily.com.cn/judicial/node_80544.html': 1712,
        'http://www.legaldaily.com.cn/judicial/node_80545.html': 1713,
        'http://www.legaldaily.com.cn/rdlf/node_34020.htm': 1714,
        'http://www.legaldaily.com.cn/rdlf/node_34017.htm': 1715,
        'http://www.legaldaily.com.cn/rdlf/node_34014.htm': 1716,
        'http://www.legaldaily.com.cn/rdlf/node_76928.htm': 1717,
        'http://www.legaldaily.com.cn/rdlf/node_76929.htm': 1718,
        'http://www.legaldaily.com.cn/rdlf/node_76930.htm': 1719,
        'http://www.legaldaily.com.cn/rdlf/node_34013.htm': 1720,
        'http://www.legaldaily.com.cn/node_80564.htm': 1721,
        'http://www.legaldaily.com.cn/legal_case/node_81780.htm': 1722,
        'http://www.legaldaily.com.cn/legal_case/node_81775.htm': 1723,
        'http://www.legaldaily.com.cn/legal_case/node_81774.htm': 1724,
        'http://www.legaldaily.com.cn/Culture/node_80971.htm': 1725,
        'http://www.legaldaily.com.cn/Culture/node_80972.htm': 1726,
        'http://www.legaldaily.com.cn/Culture/node_80984.htm': 1727,
        'http://www.legaldaily.com.cn/Culture/node_80976.htm': 1728,
        'http://www.legaldaily.com.cn/Culture/node_80981.htm': 1729,
        'http://www.legaldaily.com.cn/army/node_80560.htm': 1730,
        'http://www.legaldaily.com.cn/army/node_80559.htm': 1731,
        'http://www.legaldaily.com.cn/army/node_80558.htm': 1732,
        'http://www.legaldaily.com.cn/army/node_80556.htm': 1733,
        'http://www.legaldaily.com.cn/army/node_80554.htm': 1734,
        'http://www.legaldaily.com.cn/army/node_80550.htm': 1735,
        'http://www.legaldaily.com.cn/army/node_80549.htm': 1736,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75681.html': 1737,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75675.html': 1738,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75679.html': 1739,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75678.html': 1740,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100892.html': 1741,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100887.html': 1742,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_76151.html': 1743,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100888.html': 1744,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_76150.html': 1745,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100889.html': 1746,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100890.html': 1747,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_100891.html': 1748,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75674.html': 1749,
        'http://www.legaldaily.com.cn/Finance_and_Economics/node_75682.html': 1750,
        'http://www.legaldaily.com.cn/commentary/node_34251.htm': 1751,
        'http://www.legaldaily.com.cn/commentary/node_34252.htm': 1752,
        'http://www.legaldaily.com.cn/commentary/node_34259.htm': 1753,
        'http://www.legaldaily.com.cn/commentary/node_34253.htm': 1754,
        'http://www.legaldaily.com.cn/commentary/node_34258.htm': 1755,
        'http://www.legaldaily.com.cn/commentary/node_34254.htm': 1756,
        'http://www.legaldaily.com.cn/commentary/node_34257.htm': 1757,
        'http://www.legaldaily.com.cn/commentary/node_34255.htm': 1758,
        'http://www.legaldaily.com.cn/commentary/node_34256.htm': 1759,
        'http://www.legaldaily.com.cn/commentary/node_34249.htm': 1760,
        'http://www.legaldaily.com.cn/commentary/node_34250.htm': 1761,
        'http://www.legaldaily.com.cn/Personnel_matters/node_78109.htm': 1762,
        'http://www.legaldaily.com.cn/Personnel_matters/node_78110.htm': 1763,
        'http://www.legaldaily.com.cn/Personnel_matters/node_78128.htm': 1764,
        'http://www.legaldaily.com.cn/Personnel_matters/node_78135.htm': 1765,
        'http://www.legaldaily.com.cn/Personnel_matters/node_78136.htm': 1766,
        'http://www.legaldaily.com.cn/fxjy/node_89856.htm': 1767,
        'http://www.legaldaily.com.cn/fxjy/node_89855.htm': 1768,
        'http://www.legaldaily.com.cn/fxjy/node_89854.htm': 1769,
        'http://www.legaldaily.com.cn/fxjy/node_89853.htm': 1770,
        'http://www.legaldaily.com.cn/fxjy/node_89852.htm': 1771,
        'http://www.legaldaily.com.cn/fxjy/node_89850.htm': 1772,
        'http://www.legaldaily.com.cn/fxjy/node_89848.htm': 1773,
        'http://www.legaldaily.com.cn/fxjy/node_89847.htm': 1774,
        'http://www.legaldaily.com.cn/government/node_81789.htm': 1775,
        'http://www.legaldaily.com.cn/government/node_81790.htm': 1776,
        'http://www.legaldaily.com.cn/government/node_81791.htm': 1777,
        'http://www.legaldaily.com.cn/government/node_81792.htm': 1778,
        'http://www.legaldaily.com.cn/government/node_81793.htm': 1779,
        'http://www.legaldaily.com.cn/government/node_81795.htm': 1780,
        'http://www.legaldaily.com.cn/international/node_81910.html': 1781,
        'http://www.legaldaily.com.cn/international/node_81911.html': 1782,
        'http://www.legaldaily.com.cn/international/node_81912.html': 1783,
        'http://www.legaldaily.com.cn/international/node_81913.html': 1784,
        'http://www.legaldaily.com.cn/international/node_81914.html': 1785,
        'http://www.legaldaily.com.cn/international/node_81930.html': 1786,
        'http://www.legaldaily.com.cn/international/node_81917.html': 1787,
        'http://www.legaldaily.com.cn/international/node_81919.html': 1788,
        'http://www.legaldaily.com.cn/international/node_81920.html': 1789,
        'http://www.legaldaily.com.cn/Notarization/node_90031.htm': 1791,
        'http://www.legaldaily.com.cn/Notarization/node_90033.htm': 1799,
        # 'http://www.legaldaily.com.cn/Arbitration/node_100348.html': 1802,
        'http://www.legaldaily.com.cn/Arbitration/node_100353.html': 1807,
        'http://www.legaldaily.com.cn/integrity-observe/node_42783.htm': 1814,
        'http://www.legaldaily.com.cn/integrity-observe/node_42779.htm': 1816,
        'http://www.legaldaily.com.cn/integrity-observe/node_42778.htm': 1818,
        'http://www.legaldaily.com.cn/integrity-observe/node_42780.htm': 1819,
        'http://www.legaldaily.com.cn/integrity-observe/node_42772.htm': 1820,
        'http://www.legaldaily.com.cn/Education_Channel/node_100819.html': 1821,
        'http://www.legaldaily.com.cn/Education_Channel/node_100830.html': 1822,
        'http://www.legaldaily.com.cn/IT/node_69471.htm': 1823,
        'http://www.legaldaily.com.cn/IT/node_69470.htm': 1824,
        'http://www.legaldaily.com.cn/IT/node_69472.htm': 1825,
        'http://www.legaldaily.com.cn/IT/node_69474.htm': 1826,
        'http://www.legaldaily.com.cn/IT/node_69475.htm': 1827,
        'http://www.legaldaily.com.cn/IT/node_69477.htm': 1828,
        'http://www.legaldaily.com.cn/IT/node_69484.htm': 1829,
        'http://www.legaldaily.com.cn/Fire_control/node_89492.html': 1830,

    }


    # http://www.legaldaily.com.cn/index_article/content/2019-04/15/content_7829930.htm
    rules = (
        Rule(LinkExtractor(allow=(r'legaldaily.com.cn/.*?/%s/\d+.*?\d+.htm' % datetime.today().strftime('%Y-%m')), ),
                           callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="div640"]/dl[@class="dl640"]/dd[@class="dd640wz"]')[0]
            source_div = news_div.xpath('.//dl/dd[@class="f12 black02 yh"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('./dl/dd[@id="CONTENT" or @class="f14 black02 yh"]')[0]
        except:
           return self.parse_item2(response)

        title = ''.join(i.strip() for i in response.xpath(
            './/dl/dd[@class="f18 b black02 yh center"]/text()').extract())
        origin_name = news_div.xpath('./dl/dd[@class="f12 black02"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/commentary/content/2019-04/12/content_7828471.htm
    def parse_item2(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//body/div[@id="div1"]')[0]
            source_div = xp('.//article/table')[1]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@id="ShowContent"]')[0]
        except:
            return self.parse_item3(response)

        title = ''.join(i.strip() for i in news_div.xpath('.//*/td[@class="f22 b black"]/text()').extract())
        origin_name = news_div.xpath('.//*/td[@class="f12 black"]/table/tbody/tr/td[@class="f12 black"][1]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/leader/content/2019-04/11/content_7828106.htm
    def parse_item3(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="div1"]/div[1]/div[1]/div[2]/table')[0]
            source_div = xp('.//table//table')[1]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@id="ShowContent"]')[0]
        except:
            return self.parse_item4(response)

        title = ''.join(i.strip() for i in news_div.xpath('.//*/td[@class="f22 b black"]/text()').extract())
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/judicial/content/2019-04/10/content_7826484.html
    def parse_item4(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="warp"]/div[@class="inner_1400"]/div[@class="div1400"][3]/div[@id="div1000"]/div[@class="main3_1"]')[0]
            source_div = xp('.//div[@class="main3_6"]/dl/dd[@class="f12 black02"]/text()')[0]
            head_div = xp('.//div[@class="main3_6"]/dl/dd[@class="f12 balck02 yh"][1]')[0]
            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@class="main3_6"]/dl/dd[@class="f14 black02 yh"]')[0]
        except:
           return self.parse_item5(response)

        # title = ''.join(i.strip() for i in news_div.xpath('.//div[@class="main3_6"]/dl/dd[@class="f16 black02 yh center"][2]/text()').extract())
        title = ''.join(i.strip() for i in response.xpath(
            '//dl/dd[contains(@class, "black02 yh center")]/text()').extract())
        origin_name = source_div.extract()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/zfzz/content/2019-04/12/content_7828834.htm
    def parse_item5(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="div640"]/dl[@class="dl640"]/dd[@class="dd640wz"]')[0]
            source_div = news_div.xpath('./dl/dd[@class="f12 black02"]/text()')[0]
            head_div = news_div.xpath('./dl/dd[@class="f12 balck02 yh"]')[0]
            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('.//dl/dd[@class="f14 black02 yh"]')[0]
        except:
            return self.parse_item6(response)

        # title = ''.join(i.strip() for i in news_div.xpath('.//div[@class="main3_6"]/dl/dd[@class="f16 black02 yh center"][2]/text()').extract())
        title = ''.join(i.strip() for i in response.xpath(
            '//dl/dd[contains(@class, "black02 yh center")]/text()').extract())
        origin_name = source_div.extract()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/rdlf/content/2019-03/28/content_7813581.htm
    def parse_item6(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="div640"]/dl[@class="dl640"]/dd[@class="dd640wz"]')[0]
            source_div = news_div.xpath('.//article/table//table')[0]
            content_div = news_div.xpath('.//article/div[@id="ShowContent"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.parse_item7(response)

        title = ''.join(i.strip() for i in news_div.xpath('.//td[@class="f22 b black02"]/text()').extract())
        origin_name = source_div.xpath('./tbody/tr/td[@class="f12 black02"][1]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.legaldaily.com.cn/Personnel_matters/content/2019-01/09/content_7740941.htm
    def parse_item7(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="div705"]/dl[@class="dl735"]/dd[@class="dd660wz"]')[0]
            source_div = news_div.xpath('.//article/table//table')[0]
            content_div = news_div.xpath('.//article/div[@id="ShowContent"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('.//td[@class="f22 b black02"]/text()').extract())
        origin_name = source_div.xpath('./tbody/tr/td[@class="f12 black02"][1]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
