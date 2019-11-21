# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.html_clean import NewsBaseParser, img_fn
from news_all.spider_models import NewsRCSpider


img_pattern = re.compile(r'<img.*?(?:data-original|src)=[\',"](.*?)[\',"].*?>')  # 第一张图不是懒加载 后面的图是懒加载, 所以不能用


class HuanghexinwenParser(NewsBaseParser):
    """黄河新闻网清洗类  图片链接获取data-original"""
    
    def image_clean(self, content, img_re=None):
        fr = re.finditer(img_pattern, content)
        media = {}
        new_content = ''
        
        for i, j in enumerate(fr):
            media.setdefault("images", {})
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '<p>${{%s}}$</p>' % (i + 1)
            content = content[end:]
            img_url = j.group(1)
            if '/lazyload' in img_url:
                img_url = re.search('data-original=[\',"](.*?)[\',"]', j.group()).group(1)
            media['images'][str(i + 1)] = {"src": img_fn(img_url)}
        
        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media


class HuanghexinwenSpider(NewsRCSpider):
    """黄河新闻网"""
    name = 'hhxw'
    mystart_urls = {
        'http://car.sxgov.cn/news/more_list_column_43_1.html': 1301191,  # 黄河新闻网-国产车测评-左侧列表
        'http://car.sxgov.cn/news/more_list_column_35_1.html': 1301194,  # 黄河新闻网-新车咨询
        'http://car.sxgov.cn/news/more_list_column_2417_1.html': 1301193,  # 黄河新闻网-新车实拍
        'http://car.sxgov.cn/news/dujia.html': 1301436,  # 黄河新闻网-汽车最新列表
        'http://car.sxgov.cn/news/more_list_column_46_1.html': 1301192,  # 黄河新闻网-进口车测评
    }
    rules = (
        #http://car.sxgov.cn/news/storys_134328.html
        #http://car.sxgov.cn/news/storys_134209.html
        Rule(LinkExtractor(allow=(r'car.sxgov.cn/news/storys_\d+.html'),
                           ), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'car.sxgov.cn.*?_\d+.htm'),
                           ), callback='parse_item',
             follow=False),
    )
    parser = HuanghexinwenParser()
    
    #http://car.sxgov.cn/news/storys_134326.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='ina_news_text']/h1/text()").extract_first() or self.get_page_title(response).split('-')[0]
            content_div = xp("//div[starts-with(@class,'ina_content')]")[0]
            pubtime = xp("//span[@class='ina_data']").re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            origin_name = xp("//span[@class='ina_source']/a/text()").extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )