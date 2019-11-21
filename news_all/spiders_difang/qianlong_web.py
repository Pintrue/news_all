# -*- coding: utf-8 -*-
# @Time   : 2019/8/26 下午5:34
# @Author : NewmanZhou
# @Project : news_all
# @Software: PyCharm
from copy import deepcopy

from scrapy.conf import settings

from news_all.spider_models import NewsRCSpider, otherurl_meta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime

from news_all.tools.others import get_sub_str_ex


class QianLongSpider(NewsRCSpider):
    """千龙网  web端"""
    name = 'qianlong_web'

    mystart_urls = {
                       'http://www.qianlong.com/': 4135,  # 网站-垂直网站-千龙新闻网
                       'http://beijing.qianlong.com/': 4136,  # 网站-垂直网站-千龙新闻网-北京
                       'http://beijing.qianlong.com/yaowenjujiao/': 4137,  # 网站-垂直网站-千龙新闻网-北京-要闻聚焦
                       'http://beijing.qianlong.com/dangwulianbo/': 4138,  # 网站-垂直网站-千龙新闻网-北京-党务联播
                       'http://beijing.qianlong.com/zhengwulianbo/': 4139,  # 网站-垂直网站-千龙新闻网-北京-政务联播
                       'http://beijing.qianlong.com/tongzhigonggao/': 4140,  # 网站-垂直网站-千龙新闻网-北京-通知公告
                       'http://beijing.qianlong.com/benwangcehua/': 4141,  # 网站-垂直网站-千龙新闻网-北京-本网策划
                       'http://beijing.qianlong.com/renshigongshirenmian/': 4142,  # 网站-垂直网站-千龙新闻网-北京-人事公示任免
                       'http://beijing.qianlong.com/xinzhengjiedu/': 4143,  # 网站-垂直网站-千龙新闻网-北京-新政解读
                       'http://beijing.qianlong.com/zhengwushuju/': 4144,  # 网站-垂直网站-千龙新闻网-北京-政务数据
                       'http://beijing.qianlong.com/xinwenfabuhui/': 4145,  # 网站-垂直网站-千龙新闻网-北京-新闻发布会
                       'http://beijing.qianlong.com/jgc/': 4146,  # 网站-垂直网站-千龙新闻网-北京-京观察
                       'http://legal.qianlong.com/': 4147,  # 网站-垂直网站-千龙新闻网-法治
                       'http://legal.qianlong.com/fazhiyaowen/': 4148,  # 网站-垂直网站-千龙新闻网-法治-法治要闻
                       'http://legal.qianlong.com/shoushanzhiqu/': 4149,  # 网站-垂直网站-千龙新闻网-法治-首善之区
                       'http://legal.qianlong.com/daanzhuizong/': 4150,  # 网站-垂直网站-千龙新闻网-法治-大案追踪
                       'http://legal.qianlong.com/xinfakandian/': 4151,  # 网站-垂直网站-千龙新闻网-法治-新法看点
                       'http://legal.qianlong.com/wangluoyufa/': 4152,  # 网站-垂直网站-千龙新闻网-法治-网络与法
                       'http://legal.qianlong.com/fazhirenwu/': 4153,  # 网站-垂直网站-千龙新闻网-法治-法治人物
                       'http://legal.qianlong.com/fazhishiping/': 4154,  # 网站-垂直网站-千龙新闻网-法治-法治时评
                       'http://legal.qianlong.com/fazhituku/': 4155,  # 网站-垂直网站-千龙新闻网-法治-法治图库
                       'http://fanxiejiao.qianlong.com/': 4156,  # 网站-垂直网站-千龙新闻网-法治-反邪教
                       'http://news.qianlong.com/': 4157,  # 网站-垂直网站-千龙新闻网-千龙原创
                       'http://news.qianlong.com/qlcf/': 4158,  # 网站-垂直网站-千龙新闻网-千龙原创-采访
                       'http://news.qianlong.com/qlpl/': 4159,  # 网站-垂直网站-千龙新闻网-千龙原创-评论
                       'http://news.qianlong.com/qltx/': 4160,  # 网站-垂直网站-千龙新闻网-千龙原创-图像
                       'http://news.qianlong.com/qlsp/': 4161,  # 网站-垂直网站-千龙新闻网-千龙原创-视听
                       'http://news.qianlong.com/qldm/': 4162,  # 网站-垂直网站-千龙新闻网-千龙原创-动漫
                       'http://news.qianlong.com/qlsz/': 4163,  # 网站-垂直网站-千龙新闻网-千龙原创-时政
                       'http://news.qianlong.com/qlyl/': 4164,  # 网站-垂直网站-千龙新闻网-千龙原创-文娱
                       'http://news.qianlong.com/qlwh/': 4165,  # 网站-垂直网站-千龙新闻网-千龙原创-体育
                       'http://news.qianlong.com/qlzx/': 4166,  # 网站-垂直网站-千龙新闻网-千龙原创-资讯
                       'http://news.qianlong.com/qljy/': 4167,  # 网站-垂直网站-千龙新闻网-千龙原创-教育
                       'http://news.qianlong.com/qlzk/': 4168,  # 网站-垂直网站-千龙新闻网-千龙原创-智库
                       'http://lianzheng.qianlong.com/': 4169,  # 网站-垂直网站-千龙新闻网-廉政
                       'http://lianzheng.qianlong.com/jiaodianxinwen/': 4170,  # 网站-垂直网站-千龙新闻网-廉政-焦点新闻
                       'http://lianzheng.qianlong.com/jicenglianqing/': 4171,  # 网站-垂直网站-千龙新闻网-廉政-基层廉情
                       'http://lianzheng.qianlong.com/lianzhengkaimo/': 4172,  # 网站-垂直网站-千龙新闻网-廉政-廉政楷模
                       'http://lianzheng.qianlong.com/lianzhengshipin/': 4173,  # 网站-垂直网站-千龙新闻网-廉政-廉政视频
                       'http://lianzheng.qianlong.com/pinglun/': 4174,  # 网站-垂直网站-千龙新闻网-廉政-评论
                       'http://lianzheng.qianlong.com/lianzhengjingjian/': 4175,  # 网站-垂直网站-千龙新闻网-廉政-廉政镜鉴
                       'http://lianzheng.qianlong.com/gaocengpinglun/': 4176,  # 网站-垂直网站-千龙新闻网-廉政-高层评论
                       'http://lianzheng.qianlong.com/dangjifagui/': 4177,  # 网站-垂直网站-千龙新闻网-廉政-党纪法规
                       'http://lianzheng.qianlong.com/juanshuofa/': 4178,  # 网站-垂直网站-千龙新闻网-廉政-举案说法
                       'http://mil.qianlong.com/': 4179,  # 网站-垂直网站-千龙新闻网-军事
                       'http://mil.qianlong.com/zhongguojunshi/': 4180,  # 网站-垂直网站-千龙新闻网-军事-中国军事
                       'http://mil.qianlong.com/guojijunshi/': 4181,  # 网站-垂直网站-千龙新闻网-军事-国际军事
                       'http://mil.qianlong.com/waimeibaodao/': 4182,  # 网站-垂直网站-千龙新闻网-军事-外媒报道
                       'http://mil.qianlong.com/zhanshizhanyi/': 4183,  # 网站-垂直网站-千龙新闻网-军事-战史战役
                       'http://mil.qianlong.com/junshiyanjiu/': 4184,  # 网站-垂直网站-千龙新闻网-军事-军事研究
                       'http://mil.qianlong.com/zhuangbeitantao/': 4185,  # 网站-垂直网站-千龙新闻网-军事-装备探讨
                       'http://mil.qianlong.com/junshishipin/': 4186,  # 网站-垂直网站-千龙新闻网-军事-军事视频
                       'http://mil.qianlong.com/junshidianying/': 4187,  # 网站-垂直网站-千龙新闻网-军事-军事电影
                       'http://mil.qianlong.com/junshiyouxi/': 4188,  # 网站-垂直网站-千龙新闻网-军事-军事游戏
                       'http://culture.qianlong.com/': 4189,  # 网站-垂直网站-千龙新闻网-文化
                       'http://culture.qianlong.com/wenyiyc/': 4190,  # 网站-垂直网站-千龙新闻网-文化-文艺·演出
                       'http://culture.qianlong.com/wwhz/': 4191,  # 网站-垂直网站-千龙新闻网-文化-文物·会展
                       'http://culture.qianlong.com/wccy/': 4192,  # 网站-垂直网站-千龙新闻网-文化-文创·产业
                       'http://culture.qianlong.com/ydcb/': 4193,  # 网站-垂直网站-千龙新闻网-文化-阅读·出版
                       'http://culture.qianlong.com/jccq/': 4194,  # 网站-垂直网站-千龙新闻网-文化-京城传奇
                       'http://culture.qianlong.com/rb/': 4195,  # 网站-垂直网站-千龙新闻网-文化-热播
                       'http://culture.qianlong.com/rw/': 4196,  # 网站-垂直网站-千龙新闻网-文化-人物
                       'http://culture.qianlong.com/ht/': 4197,  # 网站-垂直网站-千龙新闻网-文化-话题
                       'http://culture.qianlong.com/lyk/': 4198,  # 网站-垂直网站-千龙新闻网-文化-另眼看
                       'http://culture.qianlong.com/zt/': 4199,  # 网站-垂直网站-千龙新闻网-文化-专题
                       'http://culture.qianlong.com/jsxw/': 4200,  # 网站-垂直网站-千龙新闻网-文化-即时新闻
                       'http://edu.qianlong.com/': 4201,  # 网站-垂直网站-千龙新闻网-教育
                       'http://edu.qianlong.com/quanweishengyin/': 4202,  # 网站-垂直网站-千龙新闻网-教育-权威声音
                       'http://edu.qianlong.com/jiaoyujuzhen/': 4203,  # 网站-垂直网站-千龙新闻网-教育-教育矩阵
                       'http://edu.qianlong.com/zhongxiaoxue/': 4204,  # 网站-垂直网站-千龙新闻网-教育-中小学
                       'http://edu.qianlong.com/gaoxiao/': 4205,  # 网站-垂直网站-千龙新闻网-教育-高校
                       'http://edu.qianlong.com/kaoyan/': 4206,  # 网站-垂直网站-千龙新闻网-教育-考研
                       'http://edu.qianlong.com/peixun/': 4207,  # 网站-垂直网站-千龙新闻网-教育-培训
                       'http://edu.qianlong.com/chengzhangriji/': 4208,  # 网站-垂直网站-千龙新闻网-教育-成长日记
                       'http://edu.qianlong.com/jiatingjiaoyu/': 4209,  # 网站-垂直网站-千龙新闻网-教育-家庭教育
                       'http://edu.qianlong.com/yuanchuang/': 4210,  # 网站-垂直网站-千龙新闻网-教育-原创
                       'http://edu.qianlong.com/qcy/': 4211,  # 网站-垂直网站-千龙新闻网-教育-青菜园
                       'http://finance.qianlong.com/': 4212,  # 网站-垂直网站-千龙新闻网-经济
                       'http://finance.qianlong.com/shoudujingji/': 4213,  # 网站-垂直网站-千龙新闻网-经济-首都经济
                       'http://finance.qianlong.com/jinrong/': 4214,  # 网站-垂直网站-千龙新闻网-经济-金融
                       'http://finance.qianlong.com/zhuanti/': 4215,  # 网站-垂直网站-千龙新闻网-经济-专题
                       'http://finance.qianlong.com/chanyexinwen/': 4216,  # 网站-垂直网站-千龙新闻网-经济-产业新闻
                       'http://finance.qianlong.com/gongsi/': 4217,  # 网站-垂直网站-千龙新闻网-经济-公司
                       'http://finance.qianlong.com/guoqi/': 4218,  # 网站-垂直网站-千龙新闻网-经济-国企
                       'http://finance.qianlong.com/shangyeminsheng/': 4219,  # 网站-垂直网站-千龙新闻网-经济-商业民生
                       'http://finance.qianlong.com/shipin/': 4220,  # 网站-垂直网站-千龙新闻网-经济-食品
                       'http://finance.qianlong.com/xiaofeitishi/': 4221,  # 网站-垂直网站-千龙新闻网-经济-消费提示
                       'http://finance.qianlong.com/caifu/': 4222,  # 网站-垂直网站-千龙新闻网-经济-财富
                       'http://finance.qianlong.com/touzi/': 4223,  # 网站-垂直网站-千龙新闻网-经济-投资
                       'http://finance.qianlong.com/shoucang/': 4224,  # 网站-垂直网站-千龙新闻网-经济-收藏
                       'http://finance.qianlong.com/huiyihuodong/': 4225,  # 网站-垂直网站-千龙新闻网-经济-会议活动
                       'http://guoqi.qianlong.com/': 4226,  # 网站-垂直网站-千龙新闻网-国企
                       'http://guoqi.qianlong.com/guoqidongtai/': 4227,  # 网站-垂直网站-千龙新闻网-国企-国企动态
                       'http://guoqi.qianlong.com/guoqirenwu/': 4228,  # 网站-垂直网站-千龙新闻网-国企-国企人物
                       'http://guoqi.qianlong.com/guoqidangjian/': 4229,  # 网站-垂直网站-千龙新闻网-国企-国企党建
                       'http://guoqi.qianlong.com/zhuanti/': 4230,  # 网站-垂直网站-千龙新闻网-国企-专题
                       'http://guoqi.qianlong.com/shehuizeren/': 4231,  # 网站-垂直网站-千龙新闻网-国企-社会责任
                       'http://guoqi.qianlong.com/lilunguandian/': 4232,  # 网站-垂直网站-千龙新闻网-国企-理论观点
                       'http://guoqi.qianlong.com/guoqijuzhen/': 4233,  # 网站-垂直网站-千龙新闻网-国企-国企矩阵
                       'http://tech.qianlong.com/': 4234,  # 网站-垂直网站-千龙新闻网-科技
                       'http://tech.qianlong.com/czbj/': 4235,  # 网站-垂直网站-千龙新闻网-科技-创在北京
                       'http://tech.qianlong.com/kjjz/': 4236,  # 网站-垂直网站-千龙新闻网-科技-科技矩阵
                       'http://tech.qianlong.com/web/': 4237,  # 网站-垂直网站-千龙新闻网-科技-互联网＋
                       'http://tech.qianlong.com/industry/': 4238,  # 网站-垂直网站-千龙新闻网-科技-IY业界
                       'http://tech.qianlong.com/game/': 4239,  # 网站-垂直网站-千龙新闻网-科技-手机·数码
                       'http://tech.qianlong.com/explore/': 4240,  # 网站-垂直网站-千龙新闻网-科技-科普探索
                       'http://tech.qianlong.com/special/': 4241,  # 网站-垂直网站-千龙新闻网-科技-科技图赏
                       'http://house.qianlong.com/': 4242,  # 网站-垂直网站-千龙新闻网-住房
                       'http://house.qianlong.com/shoudufangchan/': 4243,  # 网站-垂直网站-千龙新闻网-住房-首都房产
                       'http://house.qianlong.com/goufangshidian/': 4244,  # 网站-垂直网站-千龙新闻网-住房-购房视点
                       'http://house.qianlong.com/lvsejiaju/': 4245,  # 网站-垂直网站-千龙新闻网-住房-绿色家居
                       'http://house.qianlong.com/zhihuijiadian/': 4247,  # 网站-垂直网站-千龙新闻网-住房-智慧家电
                       'http://house.qianlong.com/wenshequ/': 4248,  # 网站-垂直网站-千龙新闻网-住房-温馨社区
                       'http://house.qianlong.com/jingcaituji/': 4249,  # 网站-垂直网站-千龙新闻网-住房-精彩图集
                       'http://ent.qianlong.com/': 4250,  # 网站-垂直网站-千龙新闻网-娱乐
                       'http://ent.qianlong.com/tuijian/': 4251,  # 网站-垂直网站-千龙新闻网-娱乐-推荐
                       'http://ent.qianlong.com/star/': 4252,  # 网站-垂直网站-千龙新闻网-娱乐-明星
                       'http://ent.qianlong.com/movie/': 4253,  # 网站-垂直网站-千龙新闻网-娱乐-电影
                       'http://ent.qianlong.com/music/': 4254,  # 网站-垂直网站-千龙新闻网-娱乐-电视
                       # 'http://ent.qianlong.com/music/': 4255,  # 网站-垂直网站-千龙新闻网-娱乐-音乐
                       'http://ent.qianlong.com/yuping/': 4256,  # 网站-垂直网站-千龙新闻网-娱乐-娱评
                       'http://ent.qianlong.com/shipin/': 4257,  # 网站-垂直网站-千龙新闻网-娱乐-视频
                       'http://ent.qianlong.com/yuanchuang/': 4258,  # 网站-垂直网站-千龙新闻网-娱乐-原创
                       'http://ent.qianlong.com/pic/': 4259,  # 网站-垂直网站-千龙新闻网-娱乐-图片
                       'http://ent.qianlong.com/zhuanti/': 4260,  # 网站-垂直网站-千龙新闻网-娱乐-专题
                       'http://sports.qianlong.com/': 4261,  # 网站-垂直网站-千龙新闻网-体育
                       'http://sports.qianlong.com/tyyc/': 4262,  # 网站-垂直网站-千龙新闻网-体育-体育原创
                       'http://sports.qianlong.com/jingchengtiyu/': 4263,  # 网站-垂直网站-千龙新闻网-体育-京城体育
                       'http://sports.qianlong.com/nba/': 4264,  # 网站-垂直网站-千龙新闻网-体育-NBA
                       'http://sports.qianlong.com/cba/': 4265,  # 网站-垂直网站-千龙新闻网-体育-CBA
                       'http://sports.qianlong.com/guojizuqiu/': 4266,  # 网站-垂直网站-千龙新闻网-体育-国际足球
                       'http://sports.qianlong.com/zhongguozuqiu/': 4267,  # 网站-垂直网站-千龙新闻网-体育-中国足球
                       'http://sports.qianlong.com/zonghetiyu/': 4268,  # 网站-垂直网站-千龙新闻网-体育-综合体育
                       'http://bbs.qianlong.com/f_256_t_230.html': 4269,  # 网站-垂直网站-千龙新闻网-体育-体坛八卦
                       'http://winter.qianlong.com/': 4270,  # 网站-垂直网站-千龙新闻网-体育-冰雪
                       'http://www.bjnvzu.com/': 4271,  # 网站-垂直网站-千龙新闻网-体育-北控凤凰
                       'http://sdcsgy.qianlong.com/': 4272,  # 网站-垂直网站-千龙新闻网-公益
                       'http://sdcsgy.qianlong.com/zhiyuanbeijing/': 4273,  # 网站-垂直网站-千龙新闻网-公益-志愿北京
                       'http://sdcsgy.qianlong.com/yigongzhiyuanzhe/': 4274,  # 网站-垂直网站-千龙新闻网-公益-义工·志愿者
                       'http://sdcsgy.qianlong.com/qiyecishanzuzhituant/': 4275,  # 网站-垂直网站-千龙新闻网-公益-企业·慈善组织·团队
                       'http://sdcsgy.qianlong.com/wangluogongyi/': 4276,  # 网站-垂直网站-千龙新闻网-公益-网络公益
                       'http://sdcsgy.qianlong.com/yigongbaoming/': 4277,  # 网站-垂直网站-千龙新闻网-公益-义工报名
                       'http://sdcsgy.qianlong.com/qiuzhubangzhu/': 4278,  # 网站-垂直网站-千龙新闻网-公益-求助·帮助
                       'http://sdcsgy.qianlong.com/gongyiguan/': 4279,  # 网站-垂直网站-千龙新闻网-公益-公益观
                       'http://sdcsgy.qianlong.com/gongyizhengce/': 4280,  # 网站-垂直网站-千龙新闻网-公益-公益政策
                       'http://auto.qianlong.com/': 4281,  # 网站-垂直网站-千龙新闻网-汽车
                       'http://auto.qianlong.com/xinche/': 4282,  # 网站-垂直网站-千龙新闻网-汽车-新车
                       'http://auto.qianlong.com/daogou/': 4283,  # 网站-垂直网站-千龙新闻网-汽车-导购
                       'http://auto.qianlong.com/hangqing/': 4284,  # 网站-垂直网站-千龙新闻网-汽车-行情
                       'http://auto.qianlong.com/shijia/': 4285,  # 网站-垂直网站-千龙新闻网-汽车-试驾
                       'http://auto.qianlong.com/hangyedongtai/': 4286,  # 网站-垂直网站-千龙新闻网-汽车-行业动态
                       'http://auto.qianlong.com/yongcheyangche/': 4287,  # 网站-垂直网站-千龙新闻网-汽车-用车
                       'http://auto.qianlong.com/changxingbeijing/': 4288,  # 网站-垂直网站-千龙新闻网-汽车-畅行北京
                       'http://auto.qianlong.com/qianlongchupin/': 4289,  # 网站-垂直网站-千龙新闻网-汽车-千龙出品
                       'http://travel.qianlong.com/': 4290,  # 网站-垂直网站-千龙新闻网-旅游
                       'http://travel.qianlong.com/beijinglvyou/': 4291,  # 网站-垂直网站-千龙新闻网-旅游-北京旅游
                       'http://travel.qianlong.com/remenxianlu/': 4292,  # 网站-垂直网站-千龙新闻网-旅游-热门路线
                       'http://travel.qianlong.com/yejiexinwen/': 4293,  # 网站-垂直网站-千龙新闻网-旅游-业界新闻
                       'http://travel.qianlong.com/beijingliwu/': 4294,  # 网站-垂直网站-千龙新闻网-旅游-北京礼物
                       'http://travel.qianlong.com/jingquresou/': 4295,  # 网站-垂直网站-千龙新闻网-旅游-景区热搜
                       'http://travel.qianlong.com/huwaitanxian/': 4296,  # 网站-垂直网站-千龙新闻网-旅游-户外探险
                       'http://travel.qianlong.com/shijue/': 4297,  # 网站-垂直网站-千龙新闻网-旅游-视觉
                       'http://travel.qianlong.com/jiudian/': 4298,  # 网站-垂直网站-千龙新闻网-旅游-酒店
                       'http://travel.qianlong.com/hangkong/': 4299,  # 网站-垂直网站-千龙新闻网-旅游-航空
                       'http://travel.qianlong.com/zhuanti/daren/': 4300,  # 网站-垂直网站-千龙新闻网-旅游-达人圈
                       'http://bjtsb.qianlong.com/': 4301,  # 网站-垂直网站-千龙新闻网-质检
                       'http://bjtsb.qianlong.com/jsxw/': 4302,  # 网站-垂直网站-千龙新闻网-质检-最新动态
                       'http://bjtsb.qianlong.com/ztbd/': 4303,  # 网站-垂直网站-千龙新闻网-质检-质检专题
                       'http://bjtsb.qianlong.com/zjfc/': 4304,  # 网站-垂直网站-千龙新闻网-质检-质检风采
                       'http://bjtsb.qianlong.com/zjsp/': 4305,  # 网站-垂直网站-千龙新闻网-质检-质检视频
                       'http://interview.qianlong.com/': 4306,  # 网站-垂直网站-千龙新闻网-采访
                       'http://interview.qianlong.com/shenduxinbeijing/': 4307,  # 网站-垂直网站-千龙新闻网-采访-深度读北京
                       'http://interview.qianlong.com/beijinging/': 4308,  # 网站-垂直网站-千龙新闻网-采访-北京ING
                       'http://interview.qianlong.com/shouduhuiying/': 4309,  # 网站-垂直网站-千龙新闻网-采访-首度回应
                       'http://interview.qianlong.com/biyaopingtai/': 4310,  # 网站-垂直网站-千龙新闻网-采访-辟谣平台
                       'http://interview.qianlong.com/wangguanredian/': 4311,  # 网站-垂直网站-千龙新闻网-采访-网观热点
                       'http://interview.qianlong.com/xinhuofajingcaigushi/': 4312,  # 网站-垂直网站-千龙新闻网-采访-新活法精彩故事
                       'http://interview.qianlong.com/jizhewenji/': 4313,  # 网站-垂直网站-千龙新闻网-采访-记者文集
                       'http://interview.qianlong.com/zhibokuaixun/': 4314,  # 网站-垂直网站-千龙新闻网-采访-京城快讯
                       'http://interview.qianlong.com/lianjiezhongwai/': 4315,  # 网站-垂直网站-千龙新闻网-采访-联接中外
                       'http://interview.qianlong.com/kanjian/': 4316,  # 网站-垂直网站-千龙新闻网-采访-看见
                       'http://review.qianlong.com/': 4317,  # 网站-垂直网站-千龙新闻网-评论
                       'http://review.qianlong.com/qianlongwangping/': 4318,  # 网站-垂直网站-千龙新闻网-评论-首都评论
                       'http://review.qianlong.com/xspl/': 4319,  # 网站-垂直网站-千龙新闻网-评论-香山评论
                       'http://review.qianlong.com/zt/ztnuanping/index.shtml': 4320,  # 网站-垂直网站-千龙新闻网-评论-暖评
                       'http://www.71.cn/xjjpl/': 4321,  # 网站-垂直网站-千龙新闻网-评论-宣讲家评论
                       'http://review.qianlong.com/tebietuijian/': 4322,  # 网站-垂直网站-千龙新闻网-评论-特别推荐
                       'http://review.qianlong.com/500ziping/': 4323,  # 网站-垂直网站-千龙新闻网-评论-500字评
                       'http://review.qianlong.com/jinrimeiping/': 4324,  # 网站-垂直网站-千龙新闻网-评论-今日媒评
                       'http://review.qianlong.com/zuozhewenji/': 4325,  # 网站-垂直网站-千龙新闻网-评论-作者文集
                       'http://review.qianlong.com/wangpingxuehui/': 4326,  # 网站-垂直网站-千龙新闻网-评论-网评学会
                       'http://review.qianlong.com/zuixinpinglun/': 4327,  # 网站-垂直网站-千龙新闻网-评论-最新评论
                       'http://review.qianlong.com/wangyouruiping/': 4328,  # 网站-垂直网站-千龙新闻网-评论-网友锐评
                       'http://review.qianlong.com/dipingxian/': 4329,  # 网站-垂直网站-千龙新闻网-评论-地评线
                       'http://photo.qianlong.com/': 4330,  # 网站-垂直网站-千龙新闻网-图像
                       'http://photo.qianlong.com/txzb/': 4331,  # 网站-垂直网站-千龙新闻网-图像-图像直播
                       'http://photo.qianlong.com/xinhuofatuxianggushi/': 4332,  # 网站-垂直网站-千龙新闻网-图像-新活法·图像故事
                       'http://photo.qianlong.com/beijingwendu/': 4333,  # 网站-垂直网站-千龙新闻网-图像-北京温度
                       'http://photo.qianlong.com/dtxw/': 4334,  # 网站-垂直网站-千龙新闻网-图像-动图新闻
                       'http://photo.qianlong.com/yingtang/': 4335,  # 网站-垂直网站-千龙新闻网-图像-影堂
                       'http://photo.qianlong.com/VRxinwen/': 4336,  # 网站-垂直网站-千龙新闻网-图像-VR新闻
                       'http://tv.qianlong.com/': 4337,  # 网站-垂直网站-千龙新闻网-视频
                       'http://tv.qianlong.com/sd/': 4338,  # 网站-垂直网站-千龙新闻网-视频-首都
                       'http://v.qianlong.com/': 4339,  # 网站-垂直网站-千龙新闻网-视频-一分半
                       'http://tv.qianlong.com/gy/': 4340,  # 网站-垂直网站-千龙新闻网-视频-公益
                       'http://tv.qianlong.com/gx/': 4341,  # 网站-垂直网站-千龙新闻网-视频-观新
                       'http://tv.qianlong.com/syf/': 4342,  # 网站-垂直网站-千龙新闻网-视频-深夜访
                   'http://tv.qianlong.com/zt/wytmy/': 4343,  # 网站-垂直网站-千龙新闻网-视频-委员听民意
                                                       'http://special.qianlong.com/180824/': 4344,  # 网站-垂直网站-千龙新闻网-视频-委员读书会
    'http://tv.qianlong.com/2018/zt/wyjt/': 4345,  # 网站-垂直网站-千龙新闻网-视频-委员讲坛
    'http://tv.qianlong.com/wsdjt/': 4346,  # 网站-垂直网站-千龙新闻网-视频-网上大课堂
    'http://tv.qianlong.com/jsxw/': 4347,  # 网站-垂直网站-千龙新闻网-视频-即时新闻
    'http://comic.qianlong.com/': 4348,  # 网站-垂直网站-千龙新闻网-兔爷动漫
    'http://comic.qianlong.com/xmsxy/': 4349,  # 网站-垂直网站-千龙新闻网-兔爷动漫-漫说新语
    'http://comic.qianlong.com/lianzaimanhua/': 4350,  # 网站-垂直网站-千龙新闻网-兔爷动漫-连载漫画
    'http://comic.qianlong.com/ycdh/': 4351,  # 网站-垂直网站-千龙新闻网-兔爷动漫-原创动画
    # 'http://winter.qianlong.com/': 4352,  # 网站-垂直网站-千龙新闻网-冰雪
    'http://winter.qianlong.com/gundongxinwen/': 4353,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·要闻
    'http://winter.qianlong.com/bxdz/': 4354,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·大众
    'http://winter.qianlong.com/bxjj/': 4355,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·竞技
    'http://winter.qianlong.com/bxxt/': 4356,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·靓图
    'http://winter.qianlong.com/bxcy/': 4357,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·产业
    'http://winter.qianlong.com/bxbk/': 4358,  # 网站-垂直网站-千龙新闻网-冰雪-冰雪·百科
    'http://bbs.qianlong.com/': 4359,  # 网站-垂直网站-千龙新闻网-社区
    'http://paike.qianlong.com/': 4363,  # 网站-垂直网站-千龙新闻网-社区-拍客
    'http://chart.qianlong.com/newsy/': 4364,  # 网站-垂直网站-千龙新闻网-千龙图表
    'http://china.qianlong.com/': 4365,  # 网站-垂直网站-千龙新闻网-中国
    'http://china.qianlong.com/yaowenjujiao/': 4366,  # 网站-垂直网站-千龙新闻网-中国-要闻聚焦
    'http://china.qianlong.com/gaocengdongtai/': 4367,  # 网站-垂直网站-千龙新闻网-中国-高层动态
    'http://china.qianlong.com/xinzhengfengxiang/': 4368,  # 网站-垂直网站-千龙新闻网-中国-新政风向
    'http://china.qianlong.com/renshixinxi/': 4369,  # 网站-垂直网站-千龙新闻网-中国-人事信息
    'http://china.qianlong.com/fanfuchanglian/': 4370,  # 网站-垂直网站-千龙新闻网-中国-反腐倡廉
    'http://china.qianlong.com/difanglianbo/': 4371,  # 网站-垂直网站-千龙新闻网-中国-地方联播
    'http://china.qianlong.com/taigangao/': 4372,  # 网站-垂直网站-千龙新闻网-中国-台港澳
    'http://china.qianlong.com/qianlongshidian/': 4373,  # 网站-垂直网站-千龙新闻网-中国-千龙视点
    'http://china.qianlong.com/kanzhongguo/': 4374,  # 网站-垂直网站-千龙新闻网-中国-世界看中国
    'http://china.qianlong.com/shihaigouchen/': 4375,  # 网站-垂直网站-千龙新闻网-中国-史海钩沉
    'http://world.qianlong.com/': 4376,  # 网站-垂直网站-千龙新闻网-国际
    'http://world.qianlong.com/guojiyaowen/': 4377,  # 网站-垂直网站-千龙新闻网-国际-国际要闻
    'http://world.qianlong.com/rediantoushi/': 4378,  # 网站-垂直网站-千龙新闻网-国际-热点透视
    'http://world.qianlong.com/qushixingwen/': 4379,  # 网站-垂直网站-千龙新闻网-国际-趣事星闻
    'http://world.qianlong.com/shiqingbolan/': 4380,  # 网站-垂直网站-千龙新闻网-国际-世情博览
    'http://world.qianlong.com/tupianguoji/': 4381,  # 网站-垂直网站-千龙新闻网-国际-图片国际
    'http://world.qianlong.com/yuanchuang/': 4382,  # 网站-垂直网站-千龙新闻网-国际-原创
    'http://world.qianlong.com/renwujujiao/': 4383,  # 网站-垂直网站-千龙新闻网-国际-人物聚焦
    'http://world.qianlong.com/dianjipaihang/': 4384,  # 网站-垂直网站-千龙新闻网-国际-点击排行
    'http://scjg.qianlong.com/': 4385,  # 网站-垂直网站-千龙新闻网-市场监管
    'http://scjg.qianlong.com/gdxw/': 4386,  # 网站-垂直网站-千龙新闻网-市场监管-滚动新闻
    'http://scjg.qianlong.com/jgdt/': 4387,  # 网站-垂直网站-千龙新闻网-市场监管-监管动态
    'http://scjg.qianlong.com/qwfb/': 4388,  # 网站-垂直网站-千龙新闻网-市场监管-权威发布
    'http://scjg.qianlong.com/fwts/': 4389,  # 网站-垂直网站-千龙新闻网-市场监管-服务贴士
    'http://scjg.qianlong.com/jgfc/': 4390,  # 网站-垂直网站-千龙新闻网-市场监管-工作风采
    'http://scjg.qianlong.com/zthd/': 4391,  # 网站-垂直网站-千龙新闻网-市场监管-专题活动
    'http://scjg.qianlong.com/spzq/': 4392,  # 网站-垂直网站-千龙新闻网-市场监管-视频专区
    'http://scjg.qianlong.com/zlgs/': 4393,  # 网站-垂直网站-千龙新闻网-市场监管-质量公告
    'http://scjg.qianlong.com/ggjc/': 4394,  # 网站-垂直网站-千龙新闻网-市场监管-广告检测
    'http://scjg.qianlong.com/tsjb/': 4395,  # 网站-垂直网站-千龙新闻网-市场监管-投诉举报
    'http://zgc.qianlong.com/': 4396,  # 网站-垂直网站-千龙新闻网-中关村
    'http://zgc.qianlong.com/zhengcexinxi/': 4397,  # 网站-垂直网站-千龙新闻网-中关村-政策信息
    'http://zgc.qianlong.com/Focus%20interpretation/': 4398,  # 网站-垂直网站-千龙新闻网-中关村-聚焦解读
    'http://zgc.qianlong.com/Line%20fax/': 4399,  # 网站-垂直网站-千龙新闻网-中关村-一线传真
    'http://zgc.qianlong.com/Enterprise%20character/': 4400,  # 网站-垂直网站-千龙新闻网-中关村-企业·人物
    'http://zgc.qianlong.com/Forward%20position/': 4401,  # 网站-垂直网站-千龙新闻网-中关村-前沿阵地
    'http://zgc.qianlong.com/Cultural%20Park/': 4402,  # 网站-垂直网站-千龙新闻网-中关村-文化园区
    'http://thinktank.qianlong.com/': 4403,  # 网站-垂直网站-千龙新闻网-智库
    'http://thinktank.qianlong.com/zkdt/': 4404,  # 网站-垂直网站-千龙新闻网-智库-智库动态
    'http://thinktank.qianlong.com/yqyj/': 4405,  # 网站-垂直网站-千龙新闻网-智库-舆情研究
    'http://thinktank.qianlong.com/zkgc/': 4406,  # 网站-垂直网站-千龙新闻网-智库-智库观察
    'http://thinktank.qianlong.com/ckhy/': 4407,  # 网站-垂直网站-千龙新闻网-智库-参考活页
    'http://thinktank.qianlong.com/qlyqcp/': 4408,  # 网站-垂直网站-千龙新闻网-智库-千龙舆情产品
    'http://thinktank.qianlong.com/qlyqfw/': 4409,  # 网站-垂直网站-千龙新闻网-智库-千龙舆情服务

    }

    # http://review.qianlong.com/2019/0828/3393422.shtml
    # http://beijing.qianlong.com/2019/0718/3366479.shtml
    # http://china.qianlong.com/2019/0911/3401546.shtml
    # http://zhibo.qianlong.com/2019/0909/3400140.shtml

    # http://chart.qianlong.com/newsy/2019/0911/3401673.shtml
    # http://culture.qianlong.com/2019/0911/3401498.shtml
    # http://sports.qianlong.com/2019/0911/3401579.shtml
    # http://finance.qianlong.com/2019/0911/3401554.shtml
    # http://travel.qianlong.com/2019/0911/3401521.shtml
    # http://tech.qianlong.com/2019/0911/3401536.shtml
    # http://edu.qianlong.com/2019/0910/3400870.shtml
    # http://interview.qianlong.com/2019/0911/3401828.shtml
    # http://edu.qianlong.com/zhuanti/fthxjyst/2019/0909/3400219.shtml

    rules = (
        # http://tv.qianlong.com/2019/0910/3400702.shtml
        Rule(LinkExtractor(allow=(r'tv.qianlong.com/%s\d{2}/\d+\.s?htm' % datetime.today().strftime('%Y/%m')),
                           ), callback='parse_item_2', follow=False),
        Rule(LinkExtractor(allow=(r'qianlong.com.*?/%s\d{2}/\d+\.s?htm' % datetime.today().strftime('%Y/%m')),
                           ), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'qianlong.*?\.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', '/index.s?htm', 'bbs.qianlong.com')),
             process_request=otherurl_meta, follow=False),
    )

    custom_settings = {
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # 备用 使用隧道代理
    custom_settings['DOWNLOADER_MIDDLEWARES']['news_all.middlewares.ProxyRdMiddleware'] = 100

    def parse_item(self, response):
        try:
            xp = response.xpath
            title = xp('//div[@class="span12"]/h1/text()').extract_first() or self.get_page_title(response).split('-')[0]
            pubtime = xp('//span[@class="pubDate"]/text()').extract_first()
            origin_name = xp('//span[@class="source"]/a/text()').extract_first()
            content_div = xp('//div[@class="article-content"]')
            content, media, _, _ = self.content_clean(content_div)
            return self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                media=media,
                content=content,
            )
        except:
            return self.produce_debugitem(response, "xpath error")

    def parse_item2(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0]
            js_text = xp('//script[re:match(text(), "function swfURL")]').extract()[0]
            video_url = next(get_sub_str_ex(js_text, 'controls src="', '"', greedy=False))

            pubtime = xp('//span[@class="pubDate"]/text()').extract_first('')
            origin_name = xp('//span[@class="source"]/a/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content='<div>#{{1}}#</div>',
            media={},
            videos={'1': {'src': video_url}},
        )
