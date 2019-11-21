from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Yoka(NewsRCSpider):
    name = 'yoka'

    # YOKA时尚网 ==》 补充全站采集
    mystart_urls = {
        'http://www.yoka.com/dna/': 7554,   #  YOKA时尚网
        'http://www.yoka.com/fashion/': 7555,   #  YOKA时尚网
        'http://www.yoka.com/club/': 7556,   #  YOKA时尚网
        'http://www.yoka.com/street/': 7557,   #  YOKA时尚网
        'http://www.yoka.com/show/?source_fashion': 7558,   #  YOKA时尚网
        'http://www.yoka.com/fashion/menstyle/': 7559,   #  YOKA时尚网
        'http://www.yoka.com/fashion/ins/': 7560,   #  YOKA时尚网
        'http://www.yoka.com/club/frontrow/': 7561,   #  YOKA时尚网
        'http://www.yoka.com/fashion/trend/': 7562,   #  YOKA时尚网
        'http://www.yoka.com/beauty/': 7563,   #  YOKA时尚网
        'http://www.yoka.com/beauty/skincare/': 7564,   #  YOKA时尚网
        'http://www.yoka.com/beauty/fragrance/': 7565,   #  YOKA时尚网
        'http://www.yoka.com/beauty/bodycare/': 7566,   #  YOKA时尚网
        'http://www.yoka.com/beauty/homme/': 7567,   #  YOKA时尚网
        'http://www.yoka.com/video/beauty/': 7568,   #  YOKA时尚网
        'http://www.yoka.com/video/runway/index.shtml': 7569,   #  YOKA时尚网
        'http://www.yoka.com/video/brand/index.shtml': 7570,   #  YOKA时尚网
        'http://www.yoka.com/video/hot/index.shtml': 7571,   #  YOKA时尚网
        'http://www.yoka.com/luxury/': 7572,   #  YOKA时尚网
        'http://www.yoka.com/marry/': 7573,   #  YOKA时尚网
        'http://www.yoka.com/luxury/ju/': 7574,   #  YOKA时尚网
        'http://www.yoka.com/luxury/eyecatch/': 7575,   #  YOKA时尚网
        'http://www.yoka.com/club/modernicon/list/index.shtml': 7576,   #  YOKA时尚网
        'http://www.yoka.com/luxury/jewelryfortunetelling/': 7653,   #  YOKA时尚网
        'http://www.yoka.com/luxury/watch/': 7654,   #  YOKA时尚网
        'http://www.yoka.com/luxury/royalstory/': 7655,   #  YOKA时尚网
        'http://www.yoka.com/marry/bridetrend/': 7656,   #  YOKA时尚网
        'http://star.yoka.com/': 7657,   #  YOKA时尚网
        'http://www.yoka.com/star/tianshengjuren/index.shtml': 7658,   #  YOKA时尚网
        'http://www.yoka.com/star/starwear/': 7659,   #  YOKA时尚网
        'http://www.yoka.com/star/starnews/': 7660,   #  YOKA时尚网
        'http://www.yoka.com/star/starface/': 7661,   #  YOKA时尚网
        'http://www.yoka.com/star/starfashion/': 7662,   #  YOKA时尚网
        'http://www.yoka.com/star/top/': 7663,   #  YOKA时尚网
        'http://life.yoka.com/': 7664,   #  YOKA时尚网
        'http://yoka.com/life/hotel/': 7665,   #  YOKA时尚网
        'http://www.yoka.com/life/digital/': 7666,   #  YOKA时尚网
        'http://www.yoka.com/life/meiqi/': 7667,   #  YOKA时尚网
        'http://www.yoka.com/life/psychologies/': 7668,   #  YOKA时尚网
        'http://www.yoka.com/life/news/': 7669,   #  YOKA时尚网
        'http://www.yokamen.cn/': 7670,   #  YOKA时尚网
        'http://www.yokamen.cn/style/': 7671,   #  YOKA时尚网
        'http://www.yokamen.cn/luxury/': 7672,   #  YOKA时尚网
        'http://www.yokamen.cn/face/': 7673,   #  YOKA时尚网
        'http://www.yokamen.cn/digital/': 7674,   #  YOKA时尚网
        'http://www.yoka.com/video/': 7675,   #  YOKA时尚网
        'http://www.yoka.com/video/feature/index.shtml': 7676,   #  YOKA时尚网
        'http://www.yoka.com/video/star/index.shtml': 7677,   #  YOKA时尚网
        'http://www.yoka.com/video/beauty/index.shtml': 7678,   #  YOKA时尚网
        'http://www.yoka.com/video/ad/index.shtml': 7679,   #  YOKA时尚网
        'http://bbs.yoka.com/': 7680,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-95-1.html': 7681,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-36-1.html': 7682,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-84-1.html': 7683,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-34-1.html': 7684,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-87-1.html': 7685,   #  YOKA时尚网
        'http://bbs.yoka.com/forum-63-1.html': 7686,   #  YOKA时尚网
        'http://brand.yoka.com/': 7687,   #  YOKA时尚网
        'http://brand.yoka.com/news.htm': 7688,   #  YOKA时尚网
        'http://brand.yoka.com/tu.htm': 7689,   #  YOKA时尚网
        'http://brand.yoka.com/comments/cosmetics/': 7690,   #  YOKA时尚网
        'http://brand.yoka.com/comments/clothes/': 7691,   #  YOKA时尚网
        'http://brand.yoka.com/comments/bag/': 7692,   #  YOKA时尚网
        'http://brand.yoka.com/comments/watch/': 7693,   #  YOKA时尚网
        'http://brand.yoka.com/comments/jewelry/': 7694,   #  YOKA时尚网
        'http://brand.yoka.com/comments/accessory/': 7695,   #  YOKA时尚网
        'http://brand.yoka.com/comments/shoes/': 7696,   #  YOKA时尚网
        'http://brand.yoka.com/video.htm': 7697,   #  YOKA时尚网
        'http://www.yoka.com/fashion/professionnews/index.shtml': 7698,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b13.html': 7699,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c30.html': 7700,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c55.html': 7701,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c20.html': 7702,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b10.html': 7703,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c11.html': 7704,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c105.html': 7705,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c38.html': 7706,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c22.html': 7707,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/c104.html': 7708,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b17.html': 7709,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b23.html': 7710,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b49.html': 7711,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b7.html': 7712,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b9.html': 7713,   #  YOKA时尚网
        'http://www.yoka.com/dna/li/b50.html': 7714,   #  YOKA时尚网
        'http://www.yoka.com/dna/star/article-0-1.html': 7715,   #  YOKA时尚网
        'http://www.yoka.com/dna/star/article-1-1.html': 7716,   #  YOKA时尚网
        'http://www.yoka.com/dna/star/article-2-1.html': 7717,   #  YOKA时尚网
        'http://www.yoka.com/dna/star/article-3-1.html': 7718,   #  YOKA时尚网
        'http://www.yoka.com/dna/star/article-4-1.html': 7719,   #  YOKA时尚网
        'http://www.yoka.com/dna/w0.html': 7720,   #  YOKA时尚网
        'http://www.yoka.com/dna/m0.html': 7721,   #  YOKA时尚网
        'http://www.yoka.com/fashion/edittj/': 7722,   #  YOKA时尚网
        'http://www.yoka.com/fashion/popinfo/': 7723,   #  YOKA时尚网
        'http://www.yoka.com/fashion/windows/': 7724,   #  YOKA时尚网
        'http://street.yoka.com/': 7725,   #  YOKA时尚网
        'http://www.yoka.com/star/hotshot/index.shtml': 7726,   #  YOKA时尚网
        'http://www.yoka.com/star/roadshow/': 7727,   #  YOKA时尚网
        'http://www.yoka.com/star/topic/': 7728,   #  YOKA时尚网
        'http://www.yoka.com/star/baby/': 7729,   #  YOKA时尚网


    }

    rules = (
        # http://www.yoka.com/dna/d/454/233.html
        Rule(LinkExtractor(allow=r'yoka.com/\w+/\w+/\d+/\d+\.html',),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'yoka.com/.*?\.html', deny=(r'/index', r'/li')),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://www.yoka.com/dna/d/454/233.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@id='dnaTextBox']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='time']/span[1]/text()").get().split('：')[-1]
            content_div = xp("//div[@id='dnaTextBox']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,
                                                                     kill_xpaths=["//div[@id='dnaTextBox']/h1",
                                                                                  "//div[@class='time']",
                                                                                  "//div[@class='ctags']"])  # str  list
            origin_name = xp("string(//div[@class='time']/span[3])").get().split('：')[1]  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )



