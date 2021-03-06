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
import traceback

from logger import logger
from fetcher import read_http_page

from .base import BaseSource


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
