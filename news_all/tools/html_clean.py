#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 11:38
# @Author  : wjq
# @File    : html_clean.py
import json
import re
import urllib.parse
from copy import deepcopy
from urllib.parse import urljoin
from lxml.etree import Element
from lxml.html import _transform_result, basestring, fromstring
from lxml.html.clean import Cleaner
from scrapy import Selector
from scrapy.conf import settings
from scrapy.selector import SelectorList
from html import unescape
from news_all.tools.others import to_list


IMG_PATTERN = re.compile(r"""<img.*?src=['"](.*?)['"].*?>""")
img_prefix = settings.get('IMG_PREFIX', 'http://43.250.238.143/pic/article/')
video_pattern = re.compile(
    r"""<video.*?(?:data-src|src)=['"](.*?)['"].*?>.*?</video>""", re.S)
video_cover_pattern = re.compile(r"""poster=['"](.*?)['"].*?>""")


def video_fn(x, video_prefix=""):
    if x.startswith('http'):
        return x
    elif x.startswith(r'//'):
        return 'http:' + x
    else:
        return urljoin(video_prefix, x)


def img_fn(x):
    if x.startswith('http'):
        return x
    elif x.startswith(r'//'):  # etl不能下载//开头的url图片
        return 'http:' + x
    else:
        return urljoin(img_prefix, x)


re_tag = re.compile(r'<[^>]+>', re.S)


def html2text(divs):
    return re_tag.sub('', divs).strip()


def get_query_map(url):
    query_map = {}
    result = urllib.parse.urlsplit(url)
    query_map["scheme"] = result.scheme
    query_map["netloc"] = result.netloc
    query_map["path"] = result.path
    query_map["fragment"] = result.fragment
    query_map["query"] = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    return query_map


class Space(object):
    # 空格
    space_unicode = ['\u00A0', '\u0020', '\u3000']
    space_del = ['&nbsp;', '&ensp;', '&emsp;', '&thinsp;', '&zwnj;', '&zwj;']  # 删除
    space_res = ['\xa0']  # 保留
    """
    1.不间断空格\u00A0,主要用在office中,让一个单词在结尾处不会换行显示,快捷键ctrl+shift+space ;
    2.半角空格(英文符号)\u0020,代码中常用的;
    3.全角空格(中文符号)\u3000,中文文章中使用;
    """


class Interpunction(object):
    # 标点符号
    pass
    """
    符号 中文 英文
    句号 。 ,
    逗号 ， .
    顿号 、 \
    分号 ； ;
    冒号 ： :
    问号 ？ ?
    感叹号 ！ !
    引号 “” ""
    括号 （） ()
    省略号 …… …
    连接号 —— -
    书名号 《》 斜体
    """


def decode_html(s):
    """替换html‘&quot;’等转义内容为html实体"""
    return unescape(s)


class MyCleaner(Cleaner):
    del_attrs = [
        "style",  # 可有可无 Cleaner默认删除了style属性
        "href",
        "id",
        "name",
        "class",
        "width",
        "max-width",
        "min-width",
        "height",
        "max-height",
        "min-height",
        "top",
        "bottom",
        "right",
        "left",
        "align",
        "valign",
        "text-align, margin",
        "margin-left",
        "margin-right",
        "margin-top",
        "margin-bottom",
        "padding",
        "padding-top",
        "padding-right",
        "padding-left",
        "padding-bottom",
    ]
    
    # 标签保留
    whitelist_tags = set(["div", "p", "strong", "table", "th", "tr", "td", "thead", "tbody", "tfoot"])
    # A list of tags to include (default include all).
    remove_tags = set(['html', 'body', 'i', 'u', 'font', 's', 'em', 'hr', 'center', 'small', 'strike', 'a', 'audio'])
    # A list of tags to kill.  Killing also removes the tag's content,i.e. the whole subtree, not just the tag itself.
    kill_tags = set(["head", "iframe", "script", "button", "input", "style"])
    trans_tag_map = {'figure': 'div', 'figcaption': 'div'}
    kill_xpaths = [r'//*[contains(@style,"display:none")]',
                   r'//*[text()="相关链接："]/following::*', r'//*[text()="相关链接："]', '//*[contains(text(),"点击查看原文链接")]']
    safe_attrs = set(Cleaner.safe_attrs)  # 新浪客户端保留data-src
    safe_attrs.add('data-src')
    safe_attrs.add('data-original')
    
    def __init__(self, **kw):
        super(MyCleaner, self).__init__(**kw)
    
    def __call__(self, doc):
        super(MyCleaner, self).__call__(doc)
        for k, v in self.trans_tag_map.items():
            for el in doc.iter(k):
                el.tag = v
        del_attrs = set(self.del_attrs)
        for el in doc.iter(Element):
            attrib = el.attrib
            for aname in attrib.keys():
                if aname in del_attrs:
                    del attrib[aname]
    
    def clean_html(self, html, kill_xpaths=None):
        kill_xpaths = to_list(kill_xpaths) + to_list(self.kill_xpaths)
        
        if isinstance(html, basestring):
            doc = fromstring(html)  # 'HtmlElement' object
        else:
            doc = deepcopy(html)
        
        ele = []
        for i in kill_xpaths:
            try:
                ekill = doc.xpath(i, namespaces={"re": "http://exslt.org/regular-expressions"})
            except Exception as e:
                print('没有找到kill_xpath: %s, 报错: %s' % (i, e))
                continue
            ele.extend(ekill)
        
        for e in ele:
            try:
                e.getparent().remove(e)
            except AttributeError as er:  # 防止包含重复删除 'NoneType' object has no attribute 'remove'
                print('tag: %s, attr: %s 的节点: 已被删除' % (e.tag, e.attrib))
        
        result_type = type(html)
        self(doc)
        return _transform_result(result_type, doc)


class Image(object):
    Extensions = ['BMP', 'jpg', 'JPG', 'JPEG', 'png', 'PNG', 'gif', 'GIF']
    Patterns = [r'''<img.*?src=['"](.*?)['"].*?>''', ]
    Repl = '${{%s}}$'


class Video(object):
    Exceptions = []
    Tags = ['video', 'video//source', 'object', 'object//embed', 'iframe', 'embed']


class NewsBaseParser(object):
    """新闻清洗类"""
    
    cleaner = MyCleaner()
    
    def image_clean(self, content, img_re=None):
        if img_re:
            img_pattern = img_re
        else:
            img_pattern = IMG_PATTERN
        fr = re.finditer(img_pattern, content)
        media = {}
        new_content = ''
        
        for i, j in enumerate(fr):
            media.setdefault("images", {})
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '<br>${{%s}}$<br>' % (i + 1)
            content = content[end:]
            media['images'][str(i + 1)] = {"src": img_fn(j.group(1))}
        
        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media
    
    def video_clean(self, content, video_prefix=""):
        fr = re.finditer(video_pattern, content)
        videos = {}
        cover = []
        
        new_content = ''
        
        for i, j in enumerate(fr):
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '#{{%s}}#' % (i + 1)
            content = content[end:]
            cover_img = video_cover_pattern.search(j.group())
            if cover_img:
                cover.append(
                    cover_img.group(1))  # todo check 1新闻多个视频， 有的视频有cover有的无cover， cover=[ imgurl, None, None,...]?
            
            videos[str(i + 1)] = {"src": video_fn(j.group(1), video_prefix)}
        new_content += content
        return new_content, videos, cover
    
    def content_clean(self, content_div, need_video, kill_xpaths, img_re=None, video_prefix=""):
        c = self._myextract(content_div)
        c = self.cleaner.clean_html(c, kill_xpaths)  # 允许的类型：str
        cont_no_img, media = self.image_clean(c, img_re)  # 允许的类型：str

        cont_no_img = cont_no_img.replace('<p><br></p>', '').replace('<div><br></div>', '')\
            .replace('\r\n', '').replace('<div></div>', '').replace('<div>\n</div>', '')\
            .replace('<p><\p>', '').replace('</div>\n<div>','</div><div>').replace('\t','')\
            .replace('<div></div>', '')
        
        cont_no_img = re.sub(r'<p[^>]*>\s*</p>', '', cont_no_img, re.S)
        cont_no_img = re.sub(r'<div[^>]*>\s*</div>', '', cont_no_img, re.S)
        cont_no_img = re.sub(r'\n+', '', cont_no_img)
        cont_no_img = re.sub(r'(?:<br>)+', '<br>', cont_no_img)

        # 环球TIME app 出现过更新换行和制表符的情况
        if cont_no_img.find('\\n') >= 0:
            cont_no_img = cont_no_img.replace(r'\\n', '')  # replace('\\n', '') 只替换'\n'为''
        if cont_no_img.find('\\t') >= 0:
            cont_no_img = cont_no_img.replace(r'\\t', '')

        if not need_video:
            return cont_no_img, media, None, None
        else:
            cont_clean, videos, cover = self.video_clean(cont_no_img, video_prefix)
            return cont_clean, media, videos, cover
    
    def video_filter(self, sel_div):
        """
        过滤视频和flash

        常见播放器的type属性值:
        Flash:type="application/x-shockwave-flash";
        Windows media player:type="application/x-mplayer2";
        Realplayer:type="audio/x-pn-realaudio-plugin"。
        todo  了解video.js插件封装的视频组件, 用jQuery封装的视频插件
        """
        if isinstance(sel_div, str):
            sel_div = Selector(text=sel_div)
            #  or sel_div.xpath('//script[contains(@src, "swfobject.js") or contains(@src, "player")]')
            # http://theory.cyol.com/node_65535.htm?para1=News&para2=201909&para3=26&urlId=273949 误判
        if sel_div.xpath('//video') or sel_div.xpath('//object|embed[contains(@src,".swf")]') or sel_div.xpath(
            '//object|embed[@type="application/x-shockwave-flash" or @type="application/x-mplayer2" or @type="audio/x-pn-realaudio-plugin"]') or sel_div.xpath(
            '//iframe[contains(@src, "player")]'):
            return True
    
    def _myextract(self, select_div):
        """
        :param select_div:      Selector, SelectorList, str_list, or str
        :return:                str
        """
        # print('输入类型: %s' % type(select_div))
        
        if isinstance(select_div, (Selector, SelectorList)):  # SelectorList也是list, 所以首先判断SelectorList
            select_div = select_div.extract()  # 如果输入是Selector, 则此处得到str; 如果输入是SelectorList, 则此处得到str list
        if isinstance(select_div, list):
            c = ''.join(select_div)
        elif isinstance(select_div, str):
            c = select_div
        else:
            raise TypeError('select_div is not Selector, SelectorList, str_list or str, it is %s!' % type(select_div))
        return c


def json_load_html(html_str):
    html_str = html_str.replace('\r', '').replace('\n', '').replace('\t', '')
    html_str = re.sub('\'', '\"', html_str)
    html_str = re.sub("u'", "\"", html_str)
    return json.loads(html_str)


if __name__ == '__main__':
    # scrapy可识别正则, 但etree错误的xpath表达式, 所以加入namespaces={"re": "http://exslt.org/regular-expressions"}，
    # s = '''<div><p>关注留守儿童，公众号进行众筹</p><p>  请关注同花顺财经微信公众号(ths518)，获取更多财经资讯</p><img></div>'''
    s = '''<p style="text-indent: 0px; text-align: center;"><strong><a href="http://www.71.cn/2019/0318/1037526.shtml" target="_blank"><span style="text-decoration: underline;"><span style="text-indent: 2em; color: #0000ff; text-decoration: underline;">点此查看完整报告</span></span></a></strong></p><p align="center"><strong><font face="宋体"><a href="http://www.71.cn/2019/0829/1056402.shtml" target="_blank">点击观看完整报告视频</a></font></strong></p>'''
    cleaner = MyCleaner()
    # cc = cleaner.clean_html(s, kill_xpaths=['//*[re:match(text(),"关注\w{2,10}公众号")]'])
    cc = cleaner.clean_html(s,  kill_xpaths='//*[re:match(text(), "点击|此观|查看\w{0,8}视频|报告")]')
    print(cc)

    s = '&#x6253;&#x5F00;APP&#xFF0C;&#x67E5;&#x770B;&#x66F4;&#x591A;&#x7CBE;&#x5F69;&#x56FE;&#x7247;'
    print(decode_html(s))