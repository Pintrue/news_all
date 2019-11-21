# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings

from news_all.spider_models import otherurl_meta
from news_all.spider_models import NewsRCSpider, js_meta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class NanhaiSpider(NewsRCSpider):
	name = 'nanhai'

	mystart_urls = {
		'http://www.hinews.cn/': 6509,
		'http://www.hinews.cn/news/hainan/': 6510,
		'http://www.hinews.cn/news/hainan/': 6511,
		'http://www.hinews.cn/news/hainan/liucigui/': 6512,
		'http://www.hinews.cn/news/hainan/shenxiaoming/': 6513,
		'http://www.hinews.cn/news/hainan/shizheng/': 6514,
		'http://www.hinews.cn/news/hainan/shehui/': 6515,
		'http://www.hinews.cn/news/hainan/jingji/': 6516,
		'http://www.hinews.cn/news/hainan/yule/': 6517,
		'http://www.hinews.cn/news/hainan/wldc/': 6518,
		'http://www.hinews.cn/news/hainan/dujia/': 6519,
		'http://www.hinews.cn/news/hainan/tujie/': 6520,
		'http://www.hinews.cn/news/hainan/rensrm/': 6521,
		'http://www.hinews.cn/news/hainan/quanwfb/': 6522,
		'http://www.hinews.cn/news/xuan/': 6523,
		'http://www.hinews.cn/news/hainan/zt12345/': 6524,
		'http://www.hinews.cn/news/shiping/index.shtml': 6525,
		'http://www.hinews.cn/news/shiping/toujpl/index.shtml': 6526,
		'http://www.hinews.cn/news/shiping/dpx/index.shtml': 6527,
		'http://www.hinews.cn/news/shiping/djpl/': 6528,
		'http://www.hinews.cn/news/shiping/zrp/index.shtml': 6529,
		'http://www.hinews.cn/news/shiping/guanhaichao/index.shtml': 6530,
		'http://www.hinews.cn/news/shiping/hnrbyl/index.shtml': 6531,
		'http://www.hinews.cn/news/shiping/jianyhn/index.shtml': 6532,
		'http://www.hinews.cn/news/shiping/nanhwl/index.shtml': 6533,
		'http://www.hinews.cn/news/shiping/shizlw/index.shtml': 6534,
		'http://www.hinews.cn/news/shiping/shehcj/index.shtml': 6535,
		'http://www.hinews.cn/news/shiping/wenypp/index.shtml': 6536,
		'http://www.hinews.cn/news/shiping/mtjj/index.shtml': 6537,
		'http://ms.hinews.cn/myztc_index.php': 6538,
		'http://ms.hinews.cn/lookingfor_leader.php': 6539,
		'http://ms.hinews.cn/comment.php': 6540,
		'http://v.hinews.cn/': 6541,
		'http://v.hinews.cn/duj.php': 6542,
		'http://v.hinews.cn/rdss.php': 6543,
		'http://v.hinews.cn/img/20130428/shipindaohang.jpg': 6544,
		'http://v.hinews.cn/zbhf.php': 6545,
		'http://v.hinews.cn/shgj.php': 6546,
		'http://v.hinews.cn/mxyl.php': 6547,
		'http://v.hinews.cn/gxlq.php': 6548,
		'http://v.hinews.cn/yevideo.php': 6549,
		'http://v.hinews.cn/yjp_index.php': 6550,
		'http://v.hinews.cn/duj.php': 6551,
		'http://v.hinews.cn/gcdy.php': 6552,
		'http://v.hinews.cn/duj.php': 6553,
		'http://v.hinews.cn/shiz.php': 6554,
		'http://v.hinews.cn/mins.php': 6555,
		'http://v.hinews.cn/lvy.php': 6556,
		'http://v.hinews.cn/wenh.php': 6557,
		'http://v.hinews.cn/qiongju.php': 6558,
		'http://v.hinews.cn/zbhf.php': 6559,
		'http://v.hinews.cn/jbft.php': 6560,
		'http://v.hinews.cn/shgj.php': 6561,
		'http://v.hinews.cn/gnxw.php': 6562,
		'http://v.hinews.cn/gjxw.php': 6563,
		'http://v.hinews.cn/kanhn.php': 6564,
		'http://v.hinews.cn/mxyl.php': 6565,
		'http://v.hinews.cn/yul.php': 6566,
		'http://v.hinews.cn/tiy.php': 6567,
		'http://www.hinews.cn/news/paihang_index.shtml': 6568,
		'http://yuqing.hinews.cn/#q2': 6569,
		'http://house.hinews.cn/': 6570,
		'http://house.hinews.cn/column.php?cid=1': 6571,
		'http://house.hinews.cn/column.php?cid=2': 6572,
		'http://house.hinews.cn/column.php?cid=4': 6573,
		'http://house.hinews.cn/column.php?cid=5': 6574,
		'http://money.hinews.cn/': 6575,
		'http://money.hinews.cn/zonghcj.php': 6576,
		'http://money.hinews.cn/zuixcphd.php': 6577,
		'http://money.hinews.cn/yinhzx.php': 6578,
		'http://money.hinews.cn/tuozfx.php': 6579,
		'http://money.hinews.cn/liczz.php': 6580,
		'http://money.hinews.cn/haincj.php': 6581,
		'http://money.hinews.cn/zhengjsccl.php': 6582,
		'http://money.hinews.cn/jingjgc.php': 6583,
		'http://money.hinews.cn/yinhlc.php': 6584,
		'http://money.hinews.cn/baoxzx.php': 6585,
		'http://money.hinews.cn/gup.php': 6586,
		'http://money.hinews.cn/jij.php': 6587,
		'http://money.hinews.cn/waih.php': 6588,
		'http://money.hinews.cn/qih.php': 6589,
		'http://money.hinews.cn/caip.php': 6590,
		'http://money.hinews.cn/caifgs.php': 6591,
		'http://money.hinews.cn/touzsc.php': 6592,
		'http://120.hinews.cn/': 6593,
		'http://120.hinews.cn/rbzk.php': 6594,
		'http://120.hinews.cn/jkjj.php': 6595,
		'http://120.hinews.cn/zjhkt.php': 6596,
		'http://120.hinews.cn/ysys.php': 6597,
		'http://120.hinews.cn/pgt.php': 6598,
		'http://120.hinews.cn/jkhn_index.php': 6599,
		'http://edu.hinews.cn/': 6600,
		'http://edu.hinews.cn/jyyw.php': 6601,
		'http://edu.hinews.cn/xyzx.php': 6602,
		'http://edu.hinews.cn/zthd.php': 6603,
		'http://edu.hinews.cn/zspx.php': 6604,
		'http://edu.hinews.cn/jyhs.php': 6605,
		'http://edu.hinews.cn/gxjy.php': 6606,
		'http://edu.hinews.cn/znjy.php': 6607,
		'http://edu.hinews.cn/zxjy.php': 6608,
		'http://edu.hinews.cn/yejy.php': 6609,
		'http://edu.hinews.cn/kszl.php': 6610,
		'http://auto.hinews.cn/': 6611,
		'http://auto.hinews.cn/new_qcyw.php': 6612,
		'http://auto.hinews.cn/new_bdzx.php': 6613,
		'http://huodong.hinews.cn/album/': 6614,
		'http://haikou.hinews.cn/': 6615,
		'http://sanya.hinews.cn/': 6616,
		'http://sansha.hinews.cn/': 6617,
		'ttp://sansha.hinews.cn/ssdt/index.shtml': 6618,
		'http://danzhou.hinews.cn/': 6619,
		'http://qionghai.hinews.cn/': 6620,
		'http://wenchang.hinews.cn/': 6621,
		'http://wanning.hinews.cn/': 6622,
		'http://dongfang.hinews.cn/': 6623,
		'http://wzs.hinews.cn/': 6624,
		'http://ledong.hinews.cn/': 6625,
		'http://chengmai.hinews.cn/': 6626,
		'http://lingao.hinews.cn/': 6627,
		'http://dingan.hinews.cn/': 6628,
		'http://lingshui.hinews.cn/': 6629,
		'http://changjiang.hinews.cn/': 6630,
		'http://baoting.hinews.cn/': 6631,
		'http://baisha.hinews.cn/': 6632,
		'http://qiongzhong.hinews.cn/': 6633,
		'http://yangpu.hinews.cn/': 6634,
		'http://www.hifarms.com.cn/': 6635,
	}

	deny_list = [r'/201[0-8]',
	             r'/200[0-9]',
	             r'/2019/0?[1-10]',
	             r'http://zhibo.hinews.cn/',
	             r'https://mp.weixin.qq.com/',
	             r'http://a.hinews.cn/',
	             r'hndaily.cn.*?/live/',
	             r'http://zhibo.hinews.cn/'
	             r'/index.shtml'
	             ]

	# http://www.hinews.cn/news/system/2019/11/04/032208722.shtml
	rules = (
		Rule(LinkExtractor(
			allow=r'hinews.cn/news/system/%s/.*?/\d+.shtml' % datetime.today().strftime('%Y/%m'), ),
			callback='parse_item',
			process_request=js_meta,
			follow=False),

		Rule(LinkExtractor(allow=r'hinews.cn.\S+\.shtml',
						   deny=deny_list),
			process_request=otherurl_meta,
			follow=False)
	)

	# http://www.hinews.cn/news/system/2019/10/31/032206495.shtml

	downloader_middlewares = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
	downloader_middlewares['scrapy.downloadermiddlewares.useragent.UserAgentMiddleware'] = None
	downloader_middlewares['news_all.middlewares.UserAgentMiddleware'] = 20
	downloader_middlewares['news_all.middlewares.PhantomJSMiddleware'] = 540

	custom_settings = {
		'DEPTH_LIMIT': 3,
		'DOWNLOADER_MIDDLEWARES': downloader_middlewares
		# {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
		# 	'news_all.middlewares.UserAgentMiddleware': 20,
		# 	'news_all.middlewares.PhantomJSMiddleware': 540, }
	}

	start_meta = {'jstype': True}

	"""
	"""
	"""
	class functions begin
	"""
	"""
	"""

	def parse_item(self, response):
		xp = response.xpath
		# http://www.hinews.cn/news/system/2019/10/31/032206482.shtml
		try:
			title = xp('.//h2/text()').extract_first()
			if not title:
				title = xp(".//h2[@class='f24 tac fwb page_h2   mt56 mb20']/text()").extract_first()
			# title = xp('//*[@id="xw_biaot"]').extract_first()
			# if not title:
			# 	title = self.get_page_title(response)
			pub_time = xp('.//li[@class="f14"]').re(r'\d{4}-\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}')[0]
			origin_name = xp('.//li[@class="f14"]/a/text()').extract()[0]
			content_div = xp('.//*[@id="bs_content"]')[0]
			content, media, videos, _ = self.content_clean(
				content_div,
				kill_xpaths=['.//div[@class="bshare-custom left mb0"]',
							 './/div[@class="f16 fl"]']
			)

		except Exception as e:
			return self.parse_item2(response)

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media,
			videos=videos
		)

	def parse_item2(self, response):
		xp = response.xpath
		# http://www.hinews.cn/news/system/2019/10/31/032206482.shtml
		try:
			title = xp('//*[@id="xw_biaot"]/text()').extract_first()
			if not title:
				title = self.get_page_title(response)
			pub_time = xp('.//li[@class="f14"]').re(r'\d{4}-\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}')[0]
			origin_name = xp('.//li[@class="f14"]/a/text()').extract()[0]
			content_div = xp('.//*[@id="bs_content"]')[0]
			content, media, videos, _ = self.content_clean(
				content_div,
				kill_xpaths=['.//div[@class="bshare-custom left mb0"]',
							 './/div[@class="f16 fl"]',
							 './/div[@class="bdsharebuttonbox bdshare-button-style0-32"]']
			)

		except Exception as e:
			print("error at parse_item() when parsing %s" % response.url)
			print(e)
			return

		return self.produce_item(
			response=response,
			title=title,
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media
		)
