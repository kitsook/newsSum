# -*- coding: utf-8 -*-

# Copyright (c) 2020 Clarence Ho (clarenceho at gmail dot com)
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

import urllib3
from lxml import html
from lxml.html.soupparser import fromstring

from fetcher import read_http_page
from logger import logger

from .base import BaseSource, RSSBase


class HackerNews(BaseSource):
    def get_id(self):
        return "hackernews"

    def get_desc(self):
        return "Hacker News"

    def get_articles(self):
        # Although the source is in RSS, the daily items are consolidated as CDATA.
        # Parse and break them down instead of using RSSBase
        rss_url = "http://www.daemonology.net/hn-daily/index.rss"
        result_list = []
        try:
            doc = html.document_fromstring(read_http_page(rss_url))
            for item in doc.xpath("//rss/channel/item"):
                title = (
                    item.xpath("title")[0].text
                    if len(item.xpath("title")) > 0
                    else "Daily Hacker News"
                )
                result_list.append(self.create_section(title))

                description = (
                    item.xpath("description")[0]
                    if len(item.xpath("description")) > 0
                    else None
                )
                if description is not None:
                    for article in description.xpath(
                        'ul/li/span[@class="storylink"]/a'
                    ):
                        if article.text and article.get("href"):
                            result_list.append(
                                self.create_article(
                                    article.text.strip(), article.get("href")
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing HackerNews: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "http://www.daemonology.net/favicon.ico"


class RFACantonese(BaseSource):
    def get_id(self):
        return "rfa_cantonese"

    def get_desc(self):
        return "RFA 粵語部"

    def get_articles(self):
        result_list = []
        site_url = "https://www.rfa.org/"
        base_url = site_url + "cantonese"

        sections = [
            ("港澳台新聞", base_url + "/htm"),
            ("世界新聞", base_url + "/world"),
            ("專題", base_url + "/in-depth"),
            ("司法", base_url + "/law-justice"),
            ("觀點", base_url + "/opinion"),
            ("事實查核", base_url + "/fact-check"),
            ("科技", base_url + "/technology"),
            ("影片", base_url + "/video"),

        ]

        try:
            for title, url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = fromstring(read_http_page(url))
                for topic in doc.xpath(
                    '//article/div[contains(@class, "c-sm-text")]'
                    '|//article/div[contains(@class, "c-md-text")]'
                    '|//article/div/div[contains(@class, "c-xl-text")]'
                ):
                    title = topic.xpath("h2/a")
                    intro = topic.xpath("p")

                    if title:
                        title_text = title[0].text

                        result_list.append(
                            self.create_article(
                                title_text.strip(),
                                site_url + title[0].get("href"),
                                intro[0].text.strip()
                                if intro and intro[0].text
                                else None,
                            )
                        )

        except Exception as e:
            logger.exception("Problem processing RFACantonese: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "https://www.rfa.org/favicon.ico"


class RFACantoneseRSS(RSSBase):
    def get_id(self):
        return "rfa_cantonese_rss"

    def get_desc(self):
        return "RFA 粵語部 RSS"

    def get_rss_links(self):
        return [
            ("RFA 自由亞洲電台粵語部", "https://www.rfa.org/cantonese/rss2.xml"),
        ]

    def get_icon_url(self):
        return "https://www.rfa.org/favicon.ico"


class RFAEnglishRSS(RSSBase):
    def get_id(self):
        return "rfa_english_rss"

    def get_desc(self):
        return "Radio Free Asia RSS"

    def get_rss_links(self):
        return [
            ("Radio Free Asia", "https://www.rfa.org/english/rss2.xml"),
        ]

    def get_icon_url(self):
        return "https://www.rfa.org/favicon.ico"


class TheInitium(RSSBase):
    def get_id(self):
        return "the_initium"

    def get_desc(self):
        return "端傳媒"

    def get_rss_links(self):
        return [
            ("端傳媒", "https://theinitium.com/feed"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAKlBMVEVHcEwos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8Mos8MhE2vAAAAADXRSTlMA7WfCQFAxEt+dh/aaB6A6SwAAAMNJREFUKJF9k1kSxCAIRAE1bsP9rzugcSlD2T8xPOmAEgCgxPgDeIpDZnTlgSXHqpp4CmkwWrFMIVCWdE6xw5kRxvZHvXxb8gcC+EFxQL/VESuzOv8GhF1RvqvP+nF9nWlWdDDtEKU2AcGfqMUfKLrDEnKR9GzDzE42kA1JLI1auoJ0d4VX22tB11Zas4Z6HCXdUDs+HQXj9N6D15OPJxtXpot60HHZsE3F5rkC+uJmzduAdZtkj+YrmoO2D/Xq+vs7/AG3ngrWRgkWkgAAAABJRU5ErkJggg=="
