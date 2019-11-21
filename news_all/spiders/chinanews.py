# -*- coding: utf-8 -*-

import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from news_all.tools.html_clean import json_load_html
from news_all.tools.others import to_list


pattern = re.compile(r'videojsList = \["(http.*?)"\]')
pattern2 = re.compile(r'"vInfo", "(http.*?)"')


class ChinanewsSpider(NewsRCSpider):
    """中国新闻网"""
    name = 'chinanews'
    mystart_urls = {
        'http://www.chinanews.com/china/': 188,  # '时政',
        'http://www.chinanews.com/world/': 189,  # '国际',
        'http://www.chinanews.com/society/': 190,  # '社会',
        'http://finance.chinanews.com/': 191,  # '财经',
        # 'http://www.chinanews.com/photo/index.shtml': 0,  # '测试图集'
        # 'http://www.chinanews.com/shipin/': 0,  # '测试视频'
        
        # 来自spiders_all
        'http://channel.chinanews.com/cns/cl/gj-zxsjg.shtml': 760,  #
        'http://channel.chinanews.com/u/gj-rw.shtml': 761,  #
        'http://www.chinanews.com/world.shtml': 762,  #
        'http://www.chinanews.com/china.shtml': 763,  #
        'http://www.chinanews.com/house/gd.shtml': 764,  # 房产新闻滚动新闻-中新网
        'http://www.chinanews.com/photo/more/1.html': 765,  #
        'http://www.chinanews.com/entertainment.shtml': 766,  #
        'http://www.chinanews.com/mil/news.shtml': 767,  # 军事新闻滚动新闻-中新网
        'http://www.chinanews.com/stock/gd.shtml': 768,  # 证券新闻滚动新闻-中新网
        'http://www.chinanews.com/it/gd.shtml': 769,  # IT新闻滚动新闻-中新网
        'http://www.chinanews.com/theory.shtml': 776,  # 理论新闻滚动新闻-中新网
        'http://finance.chinanews.com/life/gd.shtml': 778,  # 生活新闻滚动新闻-中新网
        
        # 4月25日又打标了中国新闻网
        'http://www.qh.chinanews.com/': 867, 'http://auto.chinanews.com/': 906, 'http://cul.chinanews.com/': 909,
        'http://www.chinanews.com/huaren/': 911, 'http://www.chinanews.com/gangao/': 922,
        'http://sports.chinanews.com/': 924, 'http://ent.chinanews.com/': 925, 'http://www.chinanews.com/taiwan/': 926,
        'http://fortune.chinanews.com/': 927, 'https://www.chinanews.com/china/': 928,
        'http://www.jx.chinanews.com.cn/finance/': 1015, 'http://www.jx.chinanews.com.cn/society/': 1026,
        'http://www.cq.chinanews.com.cn/more/sqpl.shtml': 1027, 'http://www.cq.chinanews.com.cn/more/166.shtml': 1028,
        'http://www.cq.chinanews.com.cn/more/165.shtml': 1029, 'http://www.cq.chinanews.com.cn/more/zxfw.shtml': 1031,
        'http://www.cq.chinanews.com.cn/more/41.shtml': 1032, 'http://www.cq.chinanews.com.cn/more/gatq.shtml': 1033,
        'http://www.cq.chinanews.com.cn/more/25.shtml': 1034, 'http://www.cq.chinanews.com.cn/more/21.shtml': 1035,
        'http://www.cq.chinanews.com.cn/more/23.shtml': 1036, 'http://www.cq.chinanews.com.cn/more/26.shtml': 1037,
        'http://www.cq.chinanews.com.cn/more/10.shtml': 1038,
        'http://www.bt.chinanews.com.cn/zhongya/index.shtml': 1039,
        'http://www.bt.chinanews.com.cn/fazhi/index.shtml': 1040,
        'http://www.bt.chinanews.com.cn/shehui/index.shtml': 1041,
        'http://www.bt.chinanews.com.cn/shituan/index.shtml': 1042, 'http://www.zx-chinanews.com/html/kjjk/': 1043,
        'http://www.zx-chinanews.com/html/shengtai/': 1044, 'http://www.zx-chinanews.com/html/wenhua/': 1045,
        'http://www.zx-chinanews.com/html/jinrong/': 1046, 'http://www.zx-chinanews.com/html/shehui/': 1047,
        'http://www.zx-chinanews.com/html/jingji/': 1048, 'http://www.zx-chinanews.com/html/xgc/': 1049,
        'http://www.zx-chinanews.com/html/shixun/': 1051, 'http://www.hn.chinanews.com/news/lyxw/': 1052,
        'http://www.hn.chinanews.com/news/tyxw/': 1053,
        
        # 5月23日打标
        'https://www.chinanews.com/society.shtml': 2683,
        
        # 老爬虫的
        'http://www.chinanews.com/': 1302160,  # 中新网-要闻区-全部
    }
    # http://www.chinanews.com/cj/2019/01-18/8732773.shtml
    rules = (
        Rule(LinkExtractor(allow=r'chinanews\.com/tp/hd\d{4}/%s-\d{2}/\d{6,}\.s?html' % datetime.today().strftime('%Y/%m'),
                           ),
             callback='parse_images', follow=False),
        # http://www.chinanews.com/gj/shipin/2019/03-10/news806858.shtml
        Rule(LinkExtractor(allow=r'chinanews\.com/.*?shipin/.*?%s.*?\d{6,}\.s?html' % datetime.today().strftime('%Y/%m'), ),
             callback='parse_shipin', follow=False),
        # http://www.chinanews.com/tp/2019/03-25/8789589.shtml
        # 'http://www.chinanews.com/kong/2019/07-18/8898809.shtml',  # http://www.chinanews.com/sh/shipin/cns/2019/07-18/news824096.shtml
        Rule(LinkExtractor(allow=r'chinanews\.com/.*?/%s-\d{2}/\d{6,}\.s?html' % datetime.today().strftime('%Y/%m'),
                           deny=r'chinanews.com/kong/\d{4}'),
             callback='parse_item', follow=False),
    )

    # custom_settings = {'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))}
    
    def parse_item(self, response):
        try:
            news_div_over = response.xpath('.//div[@class="con_left"]/div[@id="cont_1_1_2"]')[0]
            head_div = news_div_over.xpath('.//div[@class="left-time"]/div[@class="left-t"]')[0]
            content_div = response.xpath('.//div[@class="left_zw"]')[0]
            time_re = head_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        # todo http://www.chinanews.com/sh/2019/01-19/8733617.shtml  图在正文div之外
        # http://www.chinanews.com/gn/2019/01-19/8733684.shtml  正文前有视频
        title = ' '.join(i.strip().replace('-中新网', '') for i in news_div_over.xpath('./h1/text()').extract())
        source_re = head_div.re('来源：(\w{2,})')
        origin_name = source_re[0] if source_re else ''
        content, media, videos, video_cover = self.content_clean(content_div, need_video=True,
                                                                 kill_xpaths='//div[@id="adhzh"]/ancestor::table')
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_shipin(self, response):
        # http://www.chinanews.com/shipin/2019/02-11/news802714.shtml
        # http://www.chinanews.com/gj/shipin/2019/03-10/news806858.shtml
        try:
            head_div = response.xpath('.//div[@class="content_title"]')[0]
            source_text = head_div.xpath('.//p//text()').extract_first('')
            pubtime_re = re.search(r'\d{2,4}年\d{1,2}月\d{1,2}日\s\d{1,2}\:\d{1,2}', source_text)
            pubtime = pubtime_re.group(0) if pubtime_re else ''
            origin_name_re = re.search('来源：(\w+)', source_text)
            origin_name = origin_name_re.group(1) if origin_name_re.group(1) else ''
            content_div = response.xpath('.//div[@class="content_desc"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        title = ''.join(i.strip() for i in head_div.xpath('.//h1/text()').extract())
        video_sh = pattern.search(response.text) or pattern2.search(response.text)
        if not video_sh:
            # http://www.chinanews.com/gn/shipin/2019/03-10/news806888.shtml
            return self.produce_debugitem(response, "xpath error")

        video_url = video_sh.group(1)
        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content='<div>#{{1}}#</div>' + content,
            media=media,
            videos={'1': {'src': video_url}},
        )

    def parse_images(self, response):
        
        rt = response.text
        start = rt.find('var picsJson=') + len('var picsJson=')
        end = start + rt[start:].find(';')  # 或者';\r\n\n</script>', 注意不是r';\r\n\n'
        try:
            img_cons = json_load_html(rt[start:end]).get('pics')
        except Exception as e:
            print(e, rt[start:end])
            return self.produce_debugitem(response, 'xpath error')

        try:
            tail_div = response.xpath('//div[contains(text(), "发布时间")]//text()')[0]
            pubtime = tail_div.re(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')[0]  # 发布时间：2019-03-10 12:46:29 【编辑：李骏】'
        except:
            return self.produce_debugitem(response, "xpath error")
        if not img_cons:
            return self.produce_debugitem(response, 'xpath error')

        title = img_cons[0].get('alt')
        content, media = make_img_content(img_cons)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name='中国新闻网',

            content=content,
            media=media
        )

    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        kill_xpaths = to_list(kill_xpaths) + [r'//div[@id="adhzh"]/ancestor::table',
                                              r'//table[@border="0"]',
                                              ]
        return super(ChinanewsSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)
    
    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(ChinanewsSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.custom_settings = {'DOWNLOADER_MIDDLEWARES': crawler.settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT')}
        return obj


def make_img_content(img_cons):
    """拼接json中图、文列表为html
    :param img_cons list
    """
    media = {'images': {}}
    content = ''
    for i, j in enumerate(img_cons):
        content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
        img_url = j.get('bigPicUrl') or j.get('middlePicUrl') or j.get('thumbPicUrl')
        media['images'][str(i + 1)] = {"src": img_url}

        if j.get('articleTitle'):
            content += '<p>' + j['articleTitle'] + '</p>'
    return content, media
