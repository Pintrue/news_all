# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider
from datetime import datetime
from copy import deepcopy


class JunwangSpipder(NewsRCSpider):
    name = 'junwang_all'

    # 中国军网
    mystart_urls = {
                    'http://kj.81.cn/node_57740.htm': 3195,   #  近期动态
                    'http://www.81.cn/2018xczjyjzzzw/node_104108.htm': 3182,   #  要闻
                    'http://www.81.cn/2019zt/node_104908.htm': 3179,   #  雪域边关
                    'http://www.81.cn/2019zt/node_104909.htm': 3177,   #  发展成就
                    'http://www.81.cn/gjzx/hqzx.htm': 3122,   #  环球资讯
                    'http://www.81.cn/gjzx/lbdt.htm': 3123,   #  图说热点
                    'http://www.81.cn/gnxw/node_79624.htm': 3120,   #
                    'http://www.81.cn/hj/node_61378.htm': 3135,   #  海军要闻
                    'http://www.81.cn/jmtt/node_62878.htm': 3156,   #  精彩点击
                    'http://www.81.cn/jmywyl/index.htm': 3183,   #  要闻要论
                    'http://www.81.cn/jmywyl/index_2.htm': 3191,   #  2
                    'http://www.81.cn/jsdj/node_61261.htm': 3125,   #  军史聚焦
                    'http://www.81.cn/jwgz/node_79499.htm': 3088,   #  军网关注
                    'http://www.81.cn/lj/node_61385.htm': 289,  # 3130,   #  边关瞭望
                    'http://www.81.cn/syjdt/node_68979.htm': 3089,   #  图解
                    'http://www.81.cn/syjdt/node_79500.htm': 3091,   #  图片
                    'http://www.81.cn/ty/node_62119.htm': 3149,   #  精彩播报
                    'http://www.81.cn/ty/node_62124.htm': 3150,   #  体坛动态
                    'http://www.81.cn/ty/node_62268.htm': 3148,   #  体坛明星
                    'http://www.81.cn/ty/node_62274.htm': 3145,   #  足球
                    'http://www.81.cn/ty/node_62381.htm': 3142,   #  综合
                    'http://www.81.cn/tzjy/node_62042.htm': 3128,   #  新闻
                    'http://www.81.cn/tzjy/node_62048.htm': 3127,   #  武警特战
                    'http://www.81.cn/wj/node_61505.htm': 3138,   #  要闻聚焦
                    'http://www.81.cn/xue-xi/node_102743.htm': 3172,   #  学习讲堂
                    'http://www.81.cn/xue-xi/node_102747.htm': 292,  # 3175,   #  学习新视界
                    'http://www.81.cn/xue-xi/node_102752.htm': 3186,   #  强军成绩单
                    'http://www.81.cn/xue-xi/node_102753.htm': 3184,   #  强军进行时
                    'http://www.81.cn/xue-xi/node_102754.htm': 3185,   #  强军兴军策
                    'http://www.81.cn/xue-xi/node_102761.htm': 3170,   #  图解
                    'http://www.81.cn/xue-xi/node_102769.htm': 3192,   #  评论
                    'http://www.81.cn/xue-xi/node_102770.htm': 3193,   #  理论

    }

    # http://kj.81.cn/content/2019-03/27/content_9460177.htm
    rules = (
        Rule(LinkExtractor(allow=(r'81.cn/content/%s.*?\d+.htm'%datetime.today().year,), ),
             callback='parse_item', follow=False),
    )

    custom_settings = {'DEPTH_LIMIT': 0,
                       'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
                       }
    
    # http://kj.81.cn/content/2019-03/27/content_9460177.htm
    def parse_item(self, response):
        try:
            new_div = response.xpath('.//div[@class="content"]')[0]
            source_div = new_div.xpath('.//div[@class="article-header"]/div[@class="info"]')[0]
            content_div =  new_div.xpath('.//div[@id="article-content"]')[0]
            pubtime = source_div.xpath('.//*/small/i[@class="time"]/text()').extract_first('').strip()
        except:
            return self.produce_debugitem(response, "xpath error")

        title1 = response.request.meta.get('link_text', '').strip()
        title = new_div.xpath('.//*/h1/text()').extract_first('').strip() or title1

        origin_name = source_div.xpath('.//span[1]/text()').extract_first('')

        next_a = response.xpath('.//a[contains(text(), "下一页")]')  # 下一页
        if next_a :
            content_div = response.xpath('.//div[@id="article-content"]')[0]
            # print(content_div.extract())
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })

        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths=['//center'])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)

        try:
            new_div = response.xpath('.//div[@class="content"]')[0]
            content_div = new_div.xpath('.//div[@id="article-content"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()

        next_a = response.xpath('.//a[contains(text(), "下一页")]')  # 下一页
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        """
        # 或者 
        next_url = xp('//*[@class="pageLink"]//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            yield response.follow(next_url, callback=self.parse_page)
        """
        content, media, videos, video_cover = self.content_clean(meta_new['content'],kill_xpaths=['//center'])

        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
