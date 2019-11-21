# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from datetime import datetime
from urllib.parse import urljoin

from scrapy import Request
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class LizhiSpider(NewsRCSpider):
	name = 'lizhi'

	downloader_middlewares = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
	downloader_middlewares['news_all.middlewares.PhantomJSMiddleware'] = 540

	custom_settings = {
		'DEPTH_LIMIT': 0,
		'DOWNLOADER_MIDDLEWARES': downloader_middlewares
	}
	start_meta = {'jstype': True}

	mystart_urls = {
		'http://news.jstv.com/': 1,
		'http://news.jstv.com/sz/': 2,
		'http://news.jstv.com/comment/': 3,
		'http://news.jstv.com/yc/lzsp_sort1.shtml': 4,
		'http://news.jstv.com/special/20190703/1562125033831.shtml': 5,
		'http://news.jstv.com/yc/lzsp_sort2.shtml': 6,
		'http://news.jstv.com/yc/lzsp_sort5.shtml': 7,
		'http://news.jstv.com/lzp/': 8,
		'http://news.jstv.com/exposure/': 9,
		'http://news.jstv.com/pxel/': 10,
		'http://news.jstv.com/lzs/': 11,
		'http://news.jstv.com/jiangsu/': 12,
		'http://news.jstv.com/guonei/': 13,
		'http://news.jstv.com/guoji/': 14,
		'http://news.jstv.com/shehui/': 15,
		'http://news.jstv.com/junshi/': 16,
		'http://news.jstv.com/tiyu/': 17,
		'http://news.jstv.com/caijing/': 18,
		'http://news.jstv.com/yule/': 19,
		'http://news.jstv.com/fangchan/': 20,
		'http://news.jstv.com/original/': 21,
		'http://news.jstv.com/keji/': 22,
	}

	deny_list = [
		r'/200[0-9]',
		r'/201[0-8]',
		r'/2019(?:0[1-9]|10)',
		r'/list_\d+.shtml',
		r'http://news.jstv.com/lzttb_pc/'
	]

	rules = (
		Rule(LinkExtractor(allow=r'news.jstv.com/a/%s/\d+.shtml'
		                         % datetime.today().strftime('%Y%m%d'),
		                   deny=deny_list),
		     callback='parse_item',
		     follow=False
		     ),

		Rule(LinkExtractor(allow=r'http://photo.jstv.com/a/\d+.shtml',
		                   deny=deny_list),
		     callback='parse_album',
		     follow=False
		     ),

		Rule(LinkExtractor(allow=r'news.jstv.com/.*?',
		                   deny=deny_list),
		     # callback='parse_redirect',
		     process_request=js_meta,
		     follow=True),
	)

	img_pattern = re.compile(r'data-bigimg=\"(.*?)\"')
	txt_pattern = re.compile(r'alt=\"(.*?)\s*\"')

	"""
		Class functions of 'Lizhi_Spider' begin
	"""

	def parse_item(self, response):
		# http://news.jstv.com/a/20191110/1573398149283.shtml
		xp = response.xpath

		try:
			title = xp('/html/head/title/text()').extract_first().split('_')[0]
			pub_time = xp("//span[@class='time']/text()").extract()[0]
			origin_name = xp("//span[@class='source']/text()").extract()[0]
			content_div = xp("//div[@class='content']")
			content, media, videos, _ = self.content_clean(content_div, need_video=True)

		except Exception as e:
			return self.produce_debugitem(response, 'xpath error - ' + str(e))

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media,
			videos=videos
		)

	def parse_album(self, response):
		# http://photo.jstv.com/a/20191112/1573520088807.shtml
		xp = response.xpath

		try:
			title = xp('/html/head/title/text()').extract_first().split('-')[0]
			pub_time = xp('//div[@class="maintitle wrap"]/span/text()').extract()[0]
			content_div = xp('//div[@class="smallimglist_c fL"]/ul[@class="clearfix"]/li/img')
			content, media = self.concat_album_content(content_div)
		except Exception as e:
			return self.produce_debugitem(response, 'xpath error in parse_album() - ' + str(e))

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			content=content,
			media=media
		)

	def concat_album_content(self, album_content):
		media = {'images': {}}
		content = ''
		for i, j in enumerate(album_content):
			content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
			img_url = self.img_pattern.findall(j.extract())[0]
			media['images'][str(i + 1)] = {"src": img_url}
			if self.txt_pattern.search(j.extract()):
				content += '<p>' +\
				           self.txt_pattern.findall(j.extract())[0] +\
				           '</p>'
		return content, media

# def parse_redirect(self, response):
	#
	# 	if response.status in [301] and 'Location' in response.headers:
	# 		new_url = response.headers['Location']
	# 		new_url = bytes.decode(new_url)
	# 		yield Request(url=new_url, callback=self.parse_redirect)
	# 	elif re.match(r'news.jstv.com/a/%s\d{2}/\d+.shtml'
	# 	              % datetime.today().strftime('%Y%m'),
	# 	              response.url):
	# 		yield Request(url=response.url, callback=self.parse_item)
