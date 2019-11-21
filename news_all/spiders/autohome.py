# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings

from news_all.spider_models import otherurl_meta
from news_all.spider_models import NewsRCSpider, js_meta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class AutohomeSpider(NewsRCSpider):

	name = 'autohome'

	mystart_urls = {
		'https://www.autohome.com.cn/beijing/': 1,
		'https://www.autohome.com.cn/all/#pvareaid=3311229': 2,
		'https://www.autohome.com.cn/topics/#pvareaid=2023455': 3,
		'https://www.autohome.com.cn/topics/1': 4,
		'https://www.autohome.com.cn/topics/': 5,
		'https://www.autohome.com.cn/topics/2': 6,
		'https://www.autohome.com.cn/topics/3': 7,
		'https://www.autohome.com.cn/topics/5': 8,
		'https://www.autohome.com.cn/topics/6': 9,
		'https://www.autohome.com.cn/bestauto/#pvareaid=3311236': 10,
		'https://chejiahao.autohome.com.cn/#pvareaid=3311237': 11,
		'https://chejiahao.autohome.com.cn/Good#pvareaid=2808145': 12,
		'https://chejiahao.autohome.com.cn/category/1#pvareaid=2808145': 13,
		'https://chejiahao.autohome.com.cn/category/2#pvareaid=2808145': 14,
		'https://chejiahao.autohome.com.cn/category/3#pvareaid=2808145': 15,
		'https://chejiahao.autohome.com.cn/category/4#pvareaid=2808145': 16,
		'https://chejiahao.autohome.com.cn/category/5#pvareaid=2808145': 17,
		'https://chejiahao.autohome.com.cn/category/6#pvareaid=2808145': 18,
		'https://chejiahao.autohome.com.cn/category/7#pvareaid=2808145': 19,
		'https://chejiahao.autohome.com.cn/category/8#pvareaid=2808145': 20,
		'https://chejiahao.autohome.com.cn/category/9#pvareaid=2808145': 21,
		'https://chejiahao.autohome.com.cn/category/10#pvareaid=2808145': 22,
		'https://chejiahao.autohome.com.cn/category/11#pvareaid=2808145': 23,
		'https://v.autohome.com.cn/#pvareaid=3311238': 24,
		'https://v.autohome.com.cn/#': 25,
		'https://v.autohome.com.cn/u/19996353/#pvareaid=3454181': 26,
		'https://v.autohome.com.cn/u/19987472/#pvareaid=3454181': 27,
		'https://v.autohome.com.cn/u/35729101/#pvareaid=3454181': 28,
		'https://v.autohome.com.cn/u/66592556/#pvareaid=3454181': 29,
		'https://v.autohome.com.cn/u/27493450/#pvareaid=3454181': 30,
		'https://v.autohome.com.cn/u/41890819/#pvareaid=3454181': 31,
		'https://v.autohome.com.cn/u/53106259/#pvareaid=3454181': 32,
		'https://v.autohome.com.cn/u/40398749/#pvareaid=3454181': 33,
		'https://v.autohome.com.cn/u/20380947/#pvareaid=3454181': 34,
		'https://v.autohome.com.cn/u/94904626/#pvareaid=3454181': 35,
		'https://www.autohome.com.cn/hangye/#pvareaid=6825588': 36,
		'https://www.autohome.com.cn/hangye/': 37,
		'https://www.autohome.com.cn/hangye/news/': 38,
		'https://www.autohome.com.cn/hangye/guandian/': 39,
		'https://club.autohome.com.cn/#pvareaid=3311253': 40,
		'https://club.autohome.com.cn/newfe/videocommunity#pvareaid=6830656': 41,
		'https://club.autohome.com.cn/jingxuan/#pvareaid=3311254': 42,
		'https://club.autohome.com.cn/Young/Index#pvareaid=3454621': 43,
		'https://wenda.autohome.com.cn/#pvareaid=3468129': 44,
		'https://www.autohome.com.cn/ev/#pvareaid=3454680': 45,
		'https://ev.autohome.com.cn/#pvareaid=3311257': 46,
		'https://www.autohome.com.cn/all/#pvareaid=3311481': 47,
		'https://www.autohome.com.cn/all/': 48,
		'https://www.autohome.com.cn/news/': 49,
		'https://www.autohome.com.cn/advice/': 50,
		'https://www.autohome.com.cn/drive/': 51,
		'https://www.autohome.com.cn/use/': 52,
		'https://www.autohome.com.cn/culture/': 53,
		'https://www.autohome.com.cn/travels/': 54,
		'https://www.autohome.com.cn/tech/': 55,
		'https://www.autohome.com.cn/tuning/': 56,
		'https://www.autohome.com.cn/ev/': 57,
		'https://www.autohome.com.cn/hangye/list/': 58,
	}

	custom_settings = {
		'DEPTH_LIMIT': 0,
		'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
	}