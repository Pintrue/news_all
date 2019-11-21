# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from scrapy import Request
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from lxml import etree
from news_all.tools.html_clean import json_load_html
from news_all.spider_models import NewsRCSpider, NewsRSpider


class HuanqiuSpider(NewsRCSpider):
	"""环球网"""
	name = 'huanqiu'
	dd = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES'))
	dd['news_all.middlewares.ProxyRdMiddleware'] = 100
	custom_settings = {
		'DOWNLOADER_MIDDLEWARES': dd,
		'CONCURRENT_REQUESTS': 1,
		'CONCURRENT_REQUESTS_PER_IP': 1
	}

	mystart_urls = {
		'http://mil.huanqiu.com/': 165,  # '军事',
		'http://world.huanqiu.com/': 166,  # '国际',
		'http://taiwan.huanqiu.com/': 167,  # '台海',
		# 'http://mil.huanqiu.com/gt/': 0,  # '测试图集'
		# 'http://world.huanqiu.com/photo/': 0,  # '测试图集'

		'http://china.huanqiu.com/': 431,  # '国内首页-时政',    首页轮播+列表   #轮播包含图集
		'http://china.huanqiu.com/local/': 432,  # '各地新闻-时政',
		'http://china.huanqiu.com/gangao/': 433,  # '直通港澳-时政',
		'http://china.huanqiu.com/fanfu/': 436,  # '反腐新闻-时政'
		'http://china.huanqiu.com/article/': 438,  # '滚动新闻-时政'
		'http://opinion.huanqiu.com/': 439,  # '评论-头条-时政'
		'http://mil.huanqiu.com/world/': 440,  # '军事-军情动态-军事'
		'http://mil.huanqiu.com/gt/': 441,  # '军事-图说军事-军事'                      图集新闻（后续优化处理）
		'http://oversea.huanqiu.com/': 449,  # '国际-海外看中国-国际'
		'http://world.huanqiu.com/photo/': 450,  # '国际-环球眼-国际'                       图集新闻（后续优化处理）
		'http://world.huanqiu.com/regions/': 451,  # '国际-世界各地-国际'
		'http://world.huanqiu.com/exclusive/': 452,  # '国际-环球独家-国际'
		'http://world.huanqiu.com/article/': 453,  # '国际-国际滚动-国际'
		'http://society.huanqiu.com/': 455,  # '社会'  区域列表\首页轮播+侧方列表
		'http://society.huanqiu.com/societylaw/': 457,  # '社会与法'
		'http://society.huanqiu.com/socialnews/': 458,  # '社会万象'
		'http://society.huanqiu.com/photonew/': 459,  # '图集'   图集新闻（后续优化处理）
		'http://society.huanqiu.com/article/': 460,  # '社会'
		'http://finance.huanqiu.com/': 461,  # 财经首页
		'http://finance.huanqiu.com/roll/': 462,  # 滚动
		'http://tech.huanqiu.com/': 463,  # 科技首页                                      轮播包含图集
		'http://tech.huanqiu.com/per/': 465,  # 科技人物
		'http://tech.huanqiu.com/front/': 466,  # 科技前沿
		'http://tech.huanqiu.com/internet/': 467,  # 互联网+
		'http://tech.huanqiu.com/it/': 468,  # 业内
		'http://tech.huanqiu.com/comm/': 469,  # 5G/通信
		'http://tech.huanqiu.com/aerospace/': 470,  # 航空航天
		'http://tech.huanqiu.com/science/': 471,  # 科学技术
		'http://tech.huanqiu.com/intelligent/': 472,  # 智能化
		'http://tech.huanqiu.com/discovery/': 473,  # 科学探索

		# 来自spiders_all
		'http://go.huanqiu.com/news/lyfp/index.html': 664, 'http://art.huanqiu.com/news/': 665,
		'http://auto.huanqiu.com/globalnews/': 667, 'http://auto.huanqiu.com/newmodel/': 680,
		'http://auto.huanqiu.com/news/': 681, 'http://biz.huanqiu.com/pp/': 684,
		'http://biz.huanqiu.com/zx/': 685, 'http://chamber.huanqiu.com/charity/': 686,
		'http://chamber.huanqiu.com/point/': 697, 'http://chamber.huanqiu.com/projects/': 698,
		'http://china.huanqiu.com/article/?q=ns': 699, 'http://china.huanqiu.com/gangao/index.html': 700,
		'http://china.huanqiu.com/local/index.html': 701, 'http://china.huanqiu.com/photo/': 702,
		'http://city.huanqiu.com/expert/': 703, 'http://city.huanqiu.com/index/': 704,
		'http://city.huanqiu.com/policy/': 705, 'http://city.huanqiu.com/travel/': 706,
		'http://cul.huanqiu.com/toutiao/': 707, 'http://cul.huanqiu.com/wenxue/': 708,
		'http://cul.huanqiu.com/zixun/': 709, 'http://ent.huanqiu.com/hanliu/': 710,
		'http://ent.huanqiu.com/movie/yingshi-gangtai/': 711,
		'http://ent.huanqiu.com/movie/yingshi-guoji/': 712,
		'http://ent.huanqiu.com/movie/yingshi-neidi/': 713,
		'http://ent.huanqiu.com/music/yinle-gangtai/': 714, 'http://ent.huanqiu.com/music/yinle-nedi/': 715,
		'http://ent.huanqiu.com/star/mingxing-gangtai/': 716,
		'http://ent.huanqiu.com/star/mingxing-guoji/': 717,
		'http://ent.huanqiu.com/star/mingxing-neidi/': 718, 'http://ent.huanqiu.com/yuleyaowen/': 719,
		'http://fashion.huanqiu.com/news/': 720, 'http://fashion.huanqiu.com/nxfs/': 721,
		'http://fashion.huanqiu.com/pic/': 722, 'http://finance.huanqiu.com/caigc/': 723,
		'http://finance.huanqiu.com/chanjing/': 724, 'http://finance.huanqiu.com/gjcx/': 725,
		'http://finance.huanqiu.com/hqsl/': 726, 'http://finance.huanqiu.com/jinr/': 727,
		'http://finance.huanqiu.com/lingdu/': 728, 'http://finance.huanqiu.com/nengy/': 729,
		'http://finance.huanqiu.com/roll/index.html': 730, 'http://finance.huanqiu.com/xiaofeil/': 731,
		'http://game.huanqiu.com/': 732, 'http://game.huanqiu.com/gamenews/': 733,
		'http://go.huanqiu.com/news/airline/': 734, 'http://go.huanqiu.com/news/hotel/index.html': 735,
		'http://go.huanqiu.com/news/lyfp/': 736, 'http://go.huanqiu.com/news/qyly/index.html': 737,
		'http://go.huanqiu.com/news/tour/': 738, 'http://go.huanqiu.com/news/tourism/': 739,
		'http://go.huanqiu.com/vision/index.html': 740, 'http://health.huanqiu.com/': 741,
		'http://health.huanqiu.com/baby/': 742, 'http://health.huanqiu.com/exposure/': 743,
		'http://health.huanqiu.com/health_news/': 744, 'http://health.huanqiu.com/health_promotion/': 745,
		'http://health.huanqiu.com/healthindustry/': 746,
		'http://health.huanqiu.com/meirongzhengxing/': 747, 'http://health.huanqiu.com/pictorial/': 748,
		'http://health.huanqiu.com/xunyiweny/': 749, 'http://look.huanqiu.com/article/': 750,
		'http://look.huanqiu.com/hvideo/': 751, 'http://lx.huanqiu.com/ischool/': 752,
		'http://lx.huanqiu.com/life/': 753, 'http://mil.huanqiu.com/aerospace/': 754,
		'http://mil.huanqiu.com/gt/index.html': 755, 'http://mil.huanqiu.com/milmovie/': 756,
		'http://mil.huanqiu.com/world/index.html': 757,
		'http://opinion.huanqiu.com/column/author/801135074.html': 758,
		'http://opinion.huanqiu.com/editorial/': 759, 'http://opinion.huanqiu.com/opinion_china/': 770,
		'http://opinion.huanqiu.com/opinion_world/': 771, 'http://opinion.huanqiu.com/roll.html': 772,
		'http://opinion.huanqiu.com/shanrenping/': 773, 'http://oversea.huanqiu.com/article/': 775,
		'http://oversea.huanqiu.com/breaking-comment/': 777, 'http://auto.huanqiu.com/roll.html': 779,
		'http://oversea.huanqiu.com/chinagraphic/': 780, 'http://sports.huanqiu.com/roll.html': 781,
		'http://photo.huanqiu.com/photoview/?': 782, 'http://photo.huanqiu.com/weekinpicture/?': 783,
		'http://ent.huanqiu.com/roll.html': 784, 'http://look.huanqiu.com/roll.html': 785,
		'http://health.huanqiu.com/roll.html': 786, 'http://tech.huanqiu.com/roll.html': 787,
		'http://taiwan.huanqiu.com/roll.html': 788, 'http://mil.huanqiu.com/roll.html': 789,
		'http://world.huanqiu.com/roll.html': 790, 'http://china.huanqiu.com/roll.html': 791,
		'http://roll.huanqiu.com/': 792, 'http://ski.huanqiu.com/news/': 793,
		'http://smart.huanqiu.com/ai/': 794, 'http://smart.huanqiu.com/city/': 795,
		'http://smart.huanqiu.com/encounter/': 796, 'http://smart.huanqiu.com/iot/': 797,
		'http://smart.huanqiu.com/original/': 798, 'http://smart.huanqiu.com/product/': 799,
		'http://smart.huanqiu.com/prospect/': 800, 'http://smart.huanqiu.com/roll/': 801,
		'http://smart.huanqiu.com/travel/': 802, 'http://smart.huanqiu.com/viewpoint/': 803,
		'http://smart.huanqiu.com/vr/': 804, 'http://society.huanqiu.com/anecdotes/': 805,
		'http://society.huanqiu.com/article/index.html': 806,
		'http://society.huanqiu.com/photonew/index.html': 807,
		'http://society.huanqiu.com/socialnews/index.html': 808,
		'http://society.huanqiu.com/societylaw/index.html': 809,
		'http://sports.huanqiu.com/basketball/cba/': 810, 'http://sports.huanqiu.com/basketball/nba/': 811,
		'http://sports.huanqiu.com/others/zh/': 812, 'http://sports.huanqiu.com/soccer/gn/': 813,
		'http://sports.huanqiu.com/soccer/xj/': 814, 'http://sports.huanqiu.com/soccer/yc/': 815,
		'http://sports.huanqiu.com/soccer/yj/': 816, 'http://taiwan.huanqiu.com/article/': 817,
		'http://tech.huanqiu.com/aerospace/index.html': 818, 'http://tech.huanqiu.com/business/': 820,
		'http://tech.huanqiu.com/comm/index.html': 822, 'http://tech.huanqiu.com/diginews/': 824,
		'http://tech.huanqiu.com/discovery/index.html': 825, 'http://tech.huanqiu.com/domestic/': 826,
		'http://tech.huanqiu.com/elec/': 828, 'http://tech.huanqiu.com/Enterprise/': 829,
		'http://tech.huanqiu.com/game/': 830, 'http://tech.huanqiu.com/internet/index.html': 831,
		'http://tech.huanqiu.com/it/index.html': 832, 'http://tech.huanqiu.com/net/': 833,
		'http://tech.huanqiu.com/news/': 834, 'http://tech.huanqiu.com/observe/': 835,
		'http://tech.huanqiu.com/original/': 838, 'http://tech.huanqiu.com/per/index.html': 840,
		'http://tech.huanqiu.com/photo/': 843, 'http://tech.huanqiu.com/science/index.html': 844,
		'http://tech.huanqiu.com/techchina/': 846, 'http://uav.huanqiu.com/hyg/': 847,
		'http://women.huanqiu.com/news/': 849, 'http://world.huanqiu.com/article/index.html': 850,
		'http://world.huanqiu.com/exclusive/index.html': 851, 'http://world.huanqiu.com/GT_European/': 852,
		'http://world.huanqiu.com/photo/index.html': 858,
		'http://world.huanqiu.com/regions/index.html': 860,
	}

	# http://mil.huanqiu.com/gt/2019-03/2922272.html
	# http://world.huanqiu.com/photo/2019-03/2922625.html
	rules = (
		Rule(LinkExtractor(allow=(r'huanqiu\.com/(?:\w+\-?\w+/)+%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),),
						   deny=(r'huanqiu\.com/(?:gt|photo|financepic|gallery)/', r'go.huanqiu.com/vision',
								 r'finance.huanqiu.com/br/charm', r'v.huanqiu.com/', r'picture')),  # 过滤图集、视频
			 callback='parse_item', follow=False),
		# http://finance.huanqiu.com/financepic/2019-04/2925872.html
		# http://finance.huanqiu.com/br/charm/2018-01/2892401.html
		# http://go.huanqiu.com/vision/2019-03/2925374.html
		# http://tech.huanqiu.com/photo/2019-02/2920892.html
		# http://look.huanqiu.com/funnypicture/2019-03/2924322.html
		# http://look.huanqiu.com/weekinpicture/2019-03/2924289.html
		Rule(LinkExtractor(
			allow=(r'huanqiu\.com/(?:gt|photo|gallery)/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),
				   r'finance.huanqiu.com/financepic/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),
				   r'finance.huanqiu.com/br/charm/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),
				   r'go.huanqiu.com/vision/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),
				   r'look.huanqiu.com/funnypicture/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),
				   r'look.huanqiu.com/weekinpicture/%s/\d{4,}\.html' % datetime.today().strftime('%Y-%m'),)
			),
			 callback='parse_images', follow=False),
	)

	def parse_item(self, response):
		try:
			head_div = response.xpath('.//div[@class="la_tool"]')[0]
			content_div = response.xpath('.//div[@class="la_con"]')[0]
			texts = head_div.xpath('.//*/text()').extract()
			pubtime = texts[0].strip()
			title = ''.join(i.strip() for i in response.xpath('.//h1[@class="tle"]/text()').extract())
			origin_name = texts[2].strip()
			content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
		except:
			return self.parse_item_2(response)

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media,
			videos=videos
		)

	def parse_item_2(self, response):
		# http://china.huanqiu.com/article/2017-11/11382999.html
		try:
			title = response.xpath('//h1/text()')[0].extract().strip()
			content_div = response.xpath('.//div[@id="text"]/p')
			origin_name = response.xpath('.//strong[@id="source_baidu"]')[0].extract()
			pubtime = response.xpath('.//strong[@id="pubtime_baidu"]')[0].extract().strip()
			content, media, videos, cover = self.content_clean(content_div)
		except:
			return self.parse_item3(response)
			# return self.parse_images(response)

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media,
			)

	def parse_item3(self, response):
		xp = response.xpath
		try:
			title = xp("//div[@class='t-container-title']/h3/text()").extract_first()
			# TODO
			source_div = xp('//div[@class="metadata-info"]')
			pubtime = source_div.xpath('/p[@class="time"]')
			origin_name = source_div.xpath('/p[1]/span[@class="source"]/a')

			content_div = xp('.//article/section')
			content, media = self.content_clean(content_div)
		except:
			pass

		return self.produce_item(response=response,
								 title=title,
								 pubtime=pubtime,
								 origin_name=origin_name,
								 content=content,
								 media=media,
								 )

	def parse_images(self, response):
		rt = response.text
		start = rt.find('var imgData =') + len('var imgData =')
		end = start + rt[start:].find('</script>')  # 或者';\r\n\n</script>', 注意不是r';\r\n\n'
		aa = rt[start:end].strip()
		if aa[-1] == ';':
			aa = aa[:-1]
		xp = response.xpath
		try:
			img_cons = json_load_html(aa)['img']
			pubtime = xp('.//li[@class="time"]//span/text()')[0].extract()
		except:
			return self.produce_debugitem(response, "xpath error")
		if not img_cons:
			print('url: %s, have not img_cons' % response.url, '@' * 20)
			return self.produce_debugitem(response, "xpath error")

		title = xp('//h1/strong/text()').extract_first('').strip() or self.get_page_title(response).split('_')[0]
		content, media = make_img_content(img_cons)

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pubtime,
			origin_name='环球网',
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
		img_url = j.get('img_url')
		media['images'][str(i + 1)] = {"src": img_url}

		if j.get('title'):
			content += '<p>' + j['title'] + '</p>'
	return content, media


class HuanqiuXmlSpider(NewsRSpider):
	"""环球网_xml"""
	name = 'huanqiu_xml'

	mystart_urls = {
		'https://m.huanqiu.com/rss/install.htm': 861,
	}

	def parse(self, response):
		"""
		不务正业的代表？两个学医的硬是改行去唱歌，如今一个比一个红
		http://w.huanqiu.com/r/MV8wXzE0NzQzMDc1XzIxNzVfMTU1NTU0ODU0MA==
		2019-04-18 08:49:00
		:param response:
		:return:
		"""

		html = etree.fromstring(bytes(bytearray(response.text, encoding='utf-8')))
		channel_node = html.find('channel')

		for i in channel_node.findall('item'):
			url = i.find('link').text

			pubtime = i.find('pubDate').text
			title = i.find('title').text
			yield Request(url, callback=self.parse_item,
						  meta=dict(title=title, pubtime=pubtime, source_id=response.meta.get('source_id'),
									start_url_time=response.meta.get('start_url_time'),
									schedule_time=response.meta.get('schedule_time')))

	def parse_item(self, response):
		xp = response.xpath
		try:
			origin_name = xp(r'//*[@id="source_baidu"]/@title').extract_first('')
			content_div = xp(r'//div[@class="conText"]/div[@id="text"]')[0]
		except:
			# http://w.huanqiu.com/r/MV8wXzI5Mjg4MTlfMjM2XzE1NTU4OTQzODA=  新华网图片
			# http://look.huanqiu.com/weekinpicture/2019-04/2928472.html  环球网图片
			return self.parse_images(response)
		pubtime = response.meta.get('pubtime')
		# 视频http://w.huanqiu.com/r/MV8wXzE0NzY2NTIyXzExNzdfMTU1NTg5ODIyMA==
		content, media, videos, video_cover = self.content_clean(content_div, need_video=True, kill_xpaths=[
			r'//div[@class="reTopics"]/following-sibling::*',
			r'//div[@class="reTopics"]'])
		return self.produce_item(response=response,
								 title=response.meta.get('title'),
								 pubtime=pubtime,
								 origin_name=origin_name,
								 content=content,

								 media=media,
								 videos=videos,
								 cover=video_cover,
								 )

	def parse_images(self, response):
		rt = response.text
		start = rt.find('var imgData =') + len('var imgData =')
		end = start + rt[start:].find('</script>')  # 或者';\r\n\n</script>', 注意不是r';\r\n\n'
		aa = rt[start:end].strip()
		if aa[-1] == ';':
			aa = aa[:-1]
		xp = response.xpath
		try:
			img_cons = json_load_html(aa)['img']
			pubtime = xp('.//li[@class="time"]//span/text()')[0].extract()
		except:
			return self.produce_debugitem(response, "xpath error")
		if not img_cons:
			return self.produce_debugitem(response, "xpath error")

		title = xp('//h1/strong/text()').extract_first('').strip() or self.get_page_title(response).split('_')[0]
		content, media = make_img_content(img_cons)

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pubtime,
			origin_name='环球网',
			content=content,
			media=media
		)
