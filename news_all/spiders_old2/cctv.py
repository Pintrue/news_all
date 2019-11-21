#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:50
# @Author  : wjq
# @File    : cctv.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from scrapy import Request


def change_url(x):
	url = x.url
	url_2 = url.replace('shtml', 'xml')
	kwargs = {}
	for i in [
		'method', 'headers', 'body', 'cookies', 'meta', 'flags',
		'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
		kwargs.setdefault(i, getattr(x, i))
	r = Request(url_2, **kwargs)
	return r


class CctvSpider(NewsRCSpider):
	"""央视新闻"""  # todo 解析视频
	name = 'cctv'
	mystart_urls = {
		# 'http://sports.cctv.com/tabletennis/': 1200821,  # 央视新闻-乒乓-中间列表
		# 'http://sports.cctv.com/special/taiqiu/': 1200823,  # 央视新闻-台球-右侧列表采集
		# 'http://sports.cctv.com/volleyball/': 1200820,  # 央视新闻-排球-中间列表
		# 'http://sports.cctv.com/tennis/': 1200822,  # 央视新闻-网球-底部列表
		# 'http://sports.cctv.com/badminton/': 1200824,  # 央视新闻-羽毛球-中部列表
		# 'http://sports.cctv.com/football/index.shtml': 1200819,  # 央视新闻-足球-中部列表（视频）
		# 'http://news.cctv.com/china/': 1301654,  # 央视网

		'http://www.cctv.com/': 6201,   # 央视网 综合
		'http://news.cctv.com/china/?spm=C94212.P4YnMod9m2uD.0.0': 6202,   # 央视网 综合
		'http://news.cctv.com/world/?spm=C94212.PBZrLs0D62ld.0.0': 6203,   # 央视网 国际 国际要闻
		'http://news.cctv.com/society/?spm=C94212.PBi4fu284lJm.0.0': 6204,   # 央视网 社会
		'http://news.cctv.com/law/?spm=C94212.PnPr887gR6ub.0.0': 6205,   # 央视网 社会 社会与法
		'http://photo.cctv.com/': 6206,   # 央视网 综合
		'http://news.cctv.com/xwj/index.shtml?spm=C35449.P80754075394.EyslVJ3Wrhn0.1': 6207,   # 央视网 社会
		'http://news.cctv.com/special/zgmsjz/all/dggj/index.shtml?spm=C94212.PaUU9B5q1Dqd.S68239.3': 6208,   # 央视网 社会 正能量
		'http://news.cctv.com/special/zgmsjz/all/zmrw/index.shtml?spm=C94212.PVeEaLwzV3mn.S03443.4': 6209,   # 央视网 社会 正能量
		'http://news.cctv.com/special/zgmsjz/all/hyxf/index.shtml?spm=C94212.PyGKzHBuh04X.S22533.5': 6210,   # 央视网 社会 正能量
		'http://news.cctv.com/special/zgmsjz/all/junrenfc/index.shtml?spm=C94212.PaUU9B5q1Dqd.S68239.6': 6211,   # 央视网 军事 军事人物
		'http://news.cctv.com/special/zgmsjz/all/ddmf/index.shtml?spm=C94212.PwwyIuIodZjX.S90912.7': 6212,   # 央视网 社会 正能量
		'http://news.cctv.com/special/zgmsjz/all/cyym/index.shtml?spm=C94212.PA7MaagnotpZ.S62514.8': 6213,   # 央视网 财经 创业
		'http://news.cctv.com/special/zgmsjz/all/jrjx/index.shtml?spm=C94212.PM1HQG7ym9BB.S93551.9': 6214,   # 央视网 社会 正能量
		'http://news.cctv.com/ent/?spm=C94212.PZd4MuV7QTb5.0.0': 6215,   # 央视网 娱乐
		'http://news.cctv.com/yskp/index.shtml?spm=C35449.P80754075394.0.0': 6216,   # 央视网 时政 时事评论
		'http://news.cctv.com/lbj/index.shtml?spm=C35449.P80754075394.0.0&fdsf': 6217,   # 央视网 时政 领导人
		'http://news.cctv.com/xwj/index.shtml?spm=C35449.P80754075394.0.0': 6218,   # 央视网 时政
		'http://news.cctv.com/jianshi/?spm=C35449.P80754075394.0.0': 6219,   # 央视网 综合
		'http://news.cctv.com/kuaikan/index.shtml?spm=C35449.P80754075394.0.0': 6220,   # 央视网 综合
		'http://military.cctv.com/weihutang/index.shtml?spm=C35449.P80754075394.0.0': 6221,   # 央视网 军事
		'http://news.cctv.com/yuanchuang/?spm=C35449.P80754075394.0.0': 6222,   # 央视网 社会
		'http://news.cntv.cn/xwlm/gundongye/quanbu/index.shtml': 6223,   # 央视网 综合
		'http://news.cctv.com/tech/?spm=C94212.Pz2YdsvQ9WpW.0.0': 6224,   # 央视网 科技
		'http://news.cctv.com/life/?spm=C94212.PGZDd8bkBJCZ.0.0': 6225,   # 央视网 生活
		'http://people.cctv.com/?spm=C38482.PEbwoCRG76wM.0.0': 6226,   # 央视网 社会 正能量
		'http://military.cctv.com/?spm=C94212.P1U6CL9BCSrI.0.0': 6227,   # 央视网 军事
		'http://jingji.cctv.com/?spm=C94212.P1U6CL9BCSrI.0.0': 6230,   # 央视网 财经 财经要闻
		'http://jingji.cctv.com/caijing/index.shtml?spm=C87458.PxZ1sQfyXDLK.0.0': 6231,   # 央视网 财经 财经要闻
		'http://jingji.cctv.com/shiping/index.shtml?spm=C87458.PxZ1sQfyXDLK.0.0': 6233,   # 央视网 财经 财经要闻
		'http://arts.cctv.com/zx/yishuqianyan/?spm=C58899.P85179810662.E07884162877.1': 6239,   # 央视网 文化艺术
		'http://arts.cctv.com/comment/index.shtml?spm=C58899.P20645494841.S30776.4': 6240,   # 央视网 文化艺术
		'http://arts.cctv.com/kz/dt/?spm=C58899.PfWkdMWHc9n8.S30776.6': 6242,   # 央视网 文化艺术
		'http://news.cctv.com/edu/?spm=C94212.P4YnMod9m2uD.0.0': 6245,   # 央视网 教育
		'http://opinion.cctv.com/yangshiwangping/plist/index.shtml?spm=C88965.P72990804435.0.0': 6251,   # 央视网 时政 时事评论
		'http://news.cctv.com/yuanchuang/?spm=C88965.P72990804435.0.0': 6252,   # 央视网 社会
		'http://sannong.cctv.com/xinwen/?spm=C73274.P13518688384.E05854535243.2': 6255,   # 央视网 三农
		'http://sannong.cctv.com/xinwen/video/?spm=C73274.P52232081160.E05854535243.3': 6260,   # 央视网 三农 农业
		'http://sannong.cctv.com/nyjm/index.shtml?spm=C73274.PuKKZoK5oJB0.E05854535243.4': 6264,   # 央视网 三农 农业
		'http://sannong.cctv.com/xinwen/fdxnr/index.shtml?spm=C73274.P13518688384.EeRPlj3T5WqD.1': 6268,   # 央视网 三农
		'http://sannong.cctv.com/xinwen/fpjp/index.shtml?spm=C73274.P13518688384.EGZTVPPk6UiP.1': 6269,   # 央视网 三农 农村扶贫
		'http://sannong.cctv.com/xinwen/xczxxd/index.shtml?spm=C73274.P13518688384.Eqsw8mGCvcrj.1': 6271,   # 央视网 三农 农村扶贫
		'http://jiankang.cctv.com/zixun/index.shtml?spm=C88180.P76914399832.0.0': 6274,   # 央视网 健康
		'http://tv.cctv.com/lm/jkzl/?spm=C88180.P76914399832.0.0': 6275,   # 央视网 健康
		'http://tv.cctv.com/lm/shq/index.shtml?spm=C88180.P76914399832.0.0': 6277,   # 央视网 生活
		'http://tv.cctv.com/lm/renkou/?spm=C88180.P76914399832.0.0': 6279,   # 央视网 健康
		'http://tv.cctv.com/lm/zhyy/?spm=C88180.P76914399832.0.0': 6280,   # 央视网 健康 中医
		'http://jiankang.cctv.com/special/jkdjt/index.shtml?spm=C88180.P76914399832.0.0': 6281,   # 央视网 健康 健康知识
		'http://jiankang.cctv.com/hjk/index.shtml?spm=C88180.P76914399832.Elt82zheBhmd.1': 6282,   # 央视网 健康 健康知识
		'http://jiankang.cctv.com/shenghuo/index.shtml?spm=C88180.P76914399832.S25139.2': 6284,   # 央视网 健康 健康知识
		'http://jingji.cctv.com/?spm=C96370.PsikHJQ1ICOX.EutgeoL1Nnqo.5': 6297,   # 央视网 财经
		'http://jingji.cctv.com/shiping/index.shtml?spm=C87458.PxZ1sQfyXDLK.EKsr0qoCcScj.1': 6298,   # 央视网 财经 财经要闻
		'http://sports.cctv.com/?spm=C96370.PsikHJQ1ICOX.EutgeoL1Nnqo.7': 6301,   # 央视网 体育
		'http://sports.cctv.com/basketball/index.shtml?spm=C73465.PhvcG4VlqNFF.EoW8Ji0KUiOe.2': 6304,   # 央视网 体育 篮球
		'http://sports.cctv.com/special/international/video/index.shtml?spm=C73465.P75120774569.E26218772690.1': 6305,   # 央视网 体育 足球
		'http://sports.cctv.com/special/international/?spm=C73465.PhvcG4VlqNFF.EoW8Ji0KUiOe.3': 6306,   # 央视网 体育 足球
		'http://sports.cctv.com/special/teamchina/videos/index.shtml?spm=C73465.P15458795537.68152997534.2': 6307,   # 央视网 体育 足球
		'http://sports.cctv.com/special/teamchina/news/index.shtml?spm=C73465.P15458795537.S66857.1': 6308,   # 央视网 体育 足球
		'http://sports.cctv.com/special/teamchina/?spm=C73465.PhvcG4VlqNFF.EoW8Ji0KUiOe.4': 6309,   # 央视网 体育 足球
		'http://sports.cctv.com/csl/?spm=C73465.PhvcG4VlqNFF.EyAwthc54FQC.7': 6310,   # 央视网 体育 足球 中超
		'http://sports.cctv.com/special/premierleague/?spm=C73465.PhvcG4VlqNFF.EyAwthc54FQC.8': 6311,   # 央视网 体育 足球 英超
		'http://sports.cctv.com/special/seriea/?spm=C73465.PhvcG4VlqNFF.EyAwthc54FQC.9': 6312,   # 央视网 体育 足球 意甲
		'http://sports.cctv.com/jyh/CHINA/index.shtml?spm=C73465.PybaeBymEc4f.Ew2DwE2qmfTN.1': 6313,   # 央视网 体育 体育赛事
		'http://sports.cctv.com/jyh/news/index.shtml?spm=C73465.PybaeBymEc4f.EWDVuGgUudMe.1': 6314,   # 央视网 体育 体育赛事
		'http://sports.cctv.com/jyh/others/index.shtml?spm=C73465.PybaeBymEc4f.EUFlh85Ej3VR.1': 6315,   # 央视网 体育 体育赛事
		'http://sports.cctv.com/jyh/torch/index.shtml?spm=C73465.PybaeBymEc4f.EFDtYEfMfxON.1': 6316,   # 央视网 体育
		'http://sports.cctv.com/cba/news/index.shtml?spm=C73465.P35472125375.EvHUNGDlCmXx.8': 6317,   # 央视网 体育 篮球 CBA
		'http://sports.cctv.com/cba/?spm=C73465.PhvcG4VlqNFF.EyAwthc54FQC.10': 6318,   # 央视网 体育 篮球 CBA
		'http://sports.cctv.com/young/?spm=C73465.PhvcG4VlqNFF.EyAwthc54FQC.13': 6319,   # 央视网 体育
		'http://military.cctv.com/index.shtml?spm=C96370.PsikHJQ1ICOX.EutgeoL1Nnqo.8': 6320,   # 央视网 军事
		'http://news.cctv.com/lbj/index.shtml?spm=C96370.PsikHJQ1ICOX.EQcxcebtkFyF.2': 6321,   # 央视网 时政 领导人
	}

	rules = (
		# http://sports.cctv.com/2019/06/19/PHOAtIFO0FaniD2oG60qwmMw190619.shtml
		Rule(LinkExtractor(allow=(r'cctv.com/%s/\d{2}/PHOA\w+.shtml' % datetime.today().strftime('%Y/%m'),),),
							callback='parse_images', follow=False, process_request=change_url),
		# http://tv.cctv.com/2019/06/25/VIDEJXsmpvEhNosp86Pw9aTl190625.shtml
		# http://sports.cctv.com/2019/06/24/ARTIESAo3nT7wOWP60Y8Qiul190624.shtml
		# http://sports.cctv.com/2019/06/17/ARTIOgEeJz9aVY9UlQCyCGQr190617.shtml
		Rule(LinkExtractor(allow=(r'cctv.com/%s/\d{2}/\w+.shtml' % datetime.today().strftime('%Y/%m'),),
							deny=(r'tv.cctv.com/', r'/VIDE\w+.s?htm')  # 排除视频
							),
							callback='parse_item', follow=False),
		Rule(LinkExtractor(allow=(r'cctv.com/.*?\d+.s?htm',),
							deny=(r'/201[0-8]', r'/2019/0[1-9]', r'tv.cctv.com/', r'/VIDE\w+.s?htm')
							),
							process_request=otherurl_meta, follow=False),
	)

	# http://219.144.72.56/vod.cntv.lxdns.com/flash/mp4video62/TMS/2019/06/25/4024ffc4dc0b4843b3dbfcd320f20df6_h264818000nero_aac32.mp4
	# http://219.144.72.56/vod.cntv.lxdns.com/flash/mp4video62/TMS/2019/06/25/4024ffc4dc0b4843b3dbfcd320f20df6_h264818000nero_aac32.mp4?wshc_tag=0&wsts_tag=5d11f11a&wsid_tag=7c7f6882&wsiphost=ipdbm
	def parse_item(self, response):
		xp = response.xpath
		try:
			if xp('//div[@id="myFlash"] | //div[@class="showBox"] | //span[@id="myFlash"]'):  # 排除视频
				return
			sdiv = xp(r'//span[@class="info"]')[0]
			# 2019年06月25日 15:02
			pubtime = sdiv.re(r'\d{4}年\d{2}月\d{2}日(?: \d{2}:\d{2})?') or sdiv.re(r'\d{4}年\d{2}月\d{2}日(\d{2}:\d{2})?')
			if not pubtime:
				pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2}')
			# if not pubtime:
			# 	pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2}(\s\d{2}[：:]\d{2}[：:]\d{2})*')
			pubtime = pubtime[0]

			# http://sports.cctv.com/2019/11/01/ARTIAXN10tvsndQHtOccdNeC191101.shtml
			content_div = xp('//div[@class="cnt_bd"]/p')[0]
			content, media, _, _ = self.content_clean(content_div)

			origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
		except Exception as e:
			return self.parse_item2(response)

		return self.produce_item(
			response=response,
			title=xp("//h1/text()").extract_first("") or self.get_page_title(response).split('-')[0],
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media
		)

	def parse_item2(self, response):
		# http://sports.cctv.com/2019/11/02/ARTIihPtr0vAFYrI7TNjgS9U191102.shtml
		xp = response.xpath
		try:
			if xp('//div[@id="myFlash"] | //div[@class="showBox"] | //span[@id="myFlash"]'):  # 排除视频
				return
			sdiv = xp(r'//div[@class="info"] | //span[@class="info"]')[0]
			# 2019年06月25日 15:02
			pubtime = sdiv.re(r'\d{4}年\d{2}月\d{2}日(?: \d{2}:\d{2})?')
			if not pubtime:
				pubtime = sdiv.re(r'\d{4}[年-]\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}') or sdiv.re(r'\d{4}-\d{2}-\d{2}')
			pubtime = pubtime[0]

			content_div = xp('//div[@id="content_area"]/p')[0]
			content, media, _, _ = self.content_clean(content_div)

			origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
		except Exception as e:
			return self.parse_item3(response)

		return self.produce_item(
			response=response,
			title=xp("//h1/text()").extract_first("") or self.get_page_title(response).split('-')[0],
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media
		)

	def parse_item3(self, response):
		xp = response.xpath
		try:
			if xp('//div[@id="myFlash"] | //div[@class="showBox"] | //span[@id="myFlash"]'):  # 排除视频
				return
			sdiv = xp(r'//div[@class="info"] | //span[@class="info"]')[0]
			# 2019年06月25日 15:02
			pubtime = sdiv.re(r'\d{4}年\d{2}月\d{2}日(?: \d{2}:\d{2})?')
			if not pubtime:
				pubtime = sdiv.re(r'\d{4}[年-]\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}') or sdiv.re(r'\d{4}-\d{2}-\d{2}')
			pubtime = pubtime[0]

			content_div = xp('//div[@id="text_area"]')[0]
			content, media, _, _ = self.content_clean(content_div)

			origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
		except Exception as e:
			return self.parse_item4(response)
			# return self.produce_debugitem(response, "xpath error")

		return self.produce_item(
			response=response,
			title=xp('normalize-space(//*[@id="title_area"]/h1)').extract_first() or self.get_page_title(response).split('-')[0],
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media
		)

	def parse_item4(self, response):
		# http://opinion.cctv.com/2019/11/01/ARTIjTiEVEavN7aDzGO5yMvp191101.shtml
		xp = response.xpath
		try:
			if xp('//div[@id="myFlash"] | //div[@class="showBox"] | //span[@id="myFlash"]'):  # 排除视频
				return
			sdiv = xp(r'.//div[@class="bd"] | //div[@class="info"] | //span[@class="info"]')[0]
			pubtime = sdiv.re(r'\d{4}年\d{2}月\d{2}日(?: \d{2}:\d{2})?')
			if not pubtime:
				pubtime = sdiv.re(r'\d{4}[年-]\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}') or sdiv.re(r'\d{4}-\d{2}-\d{2}')
			pubtime = pubtime[0]

			content_div = xp(r'//*[@id="page_body"]/div[2]/div[1]/div[3]/div')
			content, media, _, _ = self.content_clean(content_div)

			origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
		except Exception as e:
			return self.produce_debugitem(response, "xpath error")

		return self.produce_item(
			response=response,
			title=xp("//h1/text()").extract_first("") or self.get_page_title(response).split('-')[0],
			pubtime=pubtime,
			origin_name=origin_name,
			content=content,
			media=media
		)

	def parse_item5(self, response):
		# http://news.cctv.com/2019/11/01/ARTIU1MfRogWK8l2fuMGRNHp191101.shtml
		xp = response.xpath
		try:
			if xp('//div[@id="myFlash"] | //div[@class="showBox"] | //span[@id="myFlash"]'):  # 排除视频
				return

			source_div = xp('//div[@class="biref"]/span/text()')
			origin_name = source_div.re(r'(.*?)\s*发布时间：')
			pub_time = source_div.re(r'\d{4}年\d{2}月\d{2}日(?: \d{2}:\d{2})?')
			if not pub_time:
				pub_time = source_div.re(r'\d{4}[年-]\d{2}-\d{2}\s\d{2}[：:]\d{2}[：:]\d{2}') or source_div.re(r'\d{4}-\d{2}-\d{2}')
			pub_time = pub_time[0]

			content_div = xp(r'div[@class ="cont"]/p')[0]
			content, media, _, _ = self.content_clean(content_div)

		except Exception as e:
			return self.produce_debugitem(response, "xpath error")

		return self.produce_item(
			response=response,
			title=xp("//h1/text()").extract_first("") or self.get_page_title(response).split('-')[0],
			pubtime=pub_time,
			origin_name=origin_name,
			content=content,
			media=media
		)

	def parse_images(self, response):
		# http://sports.cctv.com/2019/06/19/PHOAtIFO0FaniD2oG60qwmMw190619.shtml
		# http://sports.cctv.com/2019/06/19/PHOAtIFO0FaniD2oG60qwmMw190619.xml?randomNum=0.45162289460084803

		xp = response.xpath
		try:
			lis = xp('//ul/li')
			pubtime = lis[0].xpath('@time').extract_first('')
			media = {"images": {}}
			content = ""
			for i, j in enumerate(lis):
				idx = str(i + 1)
				media["images"][idx] = {"src": j.xpath('@photourl').extract_first("")}
				content += '<p>${{%s}}$</p>' % idx + '<p>' + j.xpath('@title').extract_first("") + '</p>'
		except Exception as e:
			return self.produce_debugitem(response, "xpath error")

		return self.produce_item(
			response=response,
			title=xp('//ul/@title').extract_first('').replace('[高清组图]', ''),
			pubtime=pubtime,
			origin_name="央视网",
			content=content,
			media=media
		)
