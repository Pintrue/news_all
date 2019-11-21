# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRSpider
from urllib.request import urljoin
from news_all.tools.time_translater import timestamps


mystart_urls_base = {
	'http://www.budejie.com/': 3800,
	'http://www.budejie.com/pic/': 3801,
	# 'http://www.budejie.com/audio/': 3802,   # 不要音频
	'http://www.budejie.com/hot/': 3804,
}


class baisibudeSpider(NewsRSpider):
	"""百思不得姐"""
	name = 'baisibude'

	mystart_urls = {i+str(p): j for p in range(1, 51) for i, j in mystart_urls_base.items()}

	# http://www.budejie.com/detail-29714094.html
	rules = (Rule(LinkExtractor(allow=r'budejie.com/detail-\d+.html',
	                            ),
	              callback='parse',
	              follow=False),
	         )

	def parse(self, response):
		xp = response.xpath
		arts = xp("//div[@class='j-r-list']/ul/li/div[@class='j-r-list-c']")
		for i in arts:
			try:
				title = i.xpath("./div[@class='j-r-list-c-desc']/a/text()").extract_first('')

				news_url = urljoin(response.url, i.xpath("./div[@class='j-r-list-c-desc']/a/@href").extract_first(''))
				cv = i.xpath("./div[@class='j-r-list-c-img']/a/img")
				content, media, _, _ = self.content_clean(cv)
			except:
				yield self.produce_debugitem(response, "xpath error")
				continue
			yield self.produce_item(
				response=response,
				title=title,
				pubtime=timestamps(),
				content=content,
				media=media,
				srcLink=news_url
			)
