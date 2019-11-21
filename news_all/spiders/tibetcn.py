# -*- coding: utf-8 -*-
import json
import re
from base64 import b64decode
from copy import deepcopy
from datetime import datetime
from urllib.request import urlopen

from scrapy.conf import settings

from news_all.spider_models import NewsRCSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class TibetCNSpider(NewsRCSpider):
	"""中国西藏网"""
	name = 'tibetcn'

	mystart_urls = {
		'http://www.tibet.cn/': 1,
		'http://www.tibet.cn/cn/news/yc/': 2,
		'http://www.tibet.cn/cn/news/zx/': 3,
		'http://www.tibet.cn/cn/news/zcdt/': 4,
		'http://www.tibet.cn/cn/politics/': 5,
		'http://www.tibet.cn/cn/bwsp/': 6,
		'http://www.tibet.cn/cn/culture/ms/': 7,
		'http://www.tibet.cn/cn/culture/gy/': 8,
		'http://www.tibet.cn/cn/culture/zx/': 9,
		'http://www.tibet.cn/cn/culture/wx/': 10,
		'http://www.tibet.cn/cn/aid_tibet/news/': 11,
		'http://www.tibet.cn/cn/aid_tibet/rw/': 12,
		'http://www.tibet.cn/cn/travel/': 13,
		'http://www.tibet.cn/cn/medicine/news/': 14,
		'http://www.tibet.cn/cn/medicine/jbzl/': 15,
		'http://www.tibet.cn/cn/medicine/sjys/': 16,
		'http://www.tibet.cn/cn/theory/zjcs/': 17,
		'http://www.tibet.cn/cn/theory/news/': 18,
		'http://www.tibet.cn/cn/rediscovery/': 19,
		'http://www.tibet.cn/cn/religion/': 20,
		'http://media.tibet.cn/photo/news/list.shtml': 21,
		'http://media.tibet.cn/photo/landscape/list.shtml': 22,
		'http://media.tibet.cn/photo/custom/list.shtml': 23,
		'http://media.tibet.cn/photo/special/list.shtml': 24,
		'http://www.tibet.cn/cn/tech/': 25,
		'http://www.tibet.cn/cn/book/': 26,
		'http://www.tibet.cn/cn/vg/': 27,
		'http://www.tibet.cn/cn/data/': 28,
		'http://www.tibet.cn/cn/edu/': 29,
		'http://www.tibet.cn/cn/ecology/': 30,
		'http://www.tibet.cn/cn/fp/': 31,
		'http://www.tibet.cn/cn/network/dt/': 32,
		'http://www.tibet.cn/cn/cloud/xszypk/a/': 33,
		'http://www.tibet.cn/cn/cloud/xszypk/b/': 34,
		'http://www.tibet.cn/cn/cloud/xszypk/c/': 35,
		'http://www.tibet.cn/cn/cloud/xszypk/d/': 36,
		'http://www.tibet.cn/cn/cloud/xszypk/e/': 37,
	}

	custom_settings = {
		'DEPTH_LIMIT': 0,
		'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
	}

	deny_list = [
		r'french.tibet.cn/fr',
		r'german.tibet.cn/de',
		r'eng.tibet.cn/eng',
		r'tb.tibet.cn/tb',
		r'tibet.cn/cn/cloud/',
		r'/gywm/',
		r'/201[0-8]',
		r'/200[0-9]',
		r'/2019(?:0[1-9]|10)',
	]

	rules = (
		Rule(
			LinkExtractor(
				allow=r'tibet.cn.*?/%s/t\d+_\d+.html'
				      % datetime.today().strftime('%Y%m'),
				deny=deny_list),
			callback='parse_item',
			follow=False
		),
		Rule(
			LinkExtractor(
				allow=r'media.tibet.cn/*photo.*?/content_\d+.shtml',
				deny=deny_list),
			callback='parse_photo',
			follow=False
		),
		Rule(
			LinkExtractor(
				allow=r'media.tibet.cn/video.*?/%s\d{2}/\d+.shtml'
				      % datetime.today().strftime('%Y%m'),
				deny=deny_list),
			callback='parse_video',
			follow=False
		),
	)

	pub_time_pattern = re.compile(r'发布时间：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
	json_str_pattern = re.compile(r'var.*?=({.*?});')
	encoded_json_pattern = re.compile(r'json:"(.*?)"')

	"""
	"""
	"""
	class functions begin
	"""
	"""
	"""

	def parse_item(self, response):
		# http://www.tibet.cn/cn/index/politics/polotocs1/201911/t20191114_6708823.html
		xp = response.xpath

		try:
			title = xp("//h2/text()").extract()[0]
			# pub_time = xp("/html/head/meta[@name='publishdate']/@content").extract()[0]
			pub_time_div = xp("//div[@class='title_box']/div[@class='info']//span[2]/text()").extract()[0]
			pub_time = self.pub_time_pattern.findall(pub_time_div)[0]
			origin_name = xp("/html/head/meta[@name='source']/@content").extract()[0]
			content_div = xp("//div[@class='content']/div[@class='left']/div[@id='text']").extract()[0]
			content, media, _, _ = self.content_clean(content_div)
		except Exception as e:
			print("error %s at parse_item() when parsing %s" % (str(e), response.url))
			return

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media,
		)

	def parse_photo(self, response):
		# http://media.tibet.cn/photo/landscape/content_12289.shtml
		xp = response.xpath

		try:
			json_url = re.sub(r'photo/.*?/content', 'picture/pic', response.url).replace('.shtml', '.js')
			origin_name = xp("/html/head/meta[@name='source']/@content").extract()[0]
		except Exception as e:
			print("error %s at parse_photo() when parsing %s" % (str(e), response.url))
			return

		return response.follow(json_url, callback=self.parse_photo_json,
		                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
		                             'origin_name': origin_name,
									'start_url_time': response.meta.get('start_url_time'),
									'schedule_time': response.meta.get('schedule_time')}
		                       )

	def parse_photo_json(self, response):
		# http://media.tibet.cn/picture/pic_12289.js

		try:
			json_str = response.text
			json_str = self.json_str_pattern.findall(json_str)[0]
			json_str = json_str.replace('\'', '\"')

			json_dict = json.loads(json_str)
			title = json_dict['title']
			pub_time = json_dict['pubdate']
			origin_name = response.meta['origin_name']

			media = {'images': {}}
			content = ''

			content_list = json_dict['contents']
			pic_num = len(content_list)

			for i in range(pic_num):
				media['images'][i + 1] = {'src': content_list[i]['photo']}
				content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
				content += '<p>' + content_list[i]['summary'] + '</p>'

		except Exception as e:
			print("error %s at parse_photo_json() when parsing %s" % (str(e), response.url))
			return

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media,
			srcLink=response.meta['first_url']
		)

	def parse_video(self, response):
		# http://media.tibet.cn/video/p/20191106/1573041896651.shtml
		xp = response.xpath

		try:
			title = xp("/html/head/title/text()").extract_first().split('_')[0]
			pub_time = xp("/html/head/meta[@name='publishdate']/@content").extract()[0]
			origin_name = xp("/html/head/meta[@name='source']/@content").extract()[0]
			content_div = xp("//div[@class='video_summ']")
			content, media, _, _ = self.content_clean(content_div,
			                                          kill_xpaths=[r'/div[@id="share"]']
			                                          )
			# videos =
			encoded_json_url_text = xp('//*[@id="tide_player"]/script/text()').extract()[0]
			encoded_json_url = self.encoded_json_pattern.findall(encoded_json_url_text)[0]
			json_url = b64decode(encoded_json_url).decode('utf-8')
			json_response = json.loads(urlopen(json_url)
			                           .read()
			                           .decode('utf-8')
			                           )
			vid_url = json_response['videos'][0]['url']

		except Exception as e:
			print("error %s at parse_video() when parsing %s" % (str(e), response.url))
			return

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content='<div>#{{1}}#</div>' + content,
			media=media,
			videos={'1': {'src': vid_url}}
		)
