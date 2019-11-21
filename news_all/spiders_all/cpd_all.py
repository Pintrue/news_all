# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CpdAllSpider(NewsRCSpider):
    """中国警察网"""
    name = 'cpd_all'

    # mystart_urls = {
    #     'http://news.cpd.com.cn/n18151/': 1891,
    #     'http://news.cpd.com.cn/n3569/': 1892, 'http://news.cpd.com.cn/n3573/': 1893,
    #     'http://zhian.cpd.com.cn/n26237008/index.html': 1894,
    # }

    mystart_urls = {
        'http://www.cpd.com.cn/': 1,
        'http://news.cpd.com.cn/n18151/': 2,
        'http://news.cpd.com.cn/n3569/': 3,
        'http://www.cpd.com.cn/n10216060/n10216158/': 4,
        'http://news.cpd.com.cn/n3573/': 5,
        'http://culture.cpd.com.cn/n2572253/n2572282/': 6,
        'http://news.cpd.com.cn/n18106/': 7,
        'http://626.cpd.com.cn/n33447855/': 8,
        'http://life.cpd.com.cn/n2630005/': 9,
        'http://sydj.cpd.com.cn/n23502532/index.html': 10,
        'http://jt.cpd.com.cn/n462011/': 11,
        'http://jt.cpd.com.cn/n462013/': 12,
        'http://jt.cpd.com.cn/n462015/': 13,
        'http://jt.cpd.com.cn/n462023/': 14,
        'http://jt.cpd.com.cn/n464703/': 15,
        'http://jt.cpd.com.cn/n462041/': 16,
        'http://jt.cpd.com.cn/n462009/': 17,
        'http://jt.cpd.com.cn/n462059/': 18,
        'http://jt.cpd.com.cn/n462061/': 19,
        'http://jt.cpd.com.cn/n462051/': 20,
        'http://minsheng.cpd.com.cn/n1448480/': 21,
        'http://minsheng.cpd.com.cn/n1448482/': 22,
        'http://minsheng.cpd.com.cn/n1448484/': 23,
        'http://eci.cpd.com.cn/n2220390/index.html': 24,
        'http://zhjw.cpd.com.cn/n30136046/index.html': 25,
        'http://zhjw.cpd.com.cn/n30136048/index.html': 26,
        'http://police.cpd.com.cn/n2578709/': 27,
        'http://police.cpd.com.cn/n2578711/': 28,
        'http://police.cpd.com.cn/n2578717/n2578735/': 29,
        'http://police.cpd.com.cn/n2578717/n2578737/': 30,
        'http://police.cpd.com.cn/n2578717/n2578741/': 31,
        'http://police.cpd.com.cn/n2578721/': 32,
        'http://police.cpd.com.cn/n2578719/': 33,
        'http://police.cpd.com.cn/n2578725/': 34,
        'http://zbzx.cpd.com.cn/tszb.asp?key=0&page=1': 35,
        'http://zbzx.cpd.com.cn/tzgg.asp?key=0&page=1': 36,
        'http://zbzx.cpd.com.cn/zxzt.asp?key=0&page=1': 37,
        'http://zbzx.cpd.com.cn/enterprise.asp?key=0&page=1&xlei=0': 38,
        'http://zbzx.cpd.com.cn/exhibition.asp?page=1': 39,
        'http://zbzx.cpd.com.cn/equipment.asp?key=0&page=1&xlei=0': 40,
        'http://fazhi.cpd.com.cn/n605478/': 41,
        'http://fazhi.cpd.com.cn/n605486/': 42,
        'http://zhian.cpd.com.cn/n26237006/index.html': 43,
        'http://zhian.cpd.com.cn/n26237004/index.html': 44,
        'http://zhian.cpd.com.cn/n26237008/index.html': 45,
        'http://zhian.cpd.com.cn/n26237010/index.html': 46,
        'http://zhian.cpd.com.cn/n26237012/index.html': 47,
        'http://zhian.cpd.com.cn/n26237014/index.html': 48,
        'http://zhian.cpd.com.cn/n26237018/index.html': 49,
        'http://zhian.cpd.com.cn/n26237020/index.html': 50,
        'http://zhian.cpd.com.cn/n26237022/index.html': 51,
        'http://zhian.cpd.com.cn/n26237024/index.html': 52,
        'http://pic.cpd.com.cn/n3842/': 53,
        'http://pic.cpd.com.cn/n3824/': 54,
        'http://pic.cpd.com.cn/n3838/': 55,
        'http://pic.cpd.com.cn/n15403910/': 56,
        'http://policewomen.cpd.com.cn/n2386974/': 57,
        'http://jiansuo.cpd.com.cn/n15441436/index.html': 58,
        'http://jiansuo.cpd.com.cn/n2698294/index.html': 59,
        'http://jiansuo.cpd.com.cn/n847291/index.html': 60,
        'http://www.cpd.com.cn/n10216060/n10216144/': 61,
        'http://www.cpd.com.cn/n10216060/n10216166/': 62,
        'http://www.cpd.com.cn/n10216060/n10216160/': 63,
        'http://www.cpd.com.cn/n10216060/n10216162/index.html': 64,
        'http://news.cpd.com.cn/n3573/index.html': 65,
    }

    custom_settings = {
        'DEPTH_LIMIT': 0,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    deny_list = [
        r'/201[0-8]',
        r'/2019(?:0[1-9]|10)',
        r'index.htm',
    ]

    # http://news.cpd.com.cn/n3559/201904/t20190415_835839.html
    rules = (
        Rule(LinkExtractor(allow=r'pic.cpd.com.*?\w+.html',
                           deny=deny_list),
             callback='parse_album',
             follow=False),
        Rule(LinkExtractor(allow=r'cpd.com.cn.*?/%s/t\d+_\d+.html' % datetime.today().strftime('%Y%m'),
                           deny=deny_list),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'cpd.com.cn.*?/content.html',
                           deny=deny_list),
             callback='parse_item_1',
             follow=False),
        Rule(LinkExtractor(allow=r'cpd.com.cn.*?\w+.html',
                           deny=deny_list),
             process_request=otherurl_meta,
             follow=False)
    )

    time_pattern = re.compile(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}')
    page_content_pattern = re.compile(r'>(.*?摄)\s*<')
    img_pattern = re.compile(r'src=\"\.\/(.*?)\"')
    prefix_pattern = re.compile(r'http://(.*?)t\w+.html')

    """
    """
    """
        CLASS FUNCTIONS BEGIN BELOW
    """
    """
    """

    # http://news.cpd.com.cn/n3559/201904/t20190415_835839.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@id="fz_change"]/div[@id="newslist"]')[0]
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}') or xp('//span[@id="pub_time_report"]/text()').extract()
            pubtime = time_re[0].strip()
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in source_div.xpath('.//h1/text()').extract()) or self.get_page_title(response).split('-')[0]
        origin_name = source_div.xpath('.//div[@class="newsattr z12"]/span[@id="source_report"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://news.cpd.com.cn/n18106/c42383483/content.html
    def parse_item_1(self, response):
        xp = response.xpath

        try:
            title = xp("//h1/gettitle/text()").extract()[0]
            pub_time = xp("//span[@id='pub_time_report']/text()").extract()[0]
            pub_time = "".join(pub_time.split())
            origin_name = xp("//span[@id='source_report']/text()").extract_first()
            origin_name = origin_name if origin_name else ''
            content_div = xp("//div[@class='news_contents hetitle_01']/.//td").extract()[0]
            content, media, _, _ = self.content_clean(content_div)

        except Exception as e:
            return self.produce_debugitem(response, "xpath error - parse_item_2(): "+str(e))

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pub_time,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://pic.cpd.com.cn/n15403910/201911/t20191104_863211.html
    def parse_album(self, response):
        xp = response.xpath

        try:
            title = xp('/html/head/title/text()').extract_first().split()[0]
            source_div = xp("//span[@id='pub_time_report']")
            time_div = source_div.xpath(".//span[@id='pub_time_report']").extract_first()
            pub_time = self.time_pattern.findall(time_div)[0]
            origin_name = source_div.xpath(".//span[@id='source_report']/text()").extract_first().split()[0]

            media = {'images': {}}
            content = ''

            page_content_div = xp('//*[@id="content"]')
            img_part = self.img_pattern.findall(page_content_div
                                                .xpath('.//p[@align="center"] | .//div[@align="center"]')
                                                .extract_first()
                                                )[0]
            img_full_url = self.concat_image_url(response.url, img_part)
            media['images']['1'] = {"src": img_full_url}
            content += '<p>' + '${{1}}$' + '</p>'

            page_content = self.page_content_clean(page_content_div)

            content += '<p>' + page_content + '</p>'

            page_num_pat = re.compile(r'var countPage = (\d+)')
            js_paging_div = xp('//*[@id="autopage"]/table/tbody/tr/td/script[1]/text()').extract()[0]
            page_num = int(page_num_pat.findall(js_paging_div)[0])

            if page_num > 1:
                second_page_url = response.url.split('.html')[0] + '_1' + '.html'
                return response.follow(second_page_url,
                                       callback=self.parse_page,
                                       meta={
                                           'source_id': response.meta.get('source_id'),
                                           'first_url': response.url,
                                           'pubtime': pub_time,
                                           'title': title,
                                           'origin_name': origin_name,
                                           'content': content,
                                           'media': media,
                                           'start_url_time': response.meta.get('start_url_time'),
                                           'schedule_time': response.meta.get('schedule_time'),
                                           'total_page': page_num,
                                           'curr_page_key': 2
                                       })

        except Exception as e:
            return self.produce_debugitem(response, "TODO: album "+str(e))

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pub_time,
            origin_name=origin_name,
            content=content,
            media=media
        )

    """
        网站给出的是相对路径，需要进行拼接
        :param  img_url::str        图片的相对引用路径
        :return img_full_url::str   图片的绝对引用路径
    """
    def concat_image_url(self, page_url, img_url):
        return 'http://' + self.prefix_pattern.findall(page_url)[0] + img_url

    # http://pic.cpd.com.cn/n15403910/201911/t20191104_863211_1.html
    # http://pic.cpd.com.cn/n3842/201911/t20191104_863196_1.html
    # http://pic.cpd.com.cn/n3838/201911/t20191111_864425_3.html
    def parse_page(self, response):
        xp = response.xpath
        new_meta = deepcopy(response.meta)

        curr_page_key = new_meta['curr_page_key']

        try:
            content_div = xp('//*[@id="content"]')

            img_divs = content_div.xpath('.//*[@align="center"]').extract()
            if len(img_divs) < 1:
                img_divs = content_div.xpath('.//*[@class="TRS_Editor"]').extract()

            img_part = ''
            for img_div in img_divs:
                if self.img_pattern.search(img_div):
                    img_part = self.img_pattern.findall(img_div)[0]

            img_full_url = self.concat_image_url(response.url, img_part)
            new_meta['media']['images'][str(curr_page_key)] = {"src": img_full_url}
            new_meta['content'] += '<p>' + '${{%s}}$' % curr_page_key + '</p>'

            page_content = self.page_content_clean(content_div)
            new_meta['content'] += '<p>' + page_content + '</p>'

            if curr_page_key < new_meta['total_page']:
                new_meta['curr_page_key'] += 1
                next_page_url = re.sub(r'_\d\.html', '_%s.html' % (new_meta['curr_page_key']-1), response.url)
                return response.follow(next_page_url,
                                       callback=self.parse_page,
                                       meta=new_meta)

        except Exception as e:
            return self.produce_debugitem(response, "TODO: page " + str(e))

        return self.produce_item(
            response=response,
            title=new_meta.get('title'),
            pubtime=new_meta.get('pubtime'),
            origin_name=new_meta.get('origin_name'),
            content=new_meta.get('content'),
            media=new_meta.get('media'),
            srcLink=new_meta.get('first_url')
        )
        # return new_meta

    def page_content_clean(self, content_div):
        clean_content = content_div.xpath('.//*[@id="contentText"]/p/text() | .//table').extract_first()

        if clean_content is not None:
            clean_content = "".join(clean_content.split())
        else:
            for c in content_div.extract():
                if self.page_content_pattern.search(c):
                    clean_content = self.page_content_pattern.findall(c)[0]
                    clean_content = "".join(clean_content.split())
                    re.sub(r'<\S+>', '', clean_content)

        return clean_content
