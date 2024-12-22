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

import json
import traceback

from fetcher import read_http_page
from logger import logger
from lxml import html

from .base import BaseSource, RDFBase, RSSBase


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


class AP(BaseSource):
    def get_id(self):
        return "ap"

    def get_desc(self):
        return "Associated Press"

    def get_articles(self):
        result_list = []

        root_url = "https://apnews.com"
        sections = [
            ("World", "/world-news"),
            ("US", "/us-news"),
            ("Politics", "/politics"),
            ("Sports", "/sports"),
            ("Entertainment", "/entertainment"),
            ("Business", "/business"),
            ("Science", "/science"),
        ]
        try:
            for title, base_url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then get page and parse
                doc = html.document_fromstring(read_http_page(root_url + base_url))
                for article in doc.xpath(
                    '//*[self::h1 or self::h2 or self::h3][contains(@class, "PagePromo-title")]'
                    ):
                    the_link = None
                    the_text = None

                    link_element = article.xpath('a[contains(@class, "Link")]')
                    if link_element and len(link_element) > 0:
                        the_link = link_element[0].xpath("@href")[0]

                    text_element = article.xpath('a/span[contains(@class, "PagePromoContentIcons-text")]')
                    if text_element and len(text_element) > 0:
                        the_text = text_element[0].text

                    if the_link and the_text:
                        result_list.append(
                            self.create_article(the_text.strip(), the_link)
                        )
        except Exception as e:
            logger.exception("Problem processing AP: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list


class Reuters(RSSBase):
    def get_id(self):
        return "reuters"

    def get_desc(self):
        return "Reuters"

    def get_rss_links(self):
        return [
            (
                "Reuters",
                "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com",
            ),
        ]
