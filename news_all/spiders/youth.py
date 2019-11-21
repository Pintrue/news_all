# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.html_clean import html2text
from news_all.spider_models import NewsRCSpider, otherurl_meta


class YouthSpider(NewsRCSpider):
    """中国青年网"""
    name = 'youth'

    mystart_urls = {'http://news.youth.cn/': 178,  # '新闻',
                    'http://finance.youth.cn/finance_yw/': 187,  # '财经要闻',
                    'http://agzy.youth.cn/qsnag/zxbd/': 4953,  # 最新报道
                    'http://auto.youth.cn/dg/': 4962,  # 导购
                    'http://auto.youth.cn/pl/': 4957,  # 评论
                    'http://auto.youth.cn/sj/': 4897,  #
                    'http://auto.youth.cn/xc/': 4963,  # 新车
                    'http://auto.youth.cn/xny/': 4958,  # 新能源
                    'http://auto.youth.cn/xw/': 4964,  # 新闻
                    'http://auto.youth.cn/zh/': 4961,  # 召回
                    'http://cunguan.youth.cn/cgxw/': 4994,  # 村官新闻
                    'http://cunguan.youth.cn/cgyc/': 4992,  # 村官原创
                    'http://cunguan.youth.cn/jjsn/': 4993,  # 聚焦三农
                    'http://d.youth.cn/shrgch/': 4997,  # 观察
                    'http://d.youth.cn/tpxw_35291/': 4995,  # 读图
                    'http://df.youth.cn/dfyw/': 4990,  # 地方要闻
                    'http://dysj.youth.cn/snqy/': 4983,  # 三农前沿
                    'http://dysj.youth.cn/ywlm/': 4985,  # 要闻聚焦
                    'http://dysj.youth.cn/zcjd/': 4984,  # 政策解读
                    'http://edu.youth.cn/jyzx/': 5054,  # 教育资讯
                    'http://edu.youth.cn/jyzx/jyxw/': 4943,  # 新闻
                    'http://finance.youth.cn/finance_bank/': 4979,  # 银行
                    'http://finance.youth.cn/finance_consumption/': 4915,  # 更多>>
                    'http://finance.youth.cn/finance_food/': 4978,  # 食品
                    'http://finance.youth.cn/finance_gdxw/': 4977,  # 滚动新闻
                    'http://finance.youth.cn/finance_house/': 4971,  # 房产
                    'http://finance.youth.cn/finance_insurance/': 4974,  # 保险
                    'http://finance.youth.cn/finance_ipo/': 4973,  # IPO
                    'http://finance.youth.cn/finance_IT/': 4970,  # 科技
                    'http://finance.youth.cn/finance_money/': 4972,  # 理财
                    'http://finance.youth.cn/finance_stock/': 128,  # 4980,  # 股市
                    'http://finance.youth.cn/finance_zqjrrdjj/': 4919,  # 更多>>
                    'http://fun.youth.cn/ds/': 4926,  # 电视
                    'http://fun.youth.cn/gnzx/': 4933,  # 娱乐资讯
                    'http://fun.youth.cn/rw/': 4929,  # 明 星
                    'http://fun.youth.cn/ylsd/': 4925,  # 音 乐
                    'http://fun.youth.cn/ys/': 4928,  # 电 影
                    'http://iot.youth.cn/yw/': 4944,  # 要闻
                    'http://lilun.youth.cn/': 4911,  # 理论
                    'http://news.youth.cn/bwyc/': 4947,  # 原创
                    'http://news.youth.cn/gj/': 4948,  # 国际
                    'http://news.youth.cn/gn/': 4949,  # 国内
                    'http://news.youth.cn/jsxw/': 4945,  # 即时新闻
                    'http://news.youth.cn/kj/': 293,  # 4916,  # 科技
                    'http://news.youth.cn/qdj/': 4946,  #
                    'http://news.youth.cn/sh/': 4950,  # 社会
                    'http://news.youth.cn/sz/': 4952,  # 时政
                    'http://news.youth.cn/tbxw/': 4895,  #
                    'http://news.youth.cn/yl/': 4951,  # 娱乐
                    'http://pinglun.youth.cn/': 4912,  # 评论
                    'http://pinglun.youth.cn/ll/': 4910,  # 理论
                    'http://pinglun.youth.cn/rlph/': 4924,  # 更多>>
                    'http://pinglun.youth.cn/shsz/': 4927,  # 时事
                    'http://pinglun.youth.cn/wztt/': 4934,  # 热点
                    'http://qnzs.youth.cn/tsxq/': 4937,  # 新闻库
                    'http://qnzz.youth.cn/tegao/': 4922,  # 特稿
                    'http://wenhua.youth.cn/whdj/': 4986,  # 点睛
                    'http://youxi.youth.cn/shrd/': 4900,  #
                    }

    # http://finance.youth.cn/finance_cyxfrdjj/201901/t20190120_11849057.htm
    rules = (
    Rule(
        LinkExtractor(allow=(r'youth\.cn.*?/%s/t\d+_\d+\.htm' % datetime.today().strftime('%Y%m'),)), callback='parse_item',
         follow=False),

        Rule(LinkExtractor(allow=(r'youth\.cn.*?\d{6,}\.htm',), deny=(r'/201[0-8]', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        try:
            head_div = response.xpath('.//div[@class="page_title"]')[0]
            pubtime = head_div.xpath('./div[1]/span[@id="page_right"]/text()')[0].extract().replace('发稿时间：',
                                                                                                    '').strip()
            content_div = response.xpath(
                './/div[@id="container"]/div[@class="TRS_Editor"]')[0]
            title = head_div.xpath('./h1/text()').extract_first('').strip()

            # http://finance.youth.cn/finance_cyxfrdjj/201901/t20190120_11849057.htm
            origin_name = head_div.xpath(
                './div[1]/span[4]/a/text()').extract_first('')
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        # http://news.youth.cn/gj/201901/t20190120_11849023.htm
        # http://news.youth.cn/sh/201901/t20190116_11846273.htm
        # http://news.youth.cn/sz/201901/t20190120_11849019.htm
        try:
            head_div = response.xpath('.//div[@class="page_bt"]')[0]
            source_div = head_div.xpath('./p[@class="pwz"]')[0]
            source_text = html2text(source_div.extract())
            time_re = re.findall(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}', source_text)
            pubtime = time_re[0]
            content_div = response.xpath('.//div[@class="page_nr"]/div[@class="page_text"]')[0]
            title = head_div.xpath('./p[@class="pbt"]/text()').extract_first('')
            origin_re = re.search('来源：\n.(.*?)\n', source_text)
            origin_name = origin_re.group(1).strip() if origin_re else ''
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item_all(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # http://auto.youth.cn/xw/201903/t20190329_11911335.htm
    def parse_item_all(self, response):
        try:
            news_div = response.xpath('.//div[@class="con"]')[0]
            source_div = news_div.xpath('.//div[@class="yth_con"]/div[@class="source"]')[0]
            pubtime = source_div.xpath('.//span[@class="fb_date"]/text()')[0].extract().replace('发稿时间：',
                                                                                                     '').strip()
            content_div = response.xpath('.//div[@class="TRS_Editor"]')[0]
            title = news_div.xpath('.//*/h1/text()').extract_first('').strip()
            origin_name = source_div.xpath('.//span[@class="soure1"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item_all_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://agzy.youth.cn/qsnag/zxbd/201903/t20190330_11912208.htm
    def parse_item_all_2(self, response):
        try:
            news_div = response.xpath('.//div[@class="concent"]')[0]
            source_div = news_div.xpath('.//div[@class="page_bt"]/p[@class="pwz"]')[0]
            source_text = html2text(source_div.extract())
            time_re = re.findall(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}', source_text)
            pubtime = time_re[0]
            content_div = response.xpath('.//*/div[@class="TRS_Editor"]')[0]
            title = news_div.xpath('./div[@class="page_bt"]/p[@class="pbt"]/text()').extract_first('')
            origin_re = re.search('来源：\n.(.*?)\n', source_text)
            origin_name = origin_re.group(1).strip() if origin_re else ''
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item_all_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://qnzz.youth.cn/qckc/201903/t20190330_11912361.htm
    def parse_item_all_3(self, response):
        try:
            news_div = response.xpath('.//div[@class="main"]/div[@class="main_l"]')[0]
            source_div = news_div.xpath('.//div[2]')[0]
            source_text = html2text(source_div.extract())
            time_re = re.findall(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}', source_text)
            pubtime = time_re[0]
            content_div = response.xpath('.//*/div[@class="TRS_Editor"]')[0]
            title = news_div.xpath('.//div[@class="l_tit"]/text()').extract_first('')
            origin_re = re.search('来源：\n.(.*?)\n', source_text)
            origin_name = origin_re.group(1).strip() if origin_re else ''
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item_all_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://d.youth.cn/shrgch/201903/t20190331_11912693.htm
    # http://df.youth.cn/dfyw/201904/t20190401_11913143.htm
    def parse_item_all_4(self, response):
        try:
            # news_div = response.xpath('.//div[@class="main"]/div[@class="main_l"]')[0]
            source_div = response.xpath('.//div[@class="page_k"]')
            # source_text = html2text(source_div.extract())
            pubtime = source_div.xpath('./div[@class="page_title"]/div[1]/span[@id="page_right"]/text()')[0].extract().replace('发稿时间：', '').strip()
            content_div = response.xpath('.//*/div[@class="TRS_Editor"]')[0]
            title = source_div.xpath('.//*/h1/text()').extract_first('')
            origin_name = source_div.xpath('.//*/span[@id="source_baidu"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
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