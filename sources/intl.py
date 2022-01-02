# -*- coding: utf-8 -*-

# Copyright (c) 2016 Clarence Ho (clarenceho at gmail dot com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .base import RSSBase
from .base import RDFBase


class BBCWorld(RSSBase):
    def get_id(self):
        return "bbcworld"

    def get_desc(self):
        return "BBC World"

    def get_rss_links(self):
        return [
            ("World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
            ("Asia", "http://feeds.bbci.co.uk/news/world/asia/rss.xml"),
        ]


class FTChinese(RSSBase):
    def get_id(self):
        return "ftchinese"

    def get_desc(self):
        return "FT中文网"

    def get_rss_links(self):
        return [
            ("每日更新", "http://big5.ftchinese.com/rss/feed"),
            ("今日焦点", "http://big5.ftchinese.com/rss/news"),
            ("十大熱門文章", "http://big5.ftchinese.com/rss/hotstoryby7day"),
            ("生活時尚", "http://big5.ftchinese.com/rss/lifestyle"),
            ("《馬丁 沃爾夫》", "http://big5.ftchinese.com/rss/column/007000012"),
        ]


class DeutscheWelle(RDFBase):
    def get_id(self):
        return "dw"

    def get_desc(self):
        return "德國之聲"

    def get_rss_links(self):
        return [
            ("德國之聲", "http://rss.dw.com/rdf/rss-chi-all"),
        ]


class WSJChinese(RSSBase):
    def get_id(self):
        return "wsjcn"

    def get_desc(self):
        return "華爾街日報"

    def get_rss_links(self):
        return [
            ("華爾街日報", "https://cn.wsj.com/zh-hant/rss"),
        ]
