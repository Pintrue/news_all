# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.others import to_list
from news_all.spider_models import NewsRCSpider, otherurl_meta
from scrapy.conf import settings


class RMLTSpider(NewsRCSpider):
    """人民论坛_all"""
    name = 'rmlt_all'
    mystart_urls = {
        'http://www.rmlt.com.cn/husheng/': 6228,  # 人民呼声_人民呼声_人民论坛网
        'http://www.rmlt.com.cn/dangjian/': 6229,  # 党建_党建_人民论坛网
        'http://www.rmlt.com.cn/original/': 6232,  # 第一评论_第一评论_人民论坛网
        'http://www.rmlt.com.cn/governance/diaocha/': 6234,  # 调查发现_国家治理_人民论坛网
        'http://www.rmlt.com.cn/academics/shoufa/': 6235,  # 成果首发_学术前沿_人民论坛网
        'http://www.rmlt.com.cn/governance/community/': 6236,  # 治理观察_国家治理_人民论坛网
        'http://www.rmlt.com.cn/governance/zhili/': 6237,  # 治理之道_国家治理_人民论坛网
        'http://www.rmlt.com.cn/marx/': 6238,  # 马克思主义_马克思主义_人民论坛网
        'http://www.rmlt.com.cn/local/practice/': 6241,  # 实践感悟_地方要闻_人民论坛网
        'http://www.rmlt.com.cn/local/wenhua/': 6243,  # 文化生活_地方要闻_人民论坛网
        'http://www.rmlt.com.cn/zzpp/zhiku/': 6244,  # 品牌智库_自主品牌_人民论坛网
        'http://www.rmlt.com.cn/xuexi/wwyt/shp/': 6246,  # 社会篇_学习新思想_人民论坛网
        'http://www.rmlt.com.cn/xuexi/wwyt/jjp/': 6247,  # 经济篇_学习新思想_人民论坛网
        'http://www.rmlt.com.cn/xuexi/wwyt/zzp/': 6248,  # 政治篇_学习新思想_人民论坛网
        'http://www.rmlt.com.cn/xuexi/qwjd/': 6249,  # 权威解读_学习新思想_人民论坛网
        'http://www.rmlt.com.cn/governance/frontier/': 6250,  # 前沿理论_国家治理_人民论坛网
        'http://www.rmlt.com.cn/xiangcun/yaowen/': 6253,  # 要闻聚焦_乡村振兴_人民论坛网
        'http://art.rmlt.com.cn/wypl/': 6254,  # 文艺评论_文艺评论_人民论坛网
        'http://www.rmlt.com.cn/eco/jingjizhuanti/': 6256,  # 经济专题_经济观察_人民论坛网
        'http://politics.rmlt.com.cn/exclusive/': 6257,  # 独家政论_人民时政_人民论坛网
        'http://www.rmlt.com.cn/eco/finance/': 6258,  # 金融·理财_经济观察_人民论坛网
        'http://www.rmlt.com.cn/eco/huanbao/': 6259,  # 环保_经济观察_人民论坛网
        'http://www.rmlt.com.cn/eco/theory/': 6261,  # 经济理论_经济观察_人民论坛网
        'http://www.rmlt.com.cn/thinktank/zksl/': 6262,  # 智库沙龙_人民智库_人民论坛网
        'http://www.rmlt.com.cn/thinktank/zjgd/': 6263,  # 专家观点_人民智库_人民论坛网
        'http://www.rmlt.com.cn/idea/yuanchuang/': 6265,  # 深度原创_思想理论_人民论坛网
        'http://www.rmlt.com.cn/idea/pattern/': 6266,  # 时代楷模_思想理论_人民论坛网
        'http://www.rmlt.com.cn/academics/xueshu/eco/': 6267,  # 经济_学术前沿_人民论坛网
    }
    # http://www.rmlt.com.cn/2019/0225/540320.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'rmlt.com.cn/%s\d{2}/\d+\.s?html' % datetime.today().strftime('%Y/%m'),), ), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'rmlt.com.cn.*?\w{5,}\.s?htm',),
                           deny=(r'/201[0-8]', r'/2019/0[1-9]')),  # todo 正则匹配排除的年月
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))}

    # http://www.rmlt.com.cn/2019/0321/542543.shtml
    def parse_item(self, response):
        try:
            xp = response.xpath
            title = xp("//h1/text()").extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[@class='date']/text()").extract()[0].strip()
            origin_name = xp("//span[@class='source']/text()").extract_first('')
            content_div = xp("//div[@class='article-content fontSizeSmall BSHARE_POP']")[0]
            content, media, videos, cover = self.content_clean_rmlt(content_div)
        except:
            return self.parse_item2(response)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item2(self, response):
        # http://www.rmlt.com.cn/2019/0325/542807.shtml
        try:
            xp = response.xpath
            title = xp("//h1[@class='article-title']/text()").extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[@class='date']/text()").extract()[0].strip()
            origin_name = xp("//span[@class='source']/text()").extract_first('')
            content_div = xp("//div[@class='article-content fontSizeSmall BSHARE_POP']")[0]
            content, media, videos, cover = self.content_clean_rmlt(content_div)
        except:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # 解析图片组 参考（参考消息）爬虫 解析图片规则
    # http://www.rmlt.com.cn/2019/0327/543052.shtml
    def parse_item3(self, response):
        try:
            xp = response.xpath
            title = xp("//h1[@class='h1']/text()").extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[@class='post-time']/text()").extract()[0].strip()
            origin_name = xp("//span[@class='source']").extract_first('')
            content_fun = xp('//script[@type="text/javascript"]')[10].extract()
        except:
            return self.produce_debugitem(response, "xpath error")
            
        pat = re.compile(r"""orig: ['"](.*?)['"].*?note: ['"](.*?)['"]""")
        fr = re.finditer(pat, content_fun)
        media = {}
        new_content = ''

        for i, j in enumerate(fr):
            media.setdefault("images", {})
            src = j.group(1)
            media["images"][str(i + 1)] = {"src": src}
            new_content += '${{%s}}$<p>%s</p>' % ((i + 1), j.group(2).encode('utf-8').decode('unicode_escape'))
        
        # content, media, videos, cover = self.content_clean_rmlt(content)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=new_content,
            media=media
        )
    
    def content_clean_rmlt(self, content_div, need_video=False, kill_xpaths=None):
        # 校验sql  db.getCollection('news_all_local_debug').find({content:{$regex:"ifengLogo："}})
        kill_xpaths = to_list(kill_xpaths) + [r'//*[@class="ifengLogo"]']
        return super(RMLTSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)
