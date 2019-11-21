# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider
from scrapy.conf import settings
from news_all.tools.time_translater import Pubtime


class PeopleSpider(NewsRCSpider):
    name = 'people'
    mystart_urls = {"http://www.people.com.cn/GB/59476/": 159,  # "要闻",
                    "http://politics.people.com.cn/": 160,  # "时政",
                    "http://opinion.people.com.cn/": 161,  # "观点",
                    "http://world.people.com.cn/": 162,  # "国际",
                    "http://tw.people.com.cn/": 163,  # "台湾",
                    "http://leaders.people.com.cn/": 164,  # "领导",
                    }
    rules = (
        Rule(LinkExtractor(allow=r'people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        # http://sd.people.com.cn/n2/2019/0211/c364532-32624121.html
        try:
            title_div = response.xpath('//div[contains(@class,"text_title")]')[0]
            content_div = response.xpath('//div[@id="rwb_zw" or @class="box_con"]')[0]
            source_div = title_div.xpath('./div/div')[0]
            pubtime = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}')[0]
        except:
            return self.parse_item2(response)

        title = self.get_full_title(title_div, response)
        origin_name = source_div.xpath('./a/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//*[contains(text(),"相关新闻")]/ancestor::p',
            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(response=response,  # 一定要写response=response, 不能是response
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,
                                 media=media,
                                 )
    
    def get_full_title(self, title_div, response):
        # 新闻标题  副标题本身以"——"开头的直接把主副标题连起来, 否则主+"——"+副
        # pre_title = ''.join(i.strip() for i in title_div.xpath('.//*[contains(@class,"pre")]/text()').extract())
        # http://dangjian.people.com.cn/n1/2019/0211/c117092-30617896.html 标题内如有<br>等html标签都删除只保留text拼接
        title = ''.join(i.strip() for i in title_div.xpath('.//h1/text()').extract())
        sub_title = ''.join(i.strip() for i in title_div.xpath('.//h2/text()').extract() or title_div.xpath(
            './/*[contains(@class,"sub")]/text()').extract())
        return join_titles(title, sub_title)
    
    def parse_item2(self, response):
        # http://politics.people.com.cn/n1/2019/0202/c1024-30608743.html
        try:
            title_div = response.xpath('//div[contains(@class,"title")]')[0]
            news_div = response.xpath('//*[@id="picG"]')[0]
            source_div = news_div.xpath('.//*[contains(text(), "来源：")]')[0]
            source_text = source_div.xpath('.//text()').extract()
            pubtime = source_text[2].replace('\n', '').strip()
            origin_name = source_text[1]
            d_pres = source_div.xpath('./preceding-sibling::*').extract()  # source_div的前兄弟节点
            content_div = Selector(text=''.join(d_pres))
        except:
            return self.parse_item3(response)

        title = self.get_full_title(title_div, response)
        
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//*[contains(text(),"相关新闻")]/ancestor::p',
            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,

                                 media=media,
                                 )
    
    def parse_item3(self, response):
        # http://society.people.com.cn/n1/2019/0202/c1008-30608898.html
        try:
            content_div = response.xpath('.//div[@class="pic"]')[0]
            title_div = response.xpath('//h1')[0]
            source_div = response.xpath('.//*[contains(text(), "来源：")]')[0]
            source_text = source_div.xpath('.//text()').extract()
            origin_name = source_text[1].replace('\n', '').replace("来源：", "").strip()
            pubtime = source_text[0].replace('\n', '').replace("来源：", "").strip()

        except:
            return self.parse_item4(response)

        title = ''.join(i.strip() for i in title_div.xpath('./text()').extract())
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//*[contains(text(),"相关新闻")]/ancestor::p',
            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,

                                 media=media,
                                 )
    
    def parse_item4(self, response):
        # http://cpc.people.com.cn/n1/2019/0115/c64094-30544006.html
        # http://cpc.people.com.cn/n1/2019/0211/c419242-30616430.html
        try:
            news_div = response.xpath('.//div[@class="text_c"]')[0]
            tail_div = news_div.xpath('.//div[contains(text(), "责编：")]')[0]
            content_div = response.xpath('.//div[@class="show_text"]')[0]
        except:
            return self.parse_item5(response)
        
        pubtime = news_div.xpath('.//*[@id="p_publishtime"]/text()').extract_first('')
        try:
            origin_name = news_div.xpath('.//*[@id="p_origin"]//text()').extract()[1]
        except:
            # http://renshi.people.com.cn/n1/2019/0211/c139617-30616673.html
            try:
                e = news_div.xpath('.//p[@class="sou"]//text()').extract()
                pubtime = e[0].replace("来源：", "").strip()
                origin_name = e[1]
            except:
                return self.parse_item5(response)

        title = self.get_full_title(news_div, response)
        
        content = content_div.extract()
        if "责编：" not in content:
            content += tail_div.extract()
        content, media, videos, video_cover = self.content_clean(content, kill_xpaths=[
            '//*[contains(text(),"相关新闻")]/ancestor::p',
            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,

                                 media=media,
                                 )
    
    def parse_item5(self, response):
        # http://health.people.com.cn/n1/2019/0212/c14739-30623757.html
        xp = response.xpath
        try:
            news_div = xp('//div[@class="articleCont"]')[0]
            tdiv = news_div.xpath('.//div[@class="title"]')[0]
            stexts = news_div.xpath('.//div[@class="artOri"].//text()').extract()
            pubtime = stexts[0].replace("来源：", "").strip()
            origin_name = stexts[1]
            content_div = news_div.xpath('.//div[@class="artDet"]')[0]
            tail_div = news_div.xpath('.//div[contains(text(), "责编：")]')[0]
        except:
            return self.parse_item6(response)

        title = tdiv.xpath('.//h2/text()').extract_first('').strip()
        sub_title = tdiv.xpath('.//h3/text()').extract_first('').strip()
        title = join_titles(title, sub_title)
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//*[contains(text(),"相关新闻")]/ancestor::p',
                                                                            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        if "责编：" not in content:
            content += tail_div.extract()
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
    
    def parse_item6(self, response):
        # http://capital.people.com.cn/n1/2019/0212/c405954-30623650.html
        xp = response.xpath
        try:
            content_div = xp('.//div[@class="gray box_text"]')[0]
            tail_div = xp('.//div[contains(text(), "责编：")]')[0]
            stexts = xp('.//*[contains(text(),"来源：")]//text()').extract()
            pubtime = stexts[0].replace("来源：", "").strip()
            origin_name = stexts[1]
        except:
            return self.parse_item_7(response)

        title = xp('.//h1/text()').extract_first('').strip()
        sub_title = xp('.//h4/text()').extract_first('').strip()
        title = join_titles(title, sub_title)
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//*[contains(text(),"相关新闻")]/ancestor::p',
                                                                            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        if "责编：" not in content:
            content += tail_div.extract()
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
    
    def parse_item_7(self, response):
        # /div[@class='w1000 txtCon clearfix']  http://cpc.people.com.cn/n1/2019/0710/c64094-31224028.html
        xp = response.xpath
        try:
            pubtime = Pubtime(xp('//div[@class="editor time1 clearfix"]/text()')[0].extract())
            content_div = xp('//div[@class="w1000 txtCon clearfix"]')[0]
            # <meta name="source" content="来源：人民日报" class="">
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract()
        except:
            return self.parse_images(response)
            
        title = xp('.//h1/text()').extract_first('').strip()
        sub_title = xp('.//h4/text()').extract_first('').strip()
        title = join_titles(title, sub_title)
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//div[@class="editor time1 clearfix"]/preceding::*',
                                                                            '//div[@class="editor time1 clearfix"]',
                                                                            '//*[contains(text(),"相关新闻")]/ancestor::p',
                                                                            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,

            media=media,
        )
    
    def parse_images(self, response):
        # http://cpc.people.com.cn/xuexi/n1/2019/0416/c385474-31032594.html
        
        xp = response.xpath
        try:
            pubtime = xp('//*[@id="picG"]/div[@class="page_c"]/div[@class="fr"]/text()').extract()[1].strip()
            content_div = xp('//div[@id="picG"]')[0]
            # http://tw.people.com.cn/n1/2019/0423/c14657-31045392.html 还要加文字正文
            content = content_div.extract() + xp(r'//div[@class="content clear clearfix"]').extract_first('')
            origin_name = xp('//head/meta[@name="source"]/@content')[0].extract().replace("原创稿", "")
        except:
            return self.produce_debugitem(response, "xpath error")
        
        next_a = xp('//div[@class="page_c"]//a[@id="next"]')
        if next_a and not next_a.re(r'javascript:showAd'):
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'origin_name': origin_name,
                                         'content': content,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        
        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=['//div[@class="page_c"]',
                                                                              r'//div[@class="edit clearfix"]'])
        
        return self.produce_item(
            response=response,
            title=xp('.//h1').extract(),
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
    
    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp('//div[@id="picG"]')[0]
            meta_new['content'] += content_div.extract() + xp(r'//div[@class="content clear clearfix"]').extract_first(
                '')
        except:
            return self.produce_debugitem(response, 'xpath error')
        
        # <a href="javascript:showAd('http://www.people.com.cn/NMediaFile/2019/0401/MAIN201904011405000414124240534.jpg', '/xuexi/n1/2019/0401/c385474-31006833.html', '/xuexi/n1/2019/0416/c385474-31032594.html', '高清图集：习近平三月精彩镜头全纪录','http://wow.people.com.cn/');" id="next" style="display: none;" class="xh-highlight">下一页</a>
        next_a = xp('//div[@class="page_c"]//a[@id="next"]')
        if next_a and not next_a.re(r'javascript:showAd'):
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths=['//div[@class="page_c"]',
                                                                              r'//div[@class="edit clearfix"]'])
        
        return self.produce_item(
            response=response,
            title=xp('.//h1').extract_first(''),
            pubtime=meta_new['pubtime'],
            origin_name=meta_new['origin_name'],
            content=content,
            media=media
        )


def join_titles(title, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title += sub_title
        else:
            title += "——" + sub_title
    return title
