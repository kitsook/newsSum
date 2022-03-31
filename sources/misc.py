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

from lxml import html
from lxml.html.soupparser import fromstring
import traceback
import json

import urllib3

from logger import logger
from fetcher import read_http_page

from .base import BaseSource
from .base import RSSBase

class HackerNews(BaseSource):
    def get_id(self):
        return "hackernews"

    def get_desc(self):
        return "Hacker News"

    def get_articles(self):
        # Although the source is in RSS, the daily items are consolidated as CDATA.
        # Parse and break them down instead of using RSSBase
        rss_url = "http://www.daemonology.net/hn-daily/index.rss"
        resultList = []
        try:
            doc = html.document_fromstring(read_http_page(rss_url))
            for item in doc.xpath("//rss/channel/item"):
                title = (
                    item.xpath("title")[0].text
                    if len(item.xpath("title")) > 0
                    else "Daily Hacker News"
                )
                resultList.append(self.create_section(title))

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
                            resultList.append(
                                self.create_article(
                                    article.text.strip(), article.get("href")
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing Hacker News: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList

class RFACantonese(BaseSource):
    def get_id(self):
        return "rfa_cantonese"

    def get_desc(self):
        return "RFA 粵語部"

    def get_articles(self):
        resultList = []
        baseUrl = "https://www.rfa.org/cantonese"

        sections = [
            ("新聞", baseUrl + "/news"),
            ("港澳台新聞", baseUrl + "/news/htm"),
            ("評論", baseUrl + "/commentaries"),
            ("聚言堂", baseUrl + "/talkshows"),
            ("專題", baseUrl + "/features/hottopic"),
            ("多媒體", baseUrl + "/multimedia"),
        ]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = fromstring(read_http_page(url))
                for topic in doc.xpath('//div[contains(@id, "topstorywidefull")]'\
                        '|//div[contains(@class, "sectionteaser")]'\
                        '|//div[contains(@class, "single_column_teaser")]'\
                        '|//div[contains(@class, "two_featured")]'):
                    title = topic.xpath('h2/a')
                    intro = topic.xpath('p')

                    if title:
                        title_text = title[0].xpath('span')

                        resultList.append(
                            self.create_article(
                              title_text[0].text.strip(),
                              title[0].get("href"),
                              intro[0].text.strip() if intro and intro[0].text else None))

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList

class RFACantoneseRSS(RSSBase):
    def get_id(self):
        return "rfa_cantonese_rss"

    def get_desc(self):
        return "RFA 粵語部 RSS"

    def get_rss_links(self):
        return [
            ("RFA 自由亞洲電台粵語部", "https://www.rfa.org/cantonese/rss2.xml"),
        ]

class RFAEnglishRSS(RSSBase):
    def get_id(self):
        return "rfa_english_rss"

    def get_desc(self):
        return "Radio Free Asia RSS"

    def get_rss_links(self):
        return [
            ("Radio Free Asia", "https://www.rfa.org/english/rss2.xml"),
        ]

class TheInitium(BaseSource):
    def get_id(self):
        return "the_initium"

    def get_desc(self):
        return "端傳媒"

    def get_articles(self):
        resultList = []
        baseUrl = "https://api.theinitium.com"
        apiUrl = "https://api.theinitium.com/api/v2/channel/articles"

        sections = [
            ("最新", apiUrl + "/?language=zh-hant&slug=latest"),
            ("香港", apiUrl + "/?language=zh-hant&slug=hongkong"),
            ("國際", apiUrl + "/?language=zh-hant&slug=international"),
            ("大陸", apiUrl + "/?language=zh-hant&slug=mainland"),
            ("台灣", apiUrl + "/?language=zh-hant&slug=taiwan"),
            ("評論", apiUrl + "/?language=zh-hant&slug=opinion"),
            ("科技", apiUrl + "/?language=zh-hant&slug=technology"),
            ("風物", apiUrl + "/?language=zh-hant&slug=culture"),
            ("廣場", apiUrl + "/?language=zh-hant&slug=notes-and-letters"),
        ]

        headers = urllib3.make_headers(basic_auth="anonymous:GiCeLEjxnqBcVpnp6cLsUvJievvRQcAXLv")
        headers['Accept'] = "application/json"

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                contents = json.loads(read_http_page(url, headers=headers))
                for digest in contents["digests"]:
                    article = digest["article"]
                    if article and article["headline"] and article["url"]:
                        resultList.append(
                            self.create_article(
                                article["headline"].strip(),
                                baseUrl + article["url"],
                                article["lead"]))

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList