# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class Jbw_allSpider(NewsRCSpider):
	"""京报网"""
	name = 'jbw'

	custom_settings = {
		'DOWNLOADER_MIDDLEWARES': {
			'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
			'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
			'news_all.middlewares.UserAgentMiddleware': 20,
			},
		'DEPTH_LIMIT': 60
	}

	mystart_urls = {
		'http://www.bjd.com.cn/': 1,
		'http://www.bjd.com.cn/rd': 2,
		'http://www.bjd.com.cn/rp': 3,
		'http://www.bjd.com.cn/70n': 4,
		'http://www.bjd.com.cn/ss': 5,
		'http://www.bjd.com.cn/cs': 6,
		'http://www.bjd.com.cn/tx': 7,
		'http://www.bjd.com.cn/sp': 8,
		'http://www.bjd.com.cn/zhb': 9,
		'http://www.bjd.com.cn/xx': 10,
		'http://www.bjd.com.cn/bj': 11,
		'http://www.bjd.com.cn/yz': 12,
		'http://www.bjd.com.cn/ms': 13,
		'http://www.bjd.com.cn/sj': 14,
		'http://www.bjd.com.cn/sd': 15,
		'http://www.bjd.com.cn/jw': 16,
		'http://www.bjd.com.cn/ty': 17,
		'http://www.bjd.com.cn/jj': 18,
		'http://www.bjd.com.cn/fw': 19,
		'http://www.bjd.com.cn/js': 20,
		'http://www.bjd.com.cn/yp': 21,
		'http://www.bjd.com.cn/yyzb': 22,
		'http://www.bjd.com.cn/zt': 23,
		'http://www.bjd.com.cn/jjy': 24,
		'http://www.bjd.com.cn/tt': 25,
	}

	deny_list = [
		r'http://www.bjd.com.cn/zhb',
		r'/200[0-9]',
		r'/201[0-8]',
		r'/2019(?:0[1-9]|10)',
	]

	rules = (
		# 'http://www.bjd.com.cn/a/201911/04/WS5dbf0cb4e4b05b28cd03d798.html'
		# 'http://www.bjd.com.cn/a/201911/08/WS5dc4fb61e4b0621d5c14d098.html'
		# 'http://www.bjd.com.cn/a/201911/08/WS5dc4be7fe4b0621d5c14cf98.html'
		Rule(LinkExtractor(allow=r'bjd.com.cn.*?/%s/\d{2}/\S+\.html' % datetime.today().strftime('%Y%m'),
						   deny=deny_list),
			 callback='parse_item',
			 # process_request=js_meta
			 follow=False),

		Rule(LinkExtractor(allow=r'page_\d+'), follow=True),

		Rule(LinkExtractor(allow=r'bjd.com.cn/\S+.html',
		                   deny=deny_list),
		     process_request=otherurl_meta,
		     follow=False),
	)

	"""
		Class functions of 'Jbw_allSpider' begin
	"""

	# http://www.bjd.com.cn/a/201911/08/WS5dc50890e4b0621d5c14d0a4.html
	def parse_item(self, response):
		xp = response.xpath

		try:
			title = xp("/html/head/title/text()").extract()[0]
			pubtime = xp("//span[@class='span31']/text()").extract_first().split()[1]
			origin_name = xp("//span[@class='span32']/text()").extract()[0]
			content_div = xp("//div[@class='contentnews21']")
			content, media, _, _ = self.content_clean(content_div)
		except Exception as e:
			return self.produce_debugitem(response, 'xpath error - '+str(e))

		return self.produce_item(
		    response=response,
		    title=title,
		    pubtime=pubtime,
		    origin_name=origin_name,
		    content=content,
		    media=media
		)

# mystart_urls = {
	#     'http://www.bjd.com.cn/jx/tp/': 1301448,   #  京报网-主题图片
	#     'http://www.bjd.com.cn/zc/btt/': 1301449,   #  京报网-社会-中间列表采集
	#     'http://www.bjd.com.cn/zc/sbs/': 1301447,   #  京报网-身边
	#     'http://www.bjd.com.cn/sd/mrq/': 1301450,   #  京报网-门儿清-左侧列表
	# }
	#
	# rules = (
	#     # http://www.bjd.com.cn/jx/jj/201906/16/t20190616_11102063.html
	#     # http://www.bjd.com.cn/zc/btt/201906/17/t20190617_11102089.html
	#     # http://www.bjd.com.cn/sd/mrq/201905/22/t20190522_11101411.html
	#     # http://www.bjd.com.cn/zc/sbs/201906/17/t20190617_11102090.html
	#     Rule(LinkExtractor(allow=(r'bjd.com.cn.*?/%s/\d{2}/t\d{8}_\d+.html' % datetime.today().strftime('%Y%m'), ),
	#                        ), callback='parse_item',
	#          follow=False),
	# )
	#
	# def parse_item(self, response):
	#     xp = response.xpath
	#     try:
	#         title = xp("//div[@class='tit']/text()").extract_first()
	#         source = xp("//div[@class='info']")[0]
	#         content_div = xp("//div[@class='TRS_Editor']")[0]
	#         pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
	#         origin_name =xp('//div[@class="info"]/span[2]/text()').extract_first('')
	#         content, media, _, _ = self.content_clean(content_div)
	#     except:
	#         return self.produce_debugitem(response, "xpath error")
	#
	#     return self.produce_item(
	#         response=response,
	#         title=title,
	#         pubtime=pubtime,
	#         origin_name=origin_name,
	#         content=content,
	#         media=media
	#     )
