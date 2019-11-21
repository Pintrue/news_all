# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider

# 好多内容都不是短句，而是新闻
class xin022spider(NewsRCSpider):
    name = 'xin022'
    mystart_urls = {
                    'http://www.xin022.com/jingdianyulu/':2135,    #网站-商业网站-新022网-首页-语录
                    'http://www.xin022.com/html/mrmy/mrmy.html':2139,    #网站-商业网站-新022网-首页-名言
                    'http://www.xin022.com/gexingqianming/':2141,    #网站-商业网站-新022网-首页-签名
                    'http://www.xin022.com/shujizaicao/':2145,    #网站-商业网站-新022网-首页-书籍
                    'http://www.xin022.com/jingdiantaici/':2316,    #网站-商业网站-新022网-首页-经典台词
                    'http://www.xin022.com/renshengganwu/':2367,    #网站-商业网站-新022网-首页-人生感悟
                    'http://www.xin022.com/fanwendaquan/':2368,    #网站-商业网站-新022网-首页-范文大全
                    'http://www.xin022.com/haowenhaoju/':2370,    #网站-商业网站-新022网-首页-好文好句
                    'http://www.xin022.com/shicimingju/':2373,    #网站-商业网站-新022网-首页-诗词名句
                    'http://www.xin022.com/youxiuzuowen/':2374,    #网站-商业网站-新022网-首页-优秀作文
                    'http://www.xin022.com/mingrenmingyan/':2375,    #网站-商业网站-新022网-名人名言
                    # 'http://www.xin022.com/gexingqianming/':2376,    #网站-商业网站-新022网-个性签名
                    'http://www.xin022.com/jingdianmingyan/':2377,    #网站-商业网站-新022网-经典名言
                    # 'http://www.xin022.com/shicimingju/':2378,    #网站-商业网站-新022网-诗句名言
                    'http://www.xin022.com/baikezhishi/':2379,    #网站-商业网站-新022网-百科知识
                    'http://www.xin022.com/qqwangming/':2380,    #网站-商业网站-新022网-QQ网名
                    #http://www.xin022.com/QQtouxiang/':2381,     #网站-商业网站-新022网-QQ头像  #全是头像，应该没有爬取的价值
                    'http://www.xin022.com/zhishixuexi/':2382,    #网站-商业网站-新022网-知识学习
                    'http://www.xin022.com/pingguoshiwan/':2383,    #网站-商业网站-新022网-苹果试玩
                    # 'http://www.xin022.com/jingdianyulu/':2385,    #网站-商业网站-新022网-经典语录
                    # 'http://www.xin022.com/shujizaicao/':2387,    #网站-商业网站-新022网-书籍摘抄
    }


    rules = (
        Rule(LinkExtractor(allow=(r'xin022.com/.*?/\d+.html'),deny=r'666n.com/html'),
        callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'xin022.com/.*?/.*?/\d+.html'),deny=r'666n.com/html'),
        callback='parse_item', follow=False),
    )
    def parse_item(self,response):
        try:
            xp = response.xpath
            try:
                title = xp('//div[@class="title"]/h1/text()').extract_first() or self.get_page_title(response).split('-')[0]
                # pubtime = xp('//div[@class="info"]/text()').extract()[0]
                # pubtime = pubtime[3:22]
                cv = xp("//div[@class='content']")[0]
                content,media,_,_=self.content_clean(cv)
            except:
                title = xp('//div[@class="title"]/h2/text()').extract_first() or self.get_page_title(response).split('-')[0]
                # pubtime = xp('//div[@class="info"]/text()').extract()[0]
                # pubtime = pubtime[9:22].replace('年','-').replace('月','-').replace('日','').replace('\u3000','')
                cv = xp("//div[@class='content']")[0]
                content,media,_,_=self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media,
        )
