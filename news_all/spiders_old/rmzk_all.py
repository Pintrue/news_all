# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider

y, m, d = datetime.today().strftime('%Y-%m-%d').split('-')


class Rmzk_allSpider(NewsRCSpider):
    """人民周刊"""
    name = 'rmzk'
    mystart_urls = {
        'http://www.peoplenews.com.cn/html/gongyoulanmu/leyou/': 1301035,  # 人民周刊 乐游
        'http://www.peoplenews.com.cn/html/gongyoulanmu/wenshi/': 1301034,  # 人民周刊 文史-左侧列表
        'http://www.peoplenews.com.cn/html/gongyoulanmu/shizheng/': 1301030,  # 人民周刊 时政-首屏左侧
        'http://www.peoplenews.com.cn/html/gongyoulanmu/kexue/': 1301033,  # 人民周刊 科学-左侧列表
        'http://www.peoplenews.com.cn/html/gongyoulanmu/caijing/': 1301031,  # 人民周刊 经济-左侧列表
        'http://www.peoplenews.com.cn/html/gongyoulanmu/shixiang/': 1301032,  # 人民周刊-世相

    }
    rules = (
        #http://www.peopleweekly.cn/html/2019/leyou_0612/15455.html
        #http://www.peopleweekly.cn/html/2019/wenshi_0612/15460.html
        #http://www.peopleweekly.cn/html/2019/shizheng_0611/15407.html
        #http://www.peopleweekly.cn/html/2019/kexue_0611/15405.html
        #http://www.peopleweekly.cn/html/2019/shixiang_0515/14476.html
        # http://www.peopleweekly.cn/html/2019/shixiang_0515/14476.html
        Rule(LinkExtractor(allow=(r'peopleweekly.cn/html/%s/\w+_%s\d{2}/\d+.html'%(y, m)),
                           deny=r'/html/\d{4}/shipin_'), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract_first() or self.get_page_title(response).split('-')[0]
            content_div = xp("//div[@class='content']")[0]
            pubtime = xp("//div[@class='rexw-ly']").re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')[0]

            
            
            origin_name =xp('//div[@class="rexw-ly"]/p/span/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )