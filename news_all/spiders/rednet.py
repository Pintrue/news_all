# -*- coding: utf-8 -*-
# @Time   : 2019/10/22 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: rednet_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re


class Rednet(NewsRCSpider):
    name = 'rednet'

    # 红网 ==》 补充全站采集
    mystart_urls = {
        'http://www.rednet.cn/': 5390,   #  红网
        'https://hn.rednet.cn/': 5391,   #  红网
        'https://hn.rednet.cn/channel/7397.html': 5392,   #  红网
        'https://hn.rednet.cn/channel/7542.html': 5393,   #  红网
        'https://hn.rednet.cn/channel/7398.html': 5394,   #  红网
        'https://hn.rednet.cn/channel/7540.html': 5395,   #  红网
        'https://hn.rednet.cn/channel/7400.html': 5396,   #  红网
        'https://hn.rednet.cn/channel/7399.html': 5397,   #  红网
        'https://news.rednet.cn/channel/8394.html': 5398,   #  红网
        'https://news.rednet.cn/channel/7621.html': 5399,   #  红网
        'https://news.rednet.cn/channel/7622.html': 5400,   #  红网
        'https://gov.rednet.cn/channel/8463.html': 5401,   #  红网
        'https://gov.rednet.cn/channel/8471.html': 5402,   #  红网
        'https://gov.rednet.cn/channel/8472.html': 5403,   #  红网
        'https://gov.rednet.cn/channel/8470.html': 5404,   #  红网
        'https://gov.rednet.cn/channel/8464.html': 5405,   #  红网
        'https://gov.rednet.cn/channel/8469.html': 5406,   #  红网
        'https://gov.rednet.cn/channel/8473.html': 5407,   #  红网
        'https://gov.rednet.cn/channel/8465.html': 5408,   #  红网
        'http://photo.rednet.cn/': 5409,   #  红网
        'http://photo.rednet.cn/space.php?do=home': 5410,   #  红网
        'http://photo.rednet.cn/space.php?do=album&view=all&orderby=dateline': 5411,   #  红网
        'http://photo.rednet.cn/space.php?do=event': 5412,   #  红网
        'http://photo.rednet.cn/space.php?do=event&view=recommend': 5413,   #  红网
        'http://photo.rednet.cn/space.php?do=event&view=city': 5414,   #  红网
        'http://photo.rednet.cn/space.php?uid=0&do=event&view=me': 5415,   #  红网
        'http://photo.rednet.cn/space.php?do=blog&view=all&orderby=dateline': 5416,   #  红网
        'http://photo.rednet.cn/space.php?do=mtag': 5417,   #  红网
        'http://video.rednet.cn/html/list/11.html': 5418,   #  红网
        'http://video.rednet.cn/channel/11078.html': 5419,   #  红网
        'http://video.rednet.cn/channel/11075.html': 5420,   #  红网
        'http://video.rednet.cn/channel/11076.html': 5421,   #  红网
        'http://video.rednet.cn/channel/11081.html': 5422,   #  红网
        'http://video.rednet.cn/channel/11079.html': 5423,   #  红网
        'http://video.rednet.cn/html/list/20.html': 5424,   #  红网
        'http://video.rednet.cn/html/list/21.html': 5425,   #  红网
        'http://video.rednet.cn/html/list/22.html': 5426,   #  红网
        'http://video.rednet.cn/html/list/19.html': 5427,   #  红网
        'https://book.rednet.cn/': 5428,   #  红网
        'https://book.rednet.cn/channel/8117.html': 5429,   #  红网
        'https://book.rednet.cn/channel/8106.html': 5430,   #  红网
        'https://wh.rednet.cn/': 5431,   #  红网
        'https://wh.rednet.cn/channel/7959.html': 5432,   #  红网
        'https://wh.rednet.cn/channel/7963.html': 5433,   #  红网
        'https://wh.rednet.cn/channel/7960.html': 5434,   #  红网
        'https://wh.rednet.cn/channel/7956.html': 5435,   #  红网
        'https://wh.rednet.cn/channel/7965.html': 5436,   #  红网
        'https://wh.rednet.cn/channel/7962.html': 5437,   #  红网
        'https://wh.rednet.cn/channel/7964.html': 5438,   #  红网
        'https://wh.rednet.cn/channel/7966.html': 5439,   #  红网
        'https://keji.rednet.cn/': 5440,   #  红网
        'https://keji.rednet.cn/channel/1616.html': 5441,   #  红网
        'https://keji.rednet.cn/channel/1617.html': 5442,   #  红网
        'https://keji.rednet.cn/channel/1615.html': 5443,   #  红网
        'https://keji.rednet.cn/channel/1618.html': 5444,   #  红网
        'https://keji.rednet.cn/channel/1622.html': 5445,   #  红网
        'https://keji.rednet.cn/channel/1619.html': 5446,   #  红网
        'https://keji.rednet.cn/channel/1620.html': 5447,   #  红网
        'https://keji.rednet.cn/channel/1621.html': 5448,   #  红网
        'https://keji.rednet.cn/channel/1626.html': 5449,   #  红网
        'https://keji.rednet.cn/channel/1673.html': 5450,   #  红网
        'https://keji.rednet.cn/channel/1627.html': 5451,   #  红网
        'https://keji.rednet.cn/channel/1628.html': 5452,   #  红网
        'https://hnny.rednet.cn/': 5453,   #  红网
        'https://hnny.rednet.cn/channel/1655.html': 5454,   #  红网
        'https://hnny.rednet.cn/channel/1656.html': 5455,   #  红网
        'https://hnny.rednet.cn/channel/1657.html': 5456,   #  红网
        'https://hnny.rednet.cn/channel/1658.html': 5457,   #  红网
        'https://hnny.rednet.cn/channel/1658.html': 5458,   #  红网
        'https://hnny.rednet.cn/channel/1663.html': 5459,   #  红网
        'https://hnny.rednet.cn/channel/1659.html': 5460,   #  红网
        'https://hnny.rednet.cn/channel/1660.html': 5461,   #  红网
        'https://hnny.rednet.cn/channel/1665.html': 5462,   #  红网
        'https://hnny.rednet.cn/channel/1661.html': 5463,   #  红网
        'https://hnny.rednet.cn/channel/1668.html': 5464,   #  红网
        'https://hnny.rednet.cn/channel/1667.html': 5465,   #  红网
        'https://gongyi.rednet.cn/': 5466,   #  红网
        'https://gongyi.rednet.cn/channel/9142.html': 5467,   #  红网
        'https://gongyi.rednet.cn/channel/10499.html': 5468,   #  红网
        'https://gongyi.rednet.cn/channel/9141.html': 5469,   #  红网
        'https://xc.rednet.cn/': 5470,   #  红网
        'https://xc.rednet.cn/channel/8180.html': 5471,   #  红网
        'https://xc.rednet.cn/channel/8172.html': 5472,   #  红网
        'https://xc.rednet.cn/channel/8171.html': 5473,   #  红网
        'https://xc.rednet.cn/channel/8168.html': 5474,   #  红网
        'https://xc.rednet.cn/channel/8182.html': 5475,   #  红网
        'https://xc.rednet.cn/channel/8181.html': 5476,   #  红网
        'https://xc.rednet.cn/channel/8176.html': 5477,   #  红网
        'https://xc.rednet.cn/channel/8177.html': 5478,   #  红网
        'https://city.rednet.cn/': 5479,   #  红网
        'https://hn.rednet.cn/channel/7401.html': 5480,   #  红网
        'https://hn.rednet.cn/channel/7397.html': 5481,   #  红网
        'https://hn.rednet.cn/channel/7542.html': 5482,   #  红网
        'https://hn.rednet.cn/channel/7398.html': 5483,   #  红网
        'https://hn.rednet.cn/channel/7540.html': 5484,   #  红网
        'https://hn.rednet.cn/channel/7400.html': 5485,   #  红网
        'https://hn.rednet.cn/channel/7399.html': 5486,   #  红网
        'https://hn.rednet.cn/channel/7418.html': 5487,   #  红网
        'https://hn.rednet.cn/channel/7419.html': 5488,   #  红网
        'https://hn.rednet.cn/channel/7417.html': 5489,   #  红网
        'https://hn.rednet.cn/channel/7420.html': 5490,   #  红网
        'https://hn.rednet.cn/channel/7421.html': 5491,   #  红网
        'https://hn.rednet.cn/channel/7424.html': 5492,   #  红网
        'https://hn.rednet.cn/channel/7423.html': 5493,   #  红网
        'https://hn.rednet.cn/channel/7422.html': 5494,   #  红网
        'https://hn.rednet.cn/channel/7425.html': 5495,   #  红网
        'https://hn.rednet.cn/channel/7429.html': 5496,   #  红网
        'https://hn.rednet.cn/channel/7426.html': 5497,   #  红网
        'https://hn.rednet.cn/channel/7427.html': 5498,   #  红网
        'https://hn.rednet.cn/channel/7428.html': 5499,   #  红网
        'https://hn.rednet.cn/channel/7431.html': 5500,   #  红网
        'https://hn.rednet.cn/channel/7430.html': 5501,   #  红网
        'https://hn.rednet.cn/channel/7438.html': 5502,   #  红网
        'https://hn.rednet.cn/channel/7437.html': 5503,   #  红网
        'https://hn.rednet.cn/channel/7436.html': 5504,   #  红网
        'https://hn.rednet.cn/channel/7439.html': 5505,   #  红网
        'https://hn.rednet.cn/channel/7440.html': 5506,   #  红网
        'https://hn.rednet.cn/channel/7442.html': 5507,   #  红网
        'https://hn.rednet.cn/channel/7441.html': 5508,   #  红网
        'https://hn.rednet.cn/channel/7443.html': 5509,   #  红网
        'https://hn.rednet.cn/channel/7541.html': 5510,   #  红网
        'https://hn.rednet.cn/channel/7447.html': 5511,   #  红网
        'https://hn.rednet.cn/channel/7446.html': 5512,   #  红网
        'https://hn.rednet.cn/channel/7445.html': 5513,   #  红网
        'https://hn.rednet.cn/channel/7444.html': 5514,   #  红网
        'https://hn.rednet.cn/channel/7448.html': 5515,   #  红网
        'https://hn.rednet.cn/channel/7449.html': 5516,   #  红网
        'https://hn.rednet.cn/channel/7450.html': 5517,   #  红网
        'https://hn.rednet.cn/channel/7451.html': 5518,   #  红网
        'https://hn.rednet.cn/channel/7454.html': 5519,   #  红网
        'https://hn.rednet.cn/channel/7453.html': 5520,   #  红网
        'https://hn.rednet.cn/channel/7452.html': 5521,   #  红网
        'https://hn.rednet.cn/channel/7455.html': 5522,   #  红网
        'https://hn.rednet.cn/channel/7456.html': 5523,   #  红网
        'https://hn.rednet.cn/channel/7457.html': 5524,   #  红网
        'https://hn.rednet.cn/channel/7458.html': 5525,   #  红网
        'https://hn.rednet.cn/channel/7460.html': 5526,   #  红网
        'https://hn.rednet.cn/channel/7462.html': 5527,   #  红网
        'https://hn.rednet.cn/channel/7465.html': 5528,   #  红网
        'https://hn.rednet.cn/channel/7466.html': 5529,   #  红网
        'https://hn.rednet.cn/channel/7461.html': 5530,   #  红网
        'https://hn.rednet.cn/channel/7463.html': 5531,   #  红网
        'https://hn.rednet.cn/channel/7464.html': 5532,   #  红网
        'https://hn.rednet.cn/channel/7467.html': 5533,   #  红网
        'https://hn.rednet.cn/channel/7459.html': 5534,   #  红网
        'https://hn.rednet.cn/channel/7469.html': 5535,   #  红网
        'https://hn.rednet.cn/channel/7468.html': 5536,   #  红网
        'https://hn.rednet.cn/channel/7470.html': 5537,   #  红网
        'https://hn.rednet.cn/channel/7473.html': 5538,   #  红网
        'https://hn.rednet.cn/channel/7476.html': 5539,   #  红网
        'https://hn.rednet.cn/channel/7474.html': 5540,   #  红网
        'https://hn.rednet.cn/channel/7475.html': 5541,   #  红网
        'https://hn.rednet.cn/channel/7472.html': 5542,   #  红网
        'https://hn.rednet.cn/channel/7471.html': 5543,   #  红网
        'https://hn.rednet.cn/channel/7549.html': 5544,   #  红网
        'https://hn.rednet.cn/channel/7477.html': 5545,   #  红网
        'https://hn.rednet.cn/channel/7478.html': 5546,   #  红网
        'https://hn.rednet.cn/channel/7481.html': 5547,   #  红网
        'https://hn.rednet.cn/channel/7480.html': 5548,   #  红网
        'https://hn.rednet.cn/channel/7482.html': 5549,   #  红网
        'https://hn.rednet.cn/channel/7479.html': 5550,   #  红网
        'https://hn.rednet.cn/channel/7483.html': 5551,   #  红网
        'https://hn.rednet.cn/channel/7487.html': 5552,   #  红网
        'https://hn.rednet.cn/channel/7486.html': 5553,   #  红网
        'https://hn.rednet.cn/channel/7484.html': 5554,   #  红网
        'https://hn.rednet.cn/channel/7485.html': 5555,   #  红网
        'https://hn.rednet.cn/channel/7488.html': 5556,   #  红网
        'https://hn.rednet.cn/channel/7489.html': 5557,   #  红网
        'https://hn.rednet.cn/channel/7495.html': 5558,   #  红网
        'https://hn.rednet.cn/channel/7494.html': 5559,   #  红网
        'https://hn.rednet.cn/channel/7491.html': 5560,   #  红网
        'https://hn.rednet.cn/channel/7492.html': 5561,   #  红网
        'https://hn.rednet.cn/channel/7493.html': 5562,   #  红网
        'https://hn.rednet.cn/channel/7496.html': 5563,   #  红网
        'https://hn.rednet.cn/channel/7490.html': 5564,   #  红网
        'https://hn.rednet.cn/channel/7497.html': 5565,   #  红网
        'https://hn.rednet.cn/channel/7498.html': 5566,   #  红网
        'https://hn.rednet.cn/channel/7507.html': 5567,   #  红网
        'https://hn.rednet.cn/channel/7500.html': 5568,   #  红网
        'https://hn.rednet.cn/channel/7506.html': 5569,   #  红网
        'https://hn.rednet.cn/channel/7503.html': 5570,   #  红网
        'https://hn.rednet.cn/channel/7504.html': 5571,   #  红网
        'https://hn.rednet.cn/channel/7501.html': 5572,   #  红网
        'https://hn.rednet.cn/channel/7505.html': 5573,   #  红网
        'https://hn.rednet.cn/channel/7502.html': 5574,   #  红网
        'https://hn.rednet.cn/channel/7499.html': 5575,   #  红网
        'https://hn.rednet.cn/channel/7509.html': 5576,   #  红网
        'https://hn.rednet.cn/channel/7508.html': 5577,   #  红网
        'https://hn.rednet.cn/channel/7510.html': 5578,   #  红网
        'https://hn.rednet.cn/channel/7514.html': 5579,   #  红网
        'https://hn.rednet.cn/channel/7517.html': 5580,   #  红网
        'https://hn.rednet.cn/channel/7516.html': 5581,   #  红网
        'https://hn.rednet.cn/channel/7515.html': 5582,   #  红网
        'https://hn.rednet.cn/channel/7512.html': 5583,   #  红网
        'https://hn.rednet.cn/channel/7511.html': 5584,   #  红网
        'https://hn.rednet.cn/channel/7513.html': 5585,   #  红网
        'https://hn.rednet.cn/channel/7518.html': 5586,   #  红网
        'https://hn.rednet.cn/channel/7550.html': 5587,   #  红网
        'https://hn.rednet.cn/channel/7551.html': 5588,   #  红网
        'https://hn.rednet.cn/channel/7519.html': 5589,   #  红网
        'https://hn.rednet.cn/channel/7526.html': 5590,   #  红网
        'https://hn.rednet.cn/channel/7522.html': 5591,   #  红网
        'https://hn.rednet.cn/channel/7523.html': 5592,   #  红网
        'https://hn.rednet.cn/channel/7524.html': 5593,   #  红网
        'https://hn.rednet.cn/channel/7521.html': 5594,   #  红网
        'https://hn.rednet.cn/channel/7530.html': 5595,   #  红网
        'https://hn.rednet.cn/channel/7525.html': 5596,   #  红网
        'https://hn.rednet.cn/channel/7527.html': 5597,   #  红网
        'https://hn.rednet.cn/channel/7529.html': 5598,   #  红网
        'https://hn.rednet.cn/channel/7528.html': 5599,   #  红网
        'https://hn.rednet.cn/channel/7520.html': 5600,   #  红网
        'https://hn.rednet.cn/channel/7539.html': 5601,   #  红网
        'https://hn.rednet.cn/channel/7531.html': 5602,   #  红网
        'https://hn.rednet.cn/channel/7536.html': 5603,   #  红网
        'https://hn.rednet.cn/channel/7537.html': 5604,   #  红网
        'https://hn.rednet.cn/channel/7532.html': 5605,   #  红网
        'https://hn.rednet.cn/channel/7534.html': 5606,   #  红网
        'https://hn.rednet.cn/channel/7533.html': 5607,   #  红网
        'https://hn.rednet.cn/channel/7535.html': 5608,   #  红网
        'https://hn.rednet.cn/channel/7538.html': 5609,   #  红网
        'https://hn.rednet.cn/channel/7432.html': 5610,   #  红网
        'https://hn.rednet.cn/channel/7433.html': 5611,   #  红网
        'https://hn.rednet.cn/channel/7434.html': 5612,   #  红网
        'https://hn.rednet.cn/channel/7435.html': 5613,   #  红网
        'https://ent.rednet.cn/': 5614,   #  红网
        'https://ent.rednet.cn/channel/7916.html': 5615,   #  红网
        'https://ent.rednet.cn/channel/7920.html': 5616,   #  红网
        'https://ent.rednet.cn/channel/7921.html': 5617,   #  红网
        'https://ent.rednet.cn/channel/7922.html': 5618,   #  红网
        'https://ent.rednet.cn/channel/7927.html': 5619,   #  红网
        'https://ent.rednet.cn/channel/7923.html': 5620,   #  红网
        'https://ent.rednet.cn/channel/7926.html': 5621,   #  红网
        'http://zt.rednet.cn/c/zt/4426/': 5622,   #  红网
        'http://zt.rednet.cn/c/zt/4426/4427.htm': 5623,   #  红网
        'http://zt.rednet.cn/c/zt/4426/13050.htm': 5624,   #  红网
        'http://zt.rednet.cn/c/zt/4426/4432.htm': 5625,   #  红网
        'http://zt.rednet.cn/c/zt/4426/4429.htm': 5626,   #  红网
        'http://exchange.rednet.cn/': 5627,   #  红网
        'http://exchange.rednet.cn/channel/299.html': 5628,   #  红网
        'http://exchange.rednet.cn/channel/300.html': 5629,   #  红网
        'http://exchange.rednet.cn/channel/302.html': 5630,   #  红网
        'https://ls.rednet.cn/': 5631,   #  红网
        'https://ls.rednet.cn/channel/7225.html': 5632,   #  红网
        'https://ls.rednet.cn/channel/7226.html': 5633,   #  红网
        'https://ls.rednet.cn/channel/7227.html': 5634,   #  红网
        'https://ls.rednet.cn/channel/7229.html': 5635,   #  红网
        'https://ls.rednet.cn/channel/7228.html': 5636,   #  红网
        'https://ls.rednet.cn/channel/7230.html': 5637,   #  红网
        'https://ls.rednet.cn/channel/7231.html': 5638,   #  红网
        'https://ls.rednet.cn/channel/7233.html': 5639,   #  红网
        'https://ls.rednet.cn/channel/7234.html': 5640,   #  红网
        'https://fupin.rednet.cn/': 5641,   #  红网
        'https://fupin.rednet.cn/channel/7624.html': 5642,   #  红网
        'https://fupin.rednet.cn/channel/7625.html': 5643,   #  红网
        'https://fupin.rednet.cn/channel/7626.html': 5644,   #  红网
        'https://fupin.rednet.cn/channel/7627.html': 5645,   #  红网
        'https://fupin.rednet.cn/channel/7628.html': 5646,   #  红网
        'https://fupin.rednet.cn/channel/7629.html': 5647,   #  红网
        'https://fupin.rednet.cn/channel/7630.html': 5648,   #  红网
        'https://fupin.rednet.cn/channel/7631.html': 5649,   #  红网
        'https://fupin.rednet.cn/channel/7632.html': 5650,   #  红网
        'https://renfang.rednet.cn/': 5651,   #  红网
        'https://renfang.rednet.cn/channel/1696.html': 5652,   #  红网
        'https://renfang.rednet.cn/channel/1697.html': 5653,   #  红网
        'https://renfang.rednet.cn/channel/1700.html': 5654,   #  红网
        'https://renfang.rednet.cn/channel/1698.html': 5655,   #  红网
        'https://renfang.rednet.cn/channel/1702.html': 5656,   #  红网
        'https://renfang.rednet.cn/channel/1699.html': 5657,   #  红网
        'https://renfang.rednet.cn/channel/1701.html': 5658,   #  红网
        'https://renfang.rednet.cn/channel/1703.html': 5659,   #  红网
        'https://ny.rednet.cn/': 5660,   #  红网
        'https://ny.rednet.cn/channel/7611.html': 5661,   #  红网
        'https://ny.rednet.cn/channel/7612.html': 5662,   #  红网
        'https://ny.rednet.cn/channel/7614.html': 5663,   #  红网
        'https://ny.rednet.cn/channel/7615.html': 5664,   #  红网
        'https://ny.rednet.cn/channel/7617.html': 5665,   #  红网
        'https://ny.rednet.cn/channel/7616.html': 5666,   #  红网
        'https://ny.rednet.cn/channel/7619.html': 5667,   #  红网
        'https://ny.rednet.cn/channel/7610.html': 5668,   #  红网
        'https://ny.rednet.cn/channel/7613.html': 5669,   #  红网
        'https://ny.rednet.cn/channel/7620.html': 5670,   #  红网
        'https://pf.rednet.cn/': 5671,   #  红网
        'https://pf.rednet.cn/channel/8339.html': 5672,   #  红网
        'https://pf.rednet.cn/channel/8340.html': 5673,   #  红网
        'https://pf.rednet.cn/channel/8342.html': 5674,   #  红网
        'https://pf.rednet.cn/channel/8349.html': 5675,   #  红网
        'https://pf.rednet.cn/channel/8351.html': 5676,   #  红网
        'https://pf.rednet.cn/channel/8344.html': 5677,   #  红网
        'https://pf.rednet.cn/channel/8343.html': 5678,   #  红网
        'https://pf.rednet.cn/channel/8341.html': 5679,   #  红网
        'https://pf.rednet.cn/channel/8348.html': 5680,   #  红网
        'https://pf.rednet.cn/channel/8347.html': 5681,   #  红网
        'https://pf.rednet.cn/channel/8350.html': 5682,   #  红网
        'https://ldhn.rednet.cn/': 5683,   #  红网
        'https://ldhn.rednet.cn/channel/8404.html': 5684,   #  红网
        'https://ldhn.rednet.cn/channel/8405.html': 5685,   #  红网
        'https://ldhn.rednet.cn/channel/8407.html': 5686,   #  红网
        'https://ldhn.rednet.cn/channel/8408.html': 5687,   #  红网
        'https://ldhn.rednet.cn/channel/8413.html': 5688,   #  红网
        'https://ldhn.rednet.cn/channel/8410.html': 5689,   #  红网
        'https://ldhn.rednet.cn/channel/8409.html': 5690,   #  红网
        'https://wz.rednet.cn/': 5691,   #  红网
        'https://scjg.rednet.cn/': 5692,   #  红网
        'https://scjg.rednet.cn/channel/11935.html': 5693,   #  红网
        'https://scjg.rednet.cn/channel/11948.html': 5694,   #  红网
        'https://scjg.rednet.cn/channel/11949.html': 5695,   #  红网
        'https://scjg.rednet.cn/channel/11950.html': 5696,   #  红网
        'https://scjg.rednet.cn/channel/11951.html': 5697,   #  红网
        'https://scjg.rednet.cn/channel/11952.html': 5698,   #  红网
        'https://scjg.rednet.cn/channel/11953.html': 5699,   #  红网
        'https://hlj.rednet.cn/': 5700,   #  红网
        'https://hlj.rednet.cn/channel/8288.html': 5701,   #  红网
        'https://hlj.rednet.cn/channel/8282.html': 5702,   #  红网
        'https://hlj.rednet.cn/channel/8291.html': 5703,   #  红网
        'https://hlj.rednet.cn/channel/8287.html': 5704,   #  红网
        'https://hlj.rednet.cn/channel/8290.html': 5705,   #  红网
        'https://hlj.rednet.cn/channel/8280.html': 5706,   #  红网
        'https://hlj.rednet.cn/channel/8284.html': 5707,   #  红网
        'https://hlj.rednet.cn/channel/8283.html': 5708,   #  红网
        'http://yuqing.rednet.cn/': 5709,   #  红网
        'http://yuqing.rednet.cn/list.asp?cid=22': 5710,   #  红网
        'http://yuqing.rednet.cn/list.asp?cid=18': 5711,   #  红网
        'http://yuqing.rednet.cn/list.asp?cid=25': 5712,   #  红网
        'http://yuqing.rednet.cn/list.asp?cid=21': 5713,   #  红网
        'https://zfcg.rednet.cn/': 5714,   #  红网
        'https://zfcg.rednet.cn/channel/7656.html': 5715,   #  红网
        'https://zfcg.rednet.cn/channel/7662.html': 5716,   #  红网
        'https://zfcg.rednet.cn/channel/7666.html': 5717,   #  红网
        'https://zrzy.rednet.cn/': 5718,   #  红网
        'https://zrzy.rednet.cn/channel/1608.html': 5719,   #  红网
        'https://zrzy.rednet.cn/channel/1609.html': 5720,   #  红网
        'https://zrzy.rednet.cn/channel/1610.html': 5721,   #  红网
        'https://zrzy.rednet.cn/channel/1611.html': 5722,   #  红网
        'https://zrzy.rednet.cn/channel/1612.html': 5723,   #  红网
        'https://zrzy.rednet.cn/channel/1613.html': 5724,   #  红网
        'https://hb.rednet.cn/': 5725,   #  红网
        'https://hb.rednet.cn/channel/7034.html': 5726,   #  红网
        'https://hb.rednet.cn/channel/7035.html': 5727,   #  红网
        'https://hb.rednet.cn/channel/7036.html': 5728,   #  红网
        'https://hb.rednet.cn/channel/7037.html': 5729,   #  红网
        'http://auto.rednet.cn/': 5730,   #  红网
        'http://auto.rednet.cn/news/list/6_7_1': 5731,   #  红网
        'http://auto.rednet.cn/news/list/6_8_1': 5732,   #  红网
        'http://auto.rednet.cn/news/list/6_46_1': 5733,   #  红网
        'http://auto.rednet.cn/news/list/6_24_1': 5734,   #  红网
        'http://auto.rednet.cn/news/list/6_32_1': 5735,   #  红网
        'http://auto.rednet.cn/news/list/6_26_1': 5736,   #  红网
        'http://auto.rednet.cn/news/list/21_23_1': 5737,   #  红网
        'http://auto.rednet.cn/news/list/21_57_1': 5738,   #  红网
        'http://auto.rednet.cn/news/list/21_29_1': 5739,   #  红网
        'http://auto.rednet.cn/news/list/21_28_1': 5740,   #  红网
        'http://auto.rednet.cn/news/list/21_30_1': 5741,   #  红网
        'http://auto.rednet.cn/news/list/21_31_1': 5742,   #  红网
        'http://auto.rednet.cn/news/list/22_41_1': 5743,   #  红网
        'https://sw.rednet.cn/': 5744,   #  红网
        'https://sw.rednet.cn/channel/7236.html': 5745,   #  红网
        'https://sw.rednet.cn/channel/7237.html': 5746,   #  红网
        'https://sw.rednet.cn/channel/7238.html': 5747,   #  红网
        'https://sw.rednet.cn/channel/7239.html': 5748,   #  红网
        'https://sw.rednet.cn/channel/7240.html': 5749,   #  红网
        'https://sw.rednet.cn/channel/7241.html': 5750,   #  红网
        'https://sw.rednet.cn/channel/7242.html': 5751,   #  红网
        'https://sw.rednet.cn/channel/7243.html': 5752,   #  红网
        'https://sw.rednet.cn/channel/7244.html': 5753,   #  红网
        'https://shuili.rednet.cn/': 5754,   #  红网
        'https://shuili.rednet.cn/channel/7064.html': 5755,   #  红网
        'https://shuili.rednet.cn/channel/7065.html': 5756,   #  红网
        'https://shuili.rednet.cn/channel/7066.html': 5757,   #  红网
        'https://shuili.rednet.cn/channel/7067.html': 5758,   #  红网
        'https://shuili.rednet.cn/channel/7068.html': 5759,   #  红网
        'https://shuili.rednet.cn/channel/7069.html': 5760,   #  红网
        'https://shuili.rednet.cn/channel/7070.html': 5761,   #  红网
        'https://shuili.rednet.cn/channel/7071.html': 5762,   #  红网
        'http://money.rednet.cn/': 5763,   #  红网
        'http://money.rednet.cn/channel/1551.html': 5764,   #  红网
        'http://money.rednet.cn/channel/1552.html': 5765,   #  红网
        'http://money.rednet.cn/channel/1546.html': 5766,   #  红网
        'http://money.rednet.cn/channel/1556.html': 5767,   #  红网
        'http://money.rednet.cn/channel/1557.html': 5768,   #  红网
        'http://money.rednet.cn/channel/1555.html': 5769,   #  红网
        'http://money.rednet.cn/channel/1559.html': 5770,   #  红网
        'https://yq.rednet.cn/': 5771,   #  红网
        'https://yq.rednet.cn/channel/7741.html': 5772,   #  红网
        'https://yq.rednet.cn/channel/7717.html': 5773,   #  红网
        'https://yq.rednet.cn/channel/7714.html': 5774,   #  红网
        'https://yq.rednet.cn/channel/7715.html': 5775,   #  红网
        'https://yq.rednet.cn/channel/7740.html': 5776,   #  红网
        'https://yq.rednet.cn/channel/7716.html': 5777,   #  红网
        'https://yq.rednet.cn/channel/7721.html': 5778,   #  红网
        'https://yq.rednet.cn/channel/7720.html': 5779,   #  红网
        'https://jt.rednet.cn/': 5780,   #  红网
        'https://jt.rednet.cn/channel/7700.html': 5781,   #  红网
        'https://jt.rednet.cn/channel/7701.html': 5782,   #  红网
        'https://jt.rednet.cn/channel/7702.html': 5783,   #  红网
        'https://jt.rednet.cn/channel/7703.html': 5784,   #  红网
        'https://jt.rednet.cn/channel/7709.html': 5785,   #  红网
        'https://jt.rednet.cn/channel/7711.html': 5786,   #  红网
        'https://jt.rednet.cn/channel/7704.html': 5787,   #  红网
        'https://jt.rednet.cn/channel/7702.html': 5788,   #  红网
        'https://jt.rednet.cn/channel/7703.html': 5789,   #  红网
        'https://jt.rednet.cn/channel/7709.html': 5790,   #  红网
        'https://jt.rednet.cn/channel/7711.html': 5791,   #  红网
        'https://jt.rednet.cn/channel/7704.html': 5792,   #  红网
        'https://jt.rednet.cn/channel/7706.html': 5793,   #  红网
        'https://jt.rednet.cn/channel/7712.html': 5794,   #  红网
        'https://jt.rednet.cn/channel/7707.html': 5795,   #  红网
        'https://gs.rednet.cn/': 5796,   #  红网
        'https://gs.rednet.cn/channel/7076.html': 5797,   #  红网
        'https://gs.rednet.cn/channel/7077.html': 5798,   #  红网
        'https://gs.rednet.cn/channel/7078.html': 5799,   #  红网
        'https://gs.rednet.cn/channel/7079.html': 5800,   #  红网
        'https://gs.rednet.cn/channel/7080.html': 5801,   #  红网
        'https://gs.rednet.cn/channel/7085.html': 5802,   #  红网
        'https://gs.rednet.cn/channel/7082.html': 5803,   #  红网
        'https://gs.rednet.cn/channel/7083.html': 5804,   #  红网
        'https://edu.rednet.cn/': 5805,   #  红网
        'https://edu.rednet.cn/channel/7647.html': 5806,   #  红网
        'https://edu.rednet.cn/channel/7637.html': 5807,   #  红网
        'https://edu.rednet.cn/channel/7644.html': 5808,   #  红网
        'https://edu.rednet.cn/channel/7645.html': 5809,   #  红网
        'https://edu.rednet.cn/channel/7643.html': 5810,   #  红网
        'https://edu.rednet.cn/channel/7638.html': 5811,   #  红网
        'https://edu.rednet.cn/channel/7639.html': 5812,   #  红网
        'https://edu.rednet.cn/channel/7641.html': 5813,   #  红网
        'https://health.rednet.cn/': 5814,   #  红网
        'https://health.rednet.cn/channel/955.html': 5815,   #  红网
        'https://health.rednet.cn/channel/971.html': 5816,   #  红网
        'https://health.rednet.cn/channel/974.html': 5817,   #  红网
        'https://health.rednet.cn/channel/952.html': 5818,   #  红网
        'https://health.rednet.cn/channel/950.html': 5819,   #  红网
        'https://health.rednet.cn/channel/956.html': 5820,   #  红网
        'https://health.rednet.cn/channel/975.html': 5821,   #  红网
        'https://health.rednet.cn/channel/972.html': 5822,   #  红网
        'https://health.rednet.cn/channel/951.html': 5823,   #  红网
        'https://stock.rednet.cn/': 5824,   #  红网
        'https://stock.rednet.cn/channel/1567.html': 5825,   #  红网
        'https://stock.rednet.cn/channel/1580.html': 5826,   #  红网
        'https://stock.rednet.cn/channel/1568.html': 5827,   #  红网
        'https://stock.rednet.cn/channel/1577.html': 5828,   #  红网
        'https://stock.rednet.cn/channel/1579.html': 5829,   #  红网
        'https://stock.rednet.cn/channel/1571.html': 5830,   #  红网
        'https://stock.rednet.cn/channel/1573.html': 5831,   #  红网
        'https://stock.rednet.cn/channel/1578.html': 5832,   #  红网
        'https://stock.rednet.cn/channel/1570.html': 5833,   #  红网
        'https://xq.rednet.cn/': 5834,   #  红网
        'https://xq.rednet.cn/channel/1512.html': 5835,   #  红网
        'https://xq.rednet.cn/channel/1497.html': 5836,   #  红网
        'https://xq.rednet.cn/channel/1498.html': 5837,   #  红网
        'https://xq.rednet.cn/channel/1499.html': 5838,   #  红网
        'https://xq.rednet.cn/channel/1507.html': 5839,   #  红网
        'https://xq.rednet.cn/channel/1500.html': 5840,   #  红网
        'https://xq.rednet.cn/channel/1508.html': 5841,   #  红网
        'https://xq.rednet.cn/channel/1509.html': 5842,   #  红网
        'https://xq.rednet.cn/channel/1510.html': 5843,   #  红网
        'https://xq.rednet.cn/channel/1501.html': 5844,   #  红网
        'https://xq.rednet.cn/channel/1503.html': 5845,   #  红网
        'https://xq.rednet.cn/channel/1515.html': 5846,   #  红网
        'https://xq.rednet.cn/channel/1516.html': 5847,   #  红网
        'https://xq.rednet.cn/channel/1504.html': 5848,   #  红网
        'https://xq.rednet.cn/channel/1518.html': 5849,   #  红网
        'https://xq.rednet.cn/channel/1519.html': 5850,   #  红网
        'https://xq.rednet.cn/channel/1520.html': 5851,   #  红网
        'https://xq.rednet.cn/channel/1523.html': 5852,   #  红网
        'https://sports.rednet.cn/': 5853,   #  红网
        'https://sports.rednet.cn/channel/7892.html': 5854,   #  红网
        'https://sports.rednet.cn/channel/7886.html': 5855,   #  红网
        'https://sports.rednet.cn/channel/7887.html': 5856,   #  红网
        'https://sports.rednet.cn/channel/7893.html': 5857,   #  红网
        'https://sports.rednet.cn/channel/7894.html': 5858,   #  红网
        'https://fdc.rednet.cn/': 5859,   #  红网
        'https://fdc.rednet.cn/channel/1528.html': 5860,   #  红网
        'https://fdc.rednet.cn/channel/1529.html': 5861,   #  红网
        'https://fdc.rednet.cn/channel/1537.html': 5862,   #  红网
        'https://fdc.rednet.cn/channel/1532.html': 5863,   #  红网
        'https://hnxs.rednet.cn/': 5864,   #  红网
        'https://hnxs.rednet.cn/channel/1629.html': 5865,   #  红网
        'https://hnxs.rednet.cn/channel/1630.html': 5866,   #  红网
        'https://hnxs.rednet.cn/channel/1637.html': 5867,   #  红网
        'https://hnxs.rednet.cn/channel/1633.html': 5868,   #  红网
        'https://hnxs.rednet.cn/channel/1634.html': 5869,   #  红网
        'https://hnxs.rednet.cn/channel/1635.html': 5870,   #  红网
        'https://hnxs.rednet.cn/channel/1636.html': 5871,   #  红网
        'https://hnxs.rednet.cn/channel/1631.html': 5872,   #  红网
        'https://hnxs.rednet.cn/channel/1632.html': 5873,   #  红网
        'https://tour.rednet.cn/': 5874,   #  红网
        'https://tour.rednet.cn/channel/10492.html': 5875,   #  红网
        'https://tour.rednet.cn/channel/10495.html': 5876,   #  红网
        'https://tour.rednet.cn/channel/10498.html': 5877,   #  红网
        'https://tour.rednet.cn/channel/10493.html': 5878,   #  红网
        'https://tour.rednet.cn/channel/10496.html': 5879,   #  红网
        'https://tour.rednet.cn/channel/10470.html': 5880,   #  红网
        'https://tax.rednet.cn/': 5881,   #  红网
        'https://xsdj.rednet.cn/': 5882,   #  红网
        'https://tax.rednet.cn/channel/7827.html': 5883,   #  红网
        'https://tax.rednet.cn/channel/7828.html': 5884,   #  红网
        'https://tax.rednet.cn/channel/7850.html': 5885,   #  红网
        'https://tax.rednet.cn/channel/7848.html': 5886,   #  红网
        'https://tax.rednet.cn/channel/7832.html': 5887,   #  红网
        'https://tax.rednet.cn/channel/7829.html': 5888,   #  红网
        'https://tax.rednet.cn/channel/7851.html': 5889,   #  红网
        'https://aq.rednet.cn/': 5890,   #  红网
        'https://aq.rednet.cn/channel/7783.html': 5891,   #  红网
        'https://aq.rednet.cn/channel/7782.html': 5892,   #  红网
        'https://aq.rednet.cn/channel/7785.html': 5893,   #  红网
        'https://aq.rednet.cn/channel/7788.html': 5894,   #  红网
        'https://aq.rednet.cn/channel/7791.html': 5895,   #  红网
        'https://guoqi.rednet.cn/': 5896,   #  红网
        'https://guoqi.rednet.cn/channel/1705.html': 5897,   #  红网
        'https://guoqi.rednet.cn/channel/1707.html': 5898,   #  红网
        'https://guoqi.rednet.cn/channel/1709.html': 5899,   #  红网
        'https://guoqi.rednet.cn/channel/1711.html': 5900,   #  红网
        'https://guoqi.rednet.cn/channel/1713.html': 5901,   #  红网
        'https://guoqi.rednet.cn/channel/1706.html': 5902,   #  红网
        'https://guoqi.rednet.cn/channel/1708.html': 5903,   #  红网
        'https://guoqi.rednet.cn/channel/1712.html': 5904,   #  红网
        'https://jj.rednet.cn/': 5905,   #  红网
        'https://jj.rednet.cn/channel/1481.html': 5906,   #  红网
        'https://jj.rednet.cn/channel/1483.html': 5907,   #  红网
        'https://jj.rednet.cn/channel/10761.html': 5908,   #  红网
        'https://life.rednet.cn/': 5909,   #  红网
        'https://life.rednet.cn/channel/1581.html': 5910,   #  红网
        'https://life.rednet.cn/channel/1584.html': 5911,   #  红网
        'https://life.rednet.cn/channel/1583.html': 5912,   #  红网
        'https://wine.rednet.cn/': 5913,   #  红网
        'https://wine.rednet.cn/channel/1561.html': 5914,   #  红网
        'https://wine.rednet.cn/channel/1562.html': 5915,   #  红网
        'https://gh.rednet.cn/': 5916,   #  红网
        'https://gh.rednet.cn/channel/1115.html': 5917,   #  红网
        'https://gh.rednet.cn/channel/1116.html': 5918,   #  红网
        'https://gh.rednet.cn/channel/1117.html': 5919,   #  红网
        'https://gh.rednet.cn/channel/1118.html': 5920,   #  红网
        'https://gh.rednet.cn/channel/1119.html': 5921,   #  红网
        'https://gh.rednet.cn/channel/1121.html': 5922,   #  红网
        'https://gh.rednet.cn/channel/1122.html': 5923,   #  红网
        'https://3c.rednet.cn/': 5924,   #  红网
        'https://3c.rednet.cn/channel/1494.html': 5925,   #  红网

    }

    rules = (
        # https://gh.rednet.cn/content/2019/11/02/6180427.html
        # https://hn.rednet.cn/content/2019/11/10/6194575.html
        # https://news.rednet.cn/content/2019/10/24/6151731.html
        # http://auto.rednet.cn/news/201910/3245584.html
        # http://video.rednet.cn/content/2019/10/24/6149717.html
        # https://hn.rednet.cn/content/2019/10/31/6177080.html
        Rule(LinkExtractor(allow=r'.rednet.cn/\w+/%s/\d{2}/\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny=r'video'),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'.rednet.cn/\w+/%s/\d+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item_2',
             follow=False),
        Rule(LinkExtractor(allow=r'.video.rednet.cn/\w+/%s/\d{2}/\d+\.html' % datetime.today().strftime('%Y/%m'),),
             callback='parse_item_4',
             follow=False),
        Rule(LinkExtractor(allow=r'.rednet.cn/.*?\.html', deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019[1-9]/',
                                                                r'/20191[0]/', r'/2019/1[0]', r'_\d', r'bbs'),),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        # https://news.rednet.cn/content/2019/10/24/6151731.html
        # https://cs.rednet.cn/content/2019/10/24/6149824.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='detail_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='p_l_25']/text()").extract_first())
            try:
                content_div = xp("//section[@class='f_right detail_article_content']")[0]
            except :
                content_div = xp("//article[@class='f18 detail-article m_b_30']")[0]
            content, media, _, _ = self.content_clean(content_div)  # str  list
            origin_name = xp("//span[@class='p_l_10'][1]/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
        )

    def parse_item_2(self, response):
        # http://auto.rednet.cn/news/201910/3245584.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@id='row_Left']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='sourceTime']/span/text()").extract_first())
            content_div = xp("//div[@class='display_content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='sourceTime']/text()").extract_first()  # None  不要用[0]
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

    def parse_item_3(self, response):
        # 时刻
        # https://moment.rednet.cn/content/2019/10/24/6151064.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='time']/text()").extract_first())
            content_div = xp("//div[@class='description']")[0]
            if '<p' not in content_div.get():
                src = xp("//section[@class='content']/script/text()").extract_first()
                # http://1400085894.vod2.myqcloud.com/3de35aaevodtransgzp1400085894/9a7ccc4d5285890795213448314/v.f30.mp4
                video_url = re.findall(r'http://\d+\.vod2\.myqcloud\.com/\w+/\w+/.*mp4', src)[0]
                videos = {'1': {'src': video_url}}
                content = '<div>#{{1}}#</div>'
            else:
                content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//section[@class='content']/p[1]/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.parse_item_6(response)
        try:
            return self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,  # ""  None xpath
                content=content,
                media=media,
                videos=videos,
            )
        except:
            return self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,  # ""  None xpath
                content=content,
                videos=videos,
            )


    def parse_item_4(self, response):
        # 有视频
        # http://video.rednet.cn/content/2019/10/24/6149717.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@id='cut_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='content_info clear']/span[1]/text()").extract_first())
            content_div = xp("//div[@class='video_left f_left']/script/text()").extract_first()
            # http://1400085894.vod2.myqcloud.com/3de35aaevodtransgzp1400085894/50f1c3f35285890795182518083/v.f30.mp4
            # http://1400085894.vod2.myqcloud.com/3de35aaevodtransgzp1400085894/9a6b488e5285890795213439504/v.f30.mp4
            # http://1400085894.vod2.myqcloud.com/3de35aaevodtransgzp1400085894/7a834b1f5285890795196928184/v.f30.mp4
            video_url = re.findall(r'http://\d+\.vod2\.myqcloud\.com/\w+/\w+/.*mp4', content_div)[0]
            videos = {'1': {'src': video_url}}
            content = '<div>#{{1}}#</div>'
            # content, media, videos, video_cover = self.content_clean(content_div, need_video=True)  # str  list
            origin_name = xp("//div[@class='content_info clear']/span[2]/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            videos=videos,

        )

    def parse_item_6(self, response):
        # 视频加文章
        # https://jj.rednet.cn/content/2019/10/28/6155896.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='detail_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='p_l_25']/text()").extract_first())
            content_div = xp("//section[@class='f_right detail_article_content p_t_20']")[0]
            content, media, _, _ = self.content_clean(content_div)  # str  list
            content_video = xp("//section[@class='f_right detail_article_content p_t_20']/script/text()").extract_first()
            # http://1400085894.vod2.myqcloud.com/3de35aaevodtransgzp1400085894/50f1c3f35285890795182518083/v.f30.mp4
            video_url = re.findall(r'http://\d+\.vod2\.myqcloud\.com/\w+/\w+/.*mp4', content_video)[0]
            videos = {'1': {'src': video_url}}
            origin_name = xp("//span[@class='p_l_10'][1]/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos
        )

