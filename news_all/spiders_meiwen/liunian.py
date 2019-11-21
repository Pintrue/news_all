# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
import re


# 好多内容都不是短句，而是新闻
class liunianspider(NewsRCSpider):
    name = 'liunian'
    mystart_urls = {'https://www.8888ln.com/': 2426,  # 网站-商业网站-流年文学-首页
                    'https://www.8888ln.com/suibi/': 2428,  # 网站-商业网站-流年文学-随笔
                    'https://www.8888ln.com/Joke/': 2430,  # 网站-商业网站-流年文学-笑话
                    'https://www.8888ln.com/sanwen/': 2432,  # 网站-商业网站-流年文学-散文
                    'https://www.8888ln.com/classic/': 2433,  # 网站-商业网站-流年文学-美文
                    'https://www.8888ln.com/lizhi/': 2435,  # 网站-商业网站-流年文学-励志
                    'https://www.8888ln.com/zheli/': 2437,  # 网站-商业网站-流年文学-哲理
                    'https://www.8888ln.com/love/': 2439,  # 网站-商业网站-流年文学-爱情
                    'https://www.8888ln.com/diary/': 2441,  # 网站-商业网站-流年文学-日记
                    'https://www.8888ln.com/shanggan/': 2443,  # 网站-商业网站-流年文学-伤感
                    'https://www.8888ln.com/zuowen/': 2445,  # 网站-商业网站-流年文学-作文
                    }
    
    rules = (
        Rule(LinkExtractor(allow=(r'8888ln.com/.*?/.*?/\d+.html'), deny=[]),
             callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        try:
            xp = response.xpath
            title = xp('//div[@class="con-tit"]/h1/text()').extract_first() or self.get_page_title(response)
            # pubtime = xp('//div[@class="con-tit"]/p/text()').extract()[0] # 时间:2019-04-10 19:36 来源:散文网(8888ln.com) 作者:1900  阅读:
            # pubtime = pubtime[3:19]
            
            origin_name = ""
            og = xp('//div[@class="con-tit"]/p/text()').extract_first('')
            ogg = re.search('作者:(.*?)阅读', og)
            if ogg:
                origin_name = ogg.group(1)
            
            cv = xp("//tbody")[0]
            content, media, _, _ = self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=datetime.now(),
            origin_name=origin_name,
            content=content,
            media=media,
        )
