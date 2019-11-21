from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.html_clean import json_load_html
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re

class PeopleSpider(NewsRCSpider):
    name = 'sina'

    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'https://news.sina.com.cn/': 6923,  # 新浪新闻
        'https://mil.news.sina.com.cn/': 6924,  # 新浪新闻
        'http://mil.news.sina.com.cn/roll/index.d.html?cid=57918': 6925,  # 新浪新闻
        'http://mil.news.sina.com.cn/roll/index.d.html?cid=57919': 6926,  # 新浪新闻
        'https://mil.news.sina.com.cn/jssd/': 6927,  # 新浪新闻
        'http://mil.news.sina.com.cn/dgby/': 6928,  # 新浪新闻
        'http://mil.news.sina.com.cn/jshm/': 6929,  # 新浪新闻
        'http://sky.news.sina.com.cn/': 6930,  # 新浪新闻
        'http://sky.news.sina.com.cn/aviation/': 6931,  # 新浪新闻
        'https://news.sina.com.cn/china/': 6932,  # 新浪新闻
        'https://news.sina.com.cn/world/': 6933,  # 新浪新闻
        'http://sports.sina.com.cn/': 6934,  # 新浪新闻
        'http://sports.video.sina.com.cn/': 6935,  # 新浪新闻
        'http://sports.sina.com.cn/hdphoto/': 6936,  # 新浪新闻
        'http://slide.sports.sina.com.cn/k/': 6937,  # 新浪新闻
        'http://slide.sports.sina.com.cn/g/': 6938,  # 新浪新闻
        'http://slide.sports.sina.com.cn/o/': 6939,  # 新浪新闻
        'http://slide.sports.sina.com.cn/t/': 6940,  # 新浪新闻
        'http://slide.sports.sina.com.cn/go/': 6941,  # 新浪新闻
        'http://slide.sports.sina.com.cn/shoe/': 6942,  # 新浪新闻
        'http://sports.sina.com.cn/hdphoto/story/': 6943,  # 新浪新闻
        'http://slide.sports.sina.com.cn/cba/': 6944,  # 新浪新闻
        'http://slide.sports.sina.com.cn/n/': 6945,  # 新浪新闻
        'http://slide.sports.sina.com.cn/golf/': 6946,  # 新浪新闻
        'http://slide.sports.sina.com.cn/f1/': 6947,  # 新浪新闻
        'http://slide.sports.sina.com.cn/l/': 6948,  # 新浪新闻
        'http://sports.sina.com.cn/china/': 6949,  # 新浪新闻
        'http://sports.sina.com.cn/z/CHN2022/': 6950,  # 新浪新闻
        'http://sports.sina.com.cn/qiruizujin/': 6951,  # 新浪新闻
        'http://sports.sina.com.cn/z/93guoao/': 6952,  # 新浪新闻
        'http://sports.sina.com.cn/csl/': 6953,  # 新浪新闻
        'http://sports.sina.com.cn/z/AFCCL/': 6954,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/zuxiebei/': 6955,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/zhongjia/': 6956,  # 新浪新闻
        'http://sports.sina.com.cn/z/womenfootball/': 6957,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/futsal/': 6958,  # 新浪新闻
        'http://sports.sina.com.cn/j/goalnews/': 6959,  # 新浪新闻
        'http://sports.sina.com.cn/global/': 6960,  # 新浪新闻
        'http://2018.sina.com.cn/': 6961,  # 新浪新闻
        'http://sports.sina.com.cn/g/championsleague/': 6962,  # 新浪新闻
        'http://sports.sina.com.cn/g/premierleague/index.shtml': 6963,  # 新浪新闻
        'http://sports.sina.com.cn/g/laliga/': 6964,  # 新浪新闻
        'http://sports.sina.com.cn/g/seriea/': 6965,  # 新浪新闻
        'http://sports.sina.com.cn/g/bundesliga/': 6966,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/euro2020/': 6967,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/europaleague1920/': 6968,  # 新浪新闻
        'http://sports.sina.com.cn/g/southamerica/': 6969,  # 新浪新闻
        'http://roll.sports.sina.com.cn/sportsori/index.shtml': 6970,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/globalzhuanlan/': 6971,  # 新浪新闻
        'http://sports.sina.com.cn/global/top20/': 6972,  # 新浪新闻
        'http://match.sports.sina.com.cn/football/opta_rank.php': 6973,  # 新浪新闻
        'http://sports.sina.com.cn/nba/': 6974,  # 新浪新闻
        'https://krcom.cn/album/aW6Ul2qUn5ppZ3Fl': 6975,  # 新浪新闻
        'https://slamdunk.sports.sina.com.cn/match#status=1&date=2019-10-31': 6976,  # 新浪新闻
        'https://slamdunk.sports.sina.com.cn/rank#type=conference': 6977,  # 新浪新闻
        'https://slamdunk.sports.sina.com.cn/player/rank#season_type=reg&item_type=average&item=points': 6978,  # 新浪新闻
        'https://slamdunk.sports.sina.com.cn/': 6979,  # 新浪新闻
        'http://lottery.sina.com.cn/ai/': 6980,  # 新浪新闻
        'http://sports.sina.com.cn/nba/scoreboard/': 6981,  # 新浪新闻
        'http://sports.sina.com.cn/cba/': 6982,  # 新浪新闻
        'http://sports.sina.com.cn/sgl/': 6983,  # 新浪新闻
        'http://cba.sports.sina.com.cn/cba/schedule': 6984,  # 新浪新闻
        'http://sports.sina.com.cn/roll/#pageid=13&lid=609&k=&num=50&page=1': 6985,  # 新浪新闻
        'http://sports.sina.com.cn/z/chenxicolumn/': 6986,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/cbareview/': 6987,  # 新浪新闻
        'http://sports.sina.com.cn/z/cbatopics/': 6988,  # 新浪新闻
        'http://sports.sina.com.cn/qiruizujin/index.shtml': 6989,  # 新浪新闻
        'http://sports.sina.com.cn/others/': 6990,  # 新浪新闻
        'http://sports.sina.com.cn/others/volley.shtml': 6991,  # 新浪新闻
        'http://sports.sina.com.cn/others/swim.shtml': 6992,  # 新浪新闻
        'http://sports.sina.com.cn/others/pingpang.shtml': 6993,  # 新浪新闻
        'http://sports.sina.com.cn/others/badmin.shtml': 6994,  # 新浪新闻
        'http://sports.sina.com.cn/others/snooker.shtml': 6995,  # 新浪新闻
        'http://sports.sina.com.cn/others/tianjing.shtml': 6996,  # 新浪新闻
        'http://sports.sina.com.cn/others/ticao.shtml': 6997,  # 新浪新闻
        'http://sports.sina.com.cn/others/sh.shtml': 6998,  # 新浪新闻
        'http://sports.sina.com.cn/others/others.shtml': 6999,  # 新浪新闻
        'http://sports.sina.com.cn/roll/#pageid=13&lid=575&k=&num=50&page=1': 7000,  # 新浪新闻
        'http://sports.sina.com.cn/others/kungfu.shtml': 7001,  # 新浪新闻
        'http://sports.sina.com.cn/winter/': 7002,  # 新浪新闻
        'http://sports.sina.com.cn/horse/': 7003,  # 新浪新闻
        'http://sports.sina.com.cn/tennis/': 7004,  # 新浪新闻
        'http://f1.sina.com.cn/': 7005,  # 新浪新闻
        'http://sports.sina.com.cn/col/roll/#pageid=401&lid=1870&k=&num=50&page=1)': 7006,  # 新浪新闻
        'http://sports.sina.com.cn/f1/schedule/': 7007,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/201920fe/': 7008,  # 新浪新闻
        'http://sports.sina.com.cn/col/roll/#pageid=401&lid=1871&k=&num=50&page=1': 7009,  # 新浪新闻
        'http://sports.sina.com.cn/col/roll/#pageid=401&lid=1872&k=&num=50&page=1': 7010,  # 新浪新闻
        'http://sports.sina.com.cn/col/roll/#pageid=401&lid=1873&k=&num=50&page=1': 7011,  # 新浪新闻
        'http://sports.sina.com.cn/roll/#pageid=13&lid=585&k=&num=50&page=1': 7012,  # 新浪新闻
        'http://sports.sina.com.cn/col/roll/#pageid=401&lid=714&k=&num=50&page=1': 7013,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/shangjieqiwang3/': 7014,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/cwl2019/': 7015,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/weiqiai/': 7016,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/sinagocollege/': 7017,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/sinapokercollege/': 7018,  # 新浪新闻
        'http://sports.sina.com.cn/zt_d/goligo/': 7019,  # 新浪新闻
        'http://sports.sina.com.cn/chess/weiqi/': 7020,  # 新浪新闻
        'http://sports.sina.com.cn/chess/guoxiang/': 7021,  # 新浪新闻
        'http://sports.sina.com.cn/chess/ent/': 7022,  # 新浪新闻
        'http://sports.sina.com.cn/chess/dv/': 7023,  # 新浪新闻
        'http://duiyi.sina.com.cn/gibo/new_gibo.asp': 7024,  # 新浪新闻
        'http://run.sina.com.cn/': 7025,  # 新浪新闻
        'http://roll.sports.sina.com.cn/run/news/1/index.shtml': 7026,  # 新浪新闻
        'http://roll.sports.sina.com.cn/run/news/2/index.shtml': 7027,  # 新浪新闻
        'http://roll.sports.sina.com.cn/run/news/3/index.shtml': 7028,  # 新浪新闻
        'http://roll.sports.sina.com.cn/run/news/4/index.shtml': 7029,  # 新浪新闻
        'http://sports.sina.com.cn/run/pic/': 7030,  # 新浪新闻
        'http://sports.sina.com.cn/run/video/': 7031,  # 新浪新闻
        'http://sports.sina.com.cn/outdoor/': 7032,  # 新浪新闻
        'http://sports.sina.com.cn/others/sailing/': 7033,  # 新浪新闻
        'http://sports.sina.com.cn/z/outdoornews/': 7034,  # 新浪新闻
        'http://sports.sina.com.cn/fitness/': 7035,  # 新浪新闻
        'http://lottery.sina.com.cn/': 7036,  # 新浪新闻
        'http://lottery.sina.com.cn/qiutong/': 7037,  # 新浪新闻
        'http://lottery.sina.com.cn/ai/datalist.shtml': 7038,  # 新浪新闻
        'http://lottery.sina.com.cn/ai/ranking/': 7039,  # 新浪新闻
        'http://sports.sina.com.cn/lotto/': 7040,  # 新浪新闻
        'http://sports.sina.com.cn/l/football/': 7041,  # 新浪新闻
        'http://odds.sports.sina.com.cn/odds/': 7042,  # 新浪新闻
        'http://odds.sports.sina.com.cn/liveodds/': 7043,  # 新浪新闻
        'http://sports.sina.com.cn/l/kaijiang/': 7044,  # 新浪新闻
        'http://caitong.sina.com.cn/': 7045,  # 新浪新闻
        'http://caitong.sina.com.cn/news/observe/': 7046,  # 新浪新闻
        'http://caitong.sina.com.cn/news/china/': 7047,  # 新浪新闻
        'http://caitong.sina.com.cn/news/world/': 7048,  # 新浪新闻
        'http://caitong.sina.com.cn/news/voice/': 7049,  # 新浪新闻
        'http://caitong.sina.com.cn/chart/': 7050,  # 新浪新闻
        'http://lottery.sina.com.cn/video/fcopen/': 7051,  # 新浪新闻
        'http://lottery.sina.com.cn/video/tcopen/': 7052,  # 新浪新闻
        'http://sports.sina.com.cn/zl/': 7053,  # 新浪新闻
        'http://sports.sina.com.cn/zl/football/': 7054,  # 新浪新闻
        'http://sports.sina.com.cn/zl/basketball/': 7055,  # 新浪新闻
        'http://sports.sina.com.cn/zl/other/': 7056,  # 新浪新闻
        'http://blog.sina.com.cn/lm/sports/': 7057,  # 新浪新闻
        'http://game.sports.sina.com.cn/?sinahome&suda-key=super&suda-value=home:guide': 7058,  # 新浪新闻
        'http://sports.sina.com.cn/sdzs/': 7059,  # 新浪新闻
        'http://sports.sina.com.cn/uclvideo/': 7060,  # 新浪新闻
        'http://sports.sina.com.cn/g/ucl/fixtures.html': 7061,  # 新浪新闻
        'http://sports.sina.com.cn/g/ucl/table.html': 7062,  # 新浪新闻
        'http://sports.sina.com.cn/g/premierleague/': 7063,  # 新浪新闻
        'http://blog.sina.com.cn/': 7064,  # 新浪新闻
        'http://blog.sina.com.cn/lm/ent/': 7065,  # 新浪新闻
        'http://blog.sina.com.cn/lm/history/': 7066,  # 新浪新闻
        'http://blog.sina.com.cn/lm/edu/': 7067,  # 新浪新闻
        'http://blog.sina.com.cn/lm/eatblog.html': 7068,  # 新浪新闻
        'http://blog.sina.com.cn/lm/baby/': 7069,  # 新浪新闻
        'http://blog.sina.com.cn/lm/astro/': 7070,  # 新浪新闻
        'http://zhuanlan.sina.com.cn/': 7071,  # 新浪新闻
        'http://news.sina.com.cn/ruijian/': 7072,  # 新浪新闻
        'http://finance.sina.com.cn/zl/': 7073,  # 新浪新闻
        'http://finance.sina.com.cn/zl/china/': 7074,  # 新浪新闻
        'http://finance.sina.com.cn/zl/international/': 7075,  # 新浪新闻
        'http://finance.sina.com.cn/zl/invest/': 7076,  # 新浪新闻
        'http://finance.sina.com.cn/zl/50forum/': 7077,  # 新浪新闻
        'http://tech.sina.com.cn/chuangshiji/': 7078,  # 新浪新闻
        'http://ent.sina.com.cn/zl/': 7079,  # 新浪新闻
        'http://ent.sina.com.cn/zl/bagua/': 7080,  # 新浪新闻
        'http://ent.sina.com.cn/zl/discuss/': 7081,  # 新浪新闻
        'http://fashion.sina.com.cn/zl/': 7082,  # 新浪新闻
        'http://fashion.sina.com.cn/zl/fashion/': 7083,  # 新浪新闻
        'http://fashion.sina.com.cn/zl/beauty/': 7084,  # 新浪新闻
        'http://weather.sina.com.cn/china/': 7085,  # 新浪新闻
        'http://weather.sina.com.cn/guoji/': 7086,  # 新浪新闻
        'http://weather.sina.com.cn/kongqi/beijing': 7087,  # 新浪新闻
        'https://fashion.sina.com.cn/': 7088,  # 新浪新闻
        'http://fashion.sina.com.cn/style/': 7089,  # 新浪新闻
        'http://fashion.sina.com.cn/beauty/': 7090,  # 新浪新闻
        'http://fashion.sina.com.cn/luxury/': 7091,  # 新浪新闻
        'http://fashion.sina.com.cn/luxury/taste/': 7092,  # 新浪新闻
        'http://roll.fashion.sina.com.cn/luxury/watch/index.shtml': 7093,  # 新浪新闻
        'http://roll.fashion.sina.com.cn/luxury/de/index.shtml': 7094,  # 新浪新闻
        'http://collection.sina.com.cn/': 7095,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml': 7096,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/hwdt/index.shtml': 7097,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/pmzx/index.shtml': 7098,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/zlxx/index.shtml': 7099,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/cpsc/index.shtml': 7100,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/jczs2/index.shtml': 7101,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/cqyw/index.shtml': 7102,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/cjrw1/index.shtml': 7103,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/plfx/index.shtml': 7104,  # 新浪新闻
        'http://collection.sina.com.cn/zisha/': 7105,  # 新浪新闻
        'http://interface.sina.cn/collection/pc_shpd_yjzx_list_index.d.html?cid=shgd': 7106,  # 新浪新闻
        'http://interface.sina.cn/collection/pc_ds_list_index.d.html?cid=dsj': 7107,  # 新浪新闻
        'http://roll.collection.sina.com.cn/collection/gjsb/index.shtml': 7108,  # 新浪新闻
        'http://interface.sina.cn/collection/pc_yszb_hyxw_list_index.html': 7109,  # 新浪新闻
        'http://fashion.sina.com.cn/wedding/': 7110,  # 新浪新闻
        'http://fashion.sina.com.cn/men/': 7111,  # 新浪新闻
        'http://roll.fashion.sina.com.cn/luxury/famous/index.shtml': 7112,  # 新浪新闻
        'http://fashion.sina.com.cn/video/': 7113,  # 新浪新闻
        'http://eladies.sina.com.cn/': 7114,  # 新浪新闻
        'https://med.sina.com/': 7115,  # 新浪新闻
        'https://med.sina.com/column/yaoqi/': 7116,  # 新浪新闻
        'https://med.sina.com/column/yaodian/': 7117,  # 新浪新闻
        'https://med.sina.com/column/yiyuan/': 7118,  # 新浪新闻
        'https://med.sina.com/column/zonghe/': 7119,  # 新浪新闻
        'https://med.sina.com/column/cth/': 7120,  # 新浪新闻
        'https://med.sina.com/article/keyword/5/': 7121,  # 新浪新闻
        'https://med.sina.com/article/keyword/6/': 7122,  # 新浪新闻
        'https://med.sina.com/column/cth/dgs/': 7123,  # 新浪新闻
        'https://med.sina.com/column/cth/cyb/': 7124,  # 新浪新闻
        'https://med.sina.com/column/cth/hlw/': 7125,  # 新浪新闻
        'http://baby.sina.com.cn/': 7126,  # 新浪新闻
        'http://baby.sina.com.cn/zhunbei/': 7127,  # 新浪新闻
        'http://baby.sina.com.cn/huaiyun/': 7128,  # 新浪新闻
        'http://baby.sina.com.cn/fenmian/': 7129,  # 新浪新闻
        'http://roll.baby.sina.com.cn/babynewslist/fmq/default/chhf/index.shtml': 7130,  # 新浪新闻
        'http://baby.sina.com.cn/xinsheng/': 7131,  # 新浪新闻
        'http://baby.sina.com.cn/yinger/': 7132,  # 新浪新闻
        'http://baby.sina.com.cn/youer/': 7133,  # 新浪新闻
        'http://baby.sina.com.cn/xueqian/': 7134,  # 新浪新闻
        'http://baby.sina.com.cn/kid/': 7135,  # 新浪新闻
        'http://baby.sina.com.cn/wemedia/': 7136,  # 新浪新闻
        'http://baby.sina.com.cn/wemedia/ask/': 7137,  # 新浪新闻
        'http://baby.sina.com.cn/wemedia/edu/': 7138,  # 新浪新闻
        'http://city.sina.com.cn/': 7139,  # 新浪新闻
        'http://city.sina.com.cn/focus/n/list.html': 7140,  # 新浪新闻
        'http://city.sina.com.cn/travel/e/list.html': 7141,  # 新浪新闻
        'http://city.sina.com.cn/city/f/teseChina/index.shtml': 7142,  # 新浪新闻
        'https://finance.sina.com.cn/': 7143,  # 新浪新闻
        'https://finance.sina.com.cn/stock/': 7144,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/mkt/': 7145,  # 新浪新闻
        'http://finance.sina.com.cn/roll/index.d.html?cid=56589&page=1': 7146,  # 新浪新闻
        'http://finance.sina.com.cn/roll/index.d.html?cid=56588': 7147,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/moneyflow/#sczjlx': 7148,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/mkt/#chgn_700532': 7149,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/corp/view/vCB_BulletinGather.php?stock_str=&gg_date=&ftype=0': 7150,
        # 新浪新闻
        'http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/lastest/index.phtml': 7151,  # 新浪新闻
        'http://finance.sina.com.cn/roll/index.d.html?cid=56592&page=1': 7152,  # 新浪新闻
        'http://finance.sina.com.cn/roll/index.d.html?cid=56615&page=1': 7153,  # 新浪新闻
        'https://finance.sina.com.cn/stock/thirdmarket/': 7154,  # 新浪新闻
        'http://stock.finance.sina.com.cn/option/quotes.html': 7155,  # 新浪新闻
        'http://live.finance.sina.com.cn/': 7156,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml': 7157,  # 新浪新闻
        'http://finance.sina.com.cn/stock/newstock/': 7158,  # 新浪新闻
        'http://finance.sina.com.cn/stock/hkstock/': 7159,  # 新浪新闻
        'https://finance.sina.com.cn/stock/usstock/': 7160,  # 新浪新闻
        'https://finance.sina.com.cn/fund/': 7161,  # 新浪新闻
        'http://finance.sina.com.cn/roll/index.d.html?cid=56907&page=1': 7162,  # 新浪新闻
        'http://vip.stock.finance.sina.com.cn/fund_center/index.html': 7163,  # 新浪新闻
        'http://finance.sina.com.cn/money/fund/filter/#': 7164,  # 新浪新闻
        'https://finance.sina.com.cn/futuremarket/': 7165,  # 新浪新闻
        'https://finance.sina.com.cn/forex/': 7166,  # 新浪新闻
        'https://finance.sina.com.cn/nmetal/': 7167,  # 新浪新闻
        'http://finance.sina.com.cn/bond/': 7168,  # 新浪新闻
        'http://finance.sina.com.cn/money/': 7169,  # 新浪新闻
        'http://finance.sina.com.cn/money/bank/': 7170,  # 新浪新闻
        'http://finance.sina.com.cn/money/insurance/': 7171,  # 新浪新闻
        'http://finance.sina.com.cn/trust/': 7172,  # 新浪新闻
        'http://finance.sina.com.cn/stock/kechuangban/': 7173,  # 新浪新闻
        'http://finance.sina.com.cn/esg/': 7174,  # 新浪新闻
        'http://blog.sina.com.cn/lm/stock/': 7175,  # 新浪新闻
        'http://guba.sina.com.cn/': 7176,  # 新浪新闻
        'http://finance.sina.com.cn/meeting/': 7177,  # 新浪新闻
        'https://ent.sina.com.cn/': 7178,  # 新浪新闻
        'https://ent.sina.com.cn/star/': 7179,  # 新浪新闻
        'http://ent.sina.com.cn/weibo/': 7180,  # 新浪新闻
        'https://ent.sina.com.cn/film/': 7181,  # 新浪新闻
        'https://ent.sina.com.cn/tv/': 7182,  # 新浪新闻
        'https://ent.sina.com.cn/zongyi/': 7183,  # 新浪新闻
        'http://yue.sina.com.cn/': 7184,  # 新浪新闻
        'http://ent.sina.com.cn/xiju/': 7185,  # 新浪新闻
        'http://ent.sina.com.cn/hr/': 7186,  # 新浪新闻
        'http://ent.sina.com.cn/video/#309922584': 7187,  # 新浪新闻
        'https://ent.sina.com.cn/korea/': 7188,  # 新浪新闻
        'http://ent.sina.com.cn/hollywood/': 7189,  # 新浪新闻
        'http://ent.sina.com.cn/zt/': 7190,  # 新浪新闻
        'http://ent.sina.com.cn/hotnews/ent/Daily/': 7191,  # 新浪新闻
        'http://ent.sina.com.cn/rollnews.shtml#pageid=382&lid=2990&k=&num=50&page=1': 7192,  # 新浪新闻
        'http://video.sina.com.cn/': 7193,  # 新浪新闻
        'http://news.video.sina.com.cn/#308920412': 7194,  # 新浪新闻
        'http://video.sina.com.cn/topic/': 7195,  # 新浪新闻
        'http://vr.sina.com.cn/': 7196,  # 新浪新闻
        'http://edu.sina.com.cn/': 7197,  # 新浪新闻
        'http://edu.sina.com.cn/gaokao/': 7198,  # 新浪新闻
        'http://edu.sina.com.cn/zxx/': 7199,  # 新浪新闻
        'http://edu.sina.com.cn/bschool/': 7200,  # 新浪新闻
        'http://edu.sina.com.cn/kids/': 7201,  # 新浪新闻
        'http://edu.sina.com.cn/cpa/': 7202,  # 新浪新闻
        'http://edu.sina.com.cn/a/': 7203,  # 新浪新闻
        'http://edu.sina.com.cn/ischool/': 7204,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80448': 7205,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80530': 7206,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80533': 7207,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80537': 7208,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80532': 7209,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80534': 7210,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80535': 7211,  # 新浪新闻
        'http://edu.sina.com.cn/yimin/': 7212,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/jzkt/': 7213,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/2018shengdian/': 7214,  # 新浪新闻
        'http://edu.sina.com.cn/ischool/gjxxzx/': 7215,  # 新浪新闻
        'http://edu.sina.com.cn/edugongyi/': 7216,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/eduweekly/': 7217,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/xgkp/': 7218,  # 新浪新闻
        'http://edu.sina.com.cn/original/hygc/': 7219,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/zzzs/': 7220,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/yikao2019/': 7221,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80460': 7222,  # 新浪新闻
        'http://edu.sina.com.cn/other/roll.d.html?cat=80462': 7223,  # 新浪新闻
        'http://edu.sina.com.cn/zt_d/qbj/#274589378': 7224,  # 新浪新闻
        'https://gongyi.sina.com.cn/': 7225,  # 新浪新闻
        'https://gongyi.sina.com.cn/gyzx/pl.html': 7226,  # 新浪新闻
        'https://gongyi.sina.com.cn/search.html': 7227,  # 新浪新闻
        'https://gongyi.sina.com.cn/gyzx/qy.html': 7228,  # 新浪新闻
        'http://fo.sina.com.cn/': 7229,  # 新浪新闻
        'http://fo.sina.com.cn/blog/': 7230,  # 新浪新闻
        'http://fo.sina.com.cn/veg/': 7231,  # 新浪新闻
        'http://travel.sina.com.cn/': 7232,  # 新浪新闻
        'http://travel.sina.com.cn/news/': 7233,  # 新浪新闻
        'http://travel.sina.com.cn/video/': 7234,  # 新浪新闻
        'http://travel.sina.com.cn/hdphoto/': 7235,  # 新浪新闻
        'http://travel.sina.com.cn/lvyou/': 7236,  # 新浪新闻
        'https://tech.sina.com.cn/': 7237,  # 新浪新闻
        'https://tech.sina.com.cn/internet/': 7238,  # 新浪新闻
        'https://tech.sina.com.cn/tele/': 7239,  # 新浪新闻
        'https://tech.sina.com.cn/it/': 7240,  # 新浪新闻
        'http://chuangye.sina.com.cn/': 7241,  # 新浪新闻
        'http://5g.sina.com.cn/': 7242,  # 新浪新闻
        'http://tech.sina.com.cn/notebook/': 7243,  # 新浪新闻
        'http://tech.sina.com.cn/digital/': 7244,  # 新浪新闻
        'http://shiqu.sina.com.cn/': 7245,  # 新浪新闻
        'https://mobile.sina.com.cn/': 7246,  # 新浪新闻
        'http://tech.sina.com.cn/mobile/tag/%E6%96%B0%E6%9C%BA%E6%9B%9D%E5%85%89': 7247,  # 新浪新闻
        'http://tech.sina.com.cn/mobile/tag/%E8%AF%84%E6%B5%8B%E8%A7%A3%E6%9E%90': 7248,  # 新浪新闻
        'http://tech.sina.com.cn/mobile/tag/%E9%80%89%E8%B4%AD%E6%8C%87%E5%8D%97': 7249,  # 新浪新闻
        'http://tech.sina.com.cn/mobile/tag/%E6%9C%BA%E6%99%BA%E5%A0%82': 7250,  # 新浪新闻
        'http://tech.sina.com.cn/apple/': 7251,  # 新浪新闻
        'http://zhongce.sina.com.cn/': 7252,  # 新浪新闻
        'https://tech.sina.com.cn/discovery/': 7253,  # 新浪新闻
        'http://tech.sina.com.cn/scientist/': 7254,  # 新浪新闻
        'https://tech.sina.com.cn/roll/rollnews.shtml#pageid=372&lid=2431&k=&num=50&page=1': 7255,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/animal/': 7256,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/civilization/': 7257,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/space/': 7258,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/life/': 7259,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/live/': 7260,  # 新浪新闻
        'http://tech.sina.com.cn/discovery/invention/': 7261,  # 新浪新闻
        'https://auto.sina.com.cn/': 7262,  # 新浪新闻
        'http://auto.sina.com.cn/newcar/': 7263,  # 新浪新闻
        'http://auto.sina.com.cn/newcar/x/': 7264,  # 新浪新闻
        'http://auto.sina.com.cn/newcar/h/': 7265,  # 新浪新闻
        'http://auto.sina.com.cn/newcar/d/': 7266,  # 新浪新闻
        'http://auto.sina.com.cn/newcar/j/': 7267,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/xinchepandian/': 7268,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/jiemaxinche/': 7269,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/xinchejiexi/': 7270,  # 新浪新闻
        'http://auto.sina.com.cn/estation/': 7271,  # 新浪新闻
        'http://auto.sina.com.cn/review/': 7272,  # 新浪新闻
        'http://auto.sina.com.cn/review/tiyan/': 7273,  # 新浪新闻
        'http://db.auto.sina.com.cn/car_manual/': 7274,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/SUVshijiapingce/': 7275,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/haiwaishijia/': 7276,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/9463/': 7277,  # 新浪新闻
        'http://auto.sina.com.cn/guide/': 7278,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/review/xiangduilun/': 7279,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/xinchejingzhenglifenxi/': 7280,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/gouchebangbangmang/': 7281,  # 新浪新闻
        'http://auto.sina.com.cn/guide/chexing/': 7282,  # 新浪新闻
        'http://auto.sina.com.cn/guide/hangqing/': 7283,  # 新浪新闻
        'http://db.auto.sina.com.cn/': 7284,  # 新浪新闻
        'http://db.auto.sina.com.cn/estation/': 7285,  # 新浪新闻
        'http://db.auto.sina.com.cn/pk/': 7286,  # 新浪新闻
        'http://db.auto.sina.com.cn/price/': 7287,  # 新浪新闻
        'http://db.auto.sina.com.cn/photo/': 7288,  # 新浪新闻
        'http://auto.sina.com.cn/video/': 7289,  # 新浪新闻
        'http://auto.sina.com.cn/live/index.d.html': 7290,  # 新浪新闻
        'http://auto.sina.com.cn/video/qchkjsp/': 7291,  # 新浪新闻
        'http://auto.sina.com.cn/video/gcbbmsp/': 7292,  # 新浪新闻
        'http://auto.sina.com.cn/news/': 7293,  # 新浪新闻
        'http://auto.sina.com.cn/news/hy/': 7294,  # 新浪新闻
        'http://auto.sina.com.cn/news/f/': 7295,  # 新浪新闻
        'http://auto.sina.com.cn/zhishu/': 7296,  # 新浪新闻
        'http://auto.sina.com.cn/zhishu/#br_0': 7297,  # 新浪新闻
        'http://auto.sina.com.cn/zhishu/#cr_0': 7298,  # 新浪新闻
        'http://auto.sina.com.cn/zhishu/#sr_0': 7299,  # 新浪新闻
        'http://auto.sina.com.cn/zhishu/#pr_0': 7300,  # 新浪新闻
        'http://auto.sina.com.cn/jishu/': 7301,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/jishu/jishujiedu/': 7302,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/biaoqian/jishuheikeji/': 7303,  # 新浪新闻
        'http://db.auto.sina.com.cn/tags/jishu/gongchangtanmi/': 7304,  # 新浪新闻
        'http://auto.sina.com.cn/yx/': 7305,  # 新浪新闻
        'http://auto.sina.com.cn/yx/yd/': 7306,  # 新浪新闻
        'http://db.auto.sina.com.cn/youliao/lists': 7307,  # 新浪新闻
        'http://auto.sina.com.cn/yx/ys/': 7308,  # 新浪新闻
        'https://feedback.auto.sina.com.cn/': 7309,  # 新浪新闻
        'https://bj.leju.com/#source=pc_sina_tydh1&source_ext=pc_sina': 7310,  # 新浪新闻
        'https://news.leju.com/#csfp=bj&wt_source=pc_sy_dh': 7311,  # 新浪新闻
        'https://news.leju.com/shuju/#wt_source=pc_ljnews_dh': 7312,  # 新浪新闻
        'https://news.leju.com/zhengce/#wt_source=pc_ljnews_dh': 7313,  # 新浪新闻
        'https://news.leju.com/renwu/#wt_source=pc_ljnews_dh': 7314,  # 新浪新闻
        'https://news.leju.com/gongsi/#wt_source=pc_ljnews_dh': 7315,  # 新浪新闻
        'https://news.leju.com/tudi/#wt_source=pc_ljnews_dh': 7316,  # 新浪新闻
        'https://live.leju.com/house/bj/#wt_source=pc_ljnews_dh': 7317,  # 新浪新闻
        'https://www.xhwhouse.com/news/#wt_source=pc_ljnews_dh': 7318,  # 新浪新闻
        'https://house.leju.com/bj/search/#wt_source=pc_sy_dh': 7319,  # 新浪新闻
        'https://bj.esf.leju.com/#bi=tg&type=house-pc&pos=index-dh&wt_source=pc_sy_dh': 7320,  # 新浪新闻
        'https://bj.7gz.com/?utm_source=sina&utm_medium=snlj&utm_campaign=ljhp_xx_nav6004&wt_source=pc_sy_dh': 7321,
        # 新浪新闻
        'https://jiaju.sina.com.cn/#wt_source=pc_sy_dh': 7322,  # 新浪新闻
        'https://www.xhaiwai.com/#wt_source=pc_sy_dh': 7323,  # 新浪新闻
        'http://jiaju.sina.com.cn/': 7324,  # 新浪新闻
        'http://news.jiaju.sina.com.cn/list-jiaju-a50b70': 7325,  # 新浪新闻
        'http://news.jiaju.sina.com.cn/list-jiaju-a50': 7326,  # 新浪新闻
        'http://photo.sina.com.cn/': 7327,  # 新浪新闻
        'http://slide.photo.sina.com.cn/': 7328,  # 新浪新闻
        'http://photo.sina.com.cn/wit/': 7329,  # 新浪新闻
        'http://photo.sina.com.cn/ygdbns/': 7330,  # 新浪新闻
        'http://photo.sina.com.cn/newyouth/': 7331,  # 新浪新闻
        'http://news.sina.com.cn/politician/': 7332,  # 新浪新闻
        'http://aipai.sina.com.cn/index/view/': 7333,  # 新浪新闻
        'http://photo.sina.com.cn/roll/index.d.html': 7334,  # 新浪新闻
        'http://news.sina.com.cn/zt_d/photocamp5/': 7335,  # 新浪新闻
        'http://book.sina.com.cn/': 7336,  # 新浪新闻
        'http://vip.book.sina.com.cn/weibobook?pos=202041': 7337,  # 新浪新闻
        'http://vip.book.sina.com.cn/weibobook/man.php?pos=202042': 7338,  # 新浪新闻
        'http://vip.book.sina.com.cn/weibobook/girl.php?pos=202043': 7339,  # 新浪新闻
        'http://vip.book.sina.com.cn/weibobook/publish.php?pos=202044': 7340,  # 新浪新闻
        'http://vip.book.sina.com.cn/weibobook/rank.php?pos=202065': 7341,  # 新浪新闻
        'http://sifa.sina.com.cn/': 7342,  # 新浪新闻
        'http://sifa.sina.com.cn/news/': 7343,  # 新浪新闻
        'http://sifa.sina.com.cn/publicity/': 7344,  # 新浪新闻
        'http://news.sina.com.cn/2016/tsspzuigaofa.shtml': 7345,  # 新浪新闻
        'http://news.sina.com.cn/sf/sqjz/': 7346,  # 新浪新闻
        'http://sifa.sina.com.cn/zhuanti/2015/tiaojie.html': 7347,  # 新浪新闻
        'http://news.sina.com.cn/sf/zt/yz/': 7348,  # 新浪新闻
        'http://sifa.sina.com.cn/briefing/index.shtml': 7349,  # 新浪新闻
        'https://games.sina.com.cn/': 7350,  # 新浪新闻
        'http://jr.sina.com.cn/web/main/index?source=sinatop': 7351,  # 新浪新闻
        'http://fund.sina.com.cn/fund/web/index': 7352,  # 新浪新闻
        'http://gov.sina.com.cn/': 7353,  # 新浪新闻
        'http://gov.sina.com.cn/#beijingNews': 7354,  # 新浪新闻
        'http://game.weibo.com/': 7355,  # 新浪新闻
        'http://game.weibo.com/search?tag=new': 7356,  # 新浪新闻
        'http://news.sina.com.cn/zt_nys/nxw0312/#282402036': 7357,  # 新浪新闻

    }

    # https://news.sina.com.cn/c/2019-10-22/doc-iicezzrr4082502.shtml
    # http://news.sina.com.cn/w/zg/2016-07-09/doc-ifxtwihp9896306.shtml
    # http://photo.sina.com.cn/newyouth/doc-iicezzrr4150612.shtml
    # http://dj.sina.com.cn/article/icezuev3968309.shtml
    # http://jiaju.sina.com.cn/news/20190505/6530682199598235820.shtml
    # http://slide.news.sina.com.cn/s/slide_1_86058_409744.html

    rules = (

        Rule(LinkExtractor(allow=r'sina.com.cn/.*\d{4}\.shtml',
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'sina.com.cn/.*\d{4}\.shtml',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        #http://www.mrjjxw.com/articles/2019-10-21/1380159.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='main-title']").extract_first("")
            pubtime = Pubtime(xp("//span[@class='date']/text()").extract_first(""))
            content_div = xp("//div[@id='article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='source']/text()").extract_first("")
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):

     #http://edu.sina.com.cn/official/2019-10-27/doc-iicezuev5137438.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='main-title']").extract_first("")
            pubtime = Pubtime(xp("//span[@class='date']/text()").extract_first(""))
            content_div = xp("//div[@id='artibody']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='source content-color']/text()").extract_first("")
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_3(self, response):
        # http://www.mrjjxw.com/articles/2019-10-21/1380159.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='main-title']").extract_first("")
            pubtime = Pubtime(xp("//span[@class='date']/text()").extract_first(""))
            content_div = xp("//div[@id='article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], needvideo=True)
            origin_name = xp("//a[@class='source']/text()").extract_first("")
        except:
            return self.parse_item_4(response)
        # except Exception as e:
        #     return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_4(self, response):

     #http://edu.sina.com.cn/official/2019-10-27/doc-iicezuev5137438.shtml
     # http://edu.sina.com.cn/official/2019-10-27/doc-iicezuev5137438.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='main-title']").extract_first("")
            pubtime = Pubtime(xp("//span[@class='titer']/text()").extract_first(""))
            content_div = xp("//div[@id='artibody']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            try:
                origin_name = xp("//span[@class='source']/text()").extract_first("")
            except:
                origin_name = xp("//a[@class='ent1 fred']/text()").extract_first("")
        except:
            return self.parse_item_5(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_5(self, response):

     # http://slide.mil.news.sina.com.cn/h/slide_8_62085_74264.html图片
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='swp-tit clearfix']/h2").extract_first("")
            pubtime = Pubtime(xp("//em[@class='swpt-time']/text()").extract_first(""))
            content_div = xp("//div[@class='swpt-1013']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = {}
        except:
            return self.parse_item_6(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_6(self, response):

     # http://dj.sina.com.cn/article/icezuev7502420.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='acticle_top']/h1").extract_first("")
            pubtime = Pubtime(xp("//span[@class='timer']/text()").extract_first(""))
            content_div = xp("//div[@id='artibody']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//span[@class='Author']/text()").extract_first("")
        except:
            return self.parse_item_7(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_7(self, response):

     # https://tech.sina.com.cn/mobile/n/n/2019-11-05/doc-iicezzrr7258764.shtml
     # http://sports.sina.com.cn/zl/football/2019-11-04/zldoc-iicezzrr7047188.shtml
     # http://travel.sina.com.cn/outbound/pages/2019-11-04/detail-iicezuev7074833.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@id='artibodyTitle']").extract_first("")
            try:
                pubtime = Pubtime(xp("//span[@id='pub_date']/text()").extract_first(""))
            except:
                pubtime = Pubtime(xp("//span[@class='time-source']/text()").extract_first(""))
            content_div = xp("//div[@id='artibody']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            try:
                origin_name = xp("//span[@id='author_ename']/a").extract_first("")
            except:
                origin_name = xp("//a[@id='media_comment']/text()").extract_first("")

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )
#视频
    # def parse_item_9(self, response):
    #
    #  # https://tech.sina.com.cn/mobile/n/n/2019-11-05/doc-iicezzrr7258764.shtml
    #  # http://sports.sina.com.cn/zl/football/2019-11-04/zldoc-iicezzrr7047188.shtml
    #     xp = response.xpath
    #     try:
    #         title = self.get_page_title(response).split('_')[0] or xp("//div[@class='Vd_titBox clearfix']/h2").extract_first("")
    #         pubtime = Pubtime(xp("//p[@class='from']/span[1]/em/text()").extract_first(""))
    #         content_div = xp("//script[@type='text/javascript']/text()").extract_first("")
    #         # http://vdata.tool.hexun.com/2019-11-01/199092185.mp4
    #         videos = re.findall(r'http://.*?\.mp4', content_div)[0]
    #         content = '<div>#{{1}}#</div>'
    #         # content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], )
    #         origin_name = xp("//p[@class='from']/span[2]/a/text()").extract_first("")
    #     except Exception as e:
    #         return self.produce_debugitem(response, "xpath error")
    #
    #     return self.produce_item(
    #         response=response,
    #         title=title,
    #         pubtime=pubtime,
    #         origin_name=origin_name,
    #         content=content,
    #         # media=media,
    #         videos=videos,
    #
    #     )

