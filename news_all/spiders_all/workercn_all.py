# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import otherurl_meta
from news_all.spiders.workercn import WorkercnSpider


class WorkercnAllspider(WorkercnSpider):
    """中工网 列表采集"""
    # 4月17日 暂停抓取
    # 'http://nmg.workercn.cn/698/698.shtml': 5099,
    # 'http://edu.workercn.cn/32904/32904.shtml': 5254,
    # 'http://job.workercn.cn/312/312.shtml': 5260,
    # 'http://acftu.workercn.cn/29603/29603.shtml': 5209,
    # 'http://character.workercn.cn/861/861.shtml': 5198,
    
    name = 'workercn_all'
    
    mystart_urls = {
        'http://nmg.workercn.cn/702/702.shtml': 5100,
        'http://nmg.workercn.cn/703/703.shtml': 5105,
        'http://nmg.workercn.cn/32895/32895.shtml': 5098,
        
        'http://comment.workercn.cn/440/440.shtml': 5233,
        'http://comment.workercn.cn/436/436.shtml': 5234,
        'http://comment.workercn.cn/437/437.shtml': 92,  # 5236,
        'http://comment.workercn.cn/433/433.shtml': 5237,
        'http://comment.workercn.cn/470/470.shtml': 5238,
        'http://comment.workercn.cn/434/434.shtml': 5239,
        'http://comment.workercn.cn/429/429.shtml': 5240,
        'http://comment.workercn.cn/435/435.shtml': 5241,
        'http://comment.workercn.cn/424/424.shtml': 5081,
        'http://comment.workercn.cn/439/439.shtml': 5097,
        'http://comment.workercn.cn/427/427.shtml': 5152,
        
        'http://acftu.workercn.cn/41/41.shtml': 5214,
        
        'http://right.workercn.cn/158/158.shtml': 5210,
        'http://right.workercn.cn/892/892.shtml': 5199,
        'http://right.workercn.cn/164/164.shtml': 5211,
        'http://right.workercn.cn/162/162.shtml': 5212,
        'http://right.workercn.cn/156/156.shtml': 5217,
        'http://right.workercn.cn/147/147.shtml': 5218,
        'http://right.workercn.cn/161/161.shtml': 5225,
        
        'http://character.workercn.cn/354/354.shtml': 5229,
        'http://character.workercn.cn/358/358.shtml': 5230,
        'http://character.workercn.cn/352/352.shtml': 5231,
        'http://character.workercn.cn/350/350.shtml': 5232,
        
        'http://job.workercn.cn/322/322.shtml': 5257,
        'http://job.workercn.cn/317/317.shtml': 5259,
        'http://job.workercn.cn/311/311.shtml': 5261,
        'http://job.workercn.cn/32473/32473.shtml': 5262,
        
        'http://theory.workercn.cn/239/239.shtml': 5173,
        'http://theory.workercn.cn/253/253.shtml': 5174,
        'http://theory.workercn.cn/252/252.shtml': 5175,
        'http://theory.workercn.cn/260/260.shtml': 5169,
        'http://theory.workercn.cn/255/255.shtml': 5170,
        'http://theory.workercn.cn/256/256.shtml': 5171,
        'http://theory.workercn.cn/32937/32937.shtml': 5172,
        'http://theory.workercn.cn/32935/32935.shtml': 5178,
        'http://theory.workercn.cn/242/242.shtml': 5181,
        'http://theory.workercn.cn/32936/32936.shtml': 5187,
        'http://theory.workercn.cn/251/251.shtml': 5197,
        
        'http://edu.workercn.cn/32908/32908.shtml': 5247,
        'http://edu.workercn.cn/32912/32912.shtml': 5248,
        'http://edu.workercn.cn/32911/32911.shtml': 5249,
        'http://edu.workercn.cn/209/209.shtml': 5251,
        'http://edu.workercn.cn/32910/32910.shtml': 5255,
    }
    
    # http://right.workercn.cn/158/201904/17/190417085739319.shtml
    rules = (
    Rule(LinkExtractor(allow=(r'workercn.cn/\d+/%s/\d{2}/\d{10,}\.s?html' % datetime.today().strftime('%Y%m'),),
                       restrict_xpaths=r'//ul[@id="leftList"]'),
         callback='parse_item', follow=False),
    Rule(LinkExtractor(allow=(r'workercn.cn/.*?\d{10,}\.s?html',), deny=(r'/201[0-8]', r'/20190[1-9]/'),
                       restrict_xpaths=r'//ul[@id="leftList"]'),
         process_request=otherurl_meta, follow=False),
    )

    custom_settings = deepcopy(WorkercnSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter'%WorkercnSpider.name},
    )