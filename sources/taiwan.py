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

import re
from datetime import datetime, timedelta
from lxml import html
import json
import urllib
from urllib.parse import urlparse
import traceback
import pytz

from logger import logger
from fetcher import read_http_page

from .base import BaseSource
from .base import RSSBase
from .base import RDFBase


class LibertyTimes(BaseSource):
    def get_id(self):
        return "libertytimes"

    def get_desc(self):
        return "自由時報"

    def get_articles(self):
        num_pages = 2
        baseUrl = "https://news.ltn.com.tw"

        resultList = []
        sections = [
            ("熱門", baseUrl + "/ajax/breakingnews/popular/"),
            ("政治", baseUrl + "/ajax/breakingnews/politics/"),
            ("社會", baseUrl + "/ajax/breakingnews/society/"),
            ("地方", baseUrl + "/ajax/breakingnews/local/"),
            ("生活", baseUrl + "/ajax/breakingnews/life/"),
            ("國際", baseUrl + "/ajax/breakingnews/world/"),
        ]

        try:
            for page in range(1, num_pages):
                for (title, url) in sections:
                    url = url + str(page)
                    # for each section, insert a title...
                    resultList.append(self.create_section(title))
                    # ... then parse the page and extract article links
                    result = json.loads(read_http_page(url + str(page)).decode("UTF-8"))
                    if result.get("code", 0) == 200:
                        data = result.get("data", [])
                        for key in data.keys():
                            title = data[key].get("title", None)
                            url = data[key].get("url", None)
                            abstract = data[key].get("summary", None)
                            if title and url:
                                resultList.append(
                                    self.create_article(title, url, abstract)
                                )

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList


class UnitedDailyNewsRSS(RSSBase):
    def get_id(self):
        return "udn"

    def get_desc(self):
        return "聯合新聞網"

    def get_rss_links(self):
        return [
            ("要聞", "http://udn.com/rssfeed/news/2/6638?ch=news"),
            ("全球", "http://udn.com/rssfeed/news/2/7225?ch=news"),
            ("兩岸", "http://udn.com/rssfeed/news/2/6640?ch=news"),
            ("地方", "http://udn.com/rssfeed/news/2/6641?ch=news"),
            ("評論", "http://udn.com/rssfeed/news/2/6643?ch=news"),
            ("產經", "http://udn.com/rssfeed/news/2/6644?ch=news"),
            ("股市", "http://udn.com/rssfeed/news/2/6645?ch=news"),
            ("娛樂", "http://udn.com/rssfeed/news/2/6648?ch=news"),
            ("運動", "http://udn.com/rssfeed/news/2/7227?ch=news"),
            ("社會", "http://udn.com/rssfeed/news/2/6639?ch=news"),
            ("生活", "http://udn.com/rssfeed/news/2/6649?ch=news"),
            ("數位", "http://udn.com/rssfeed/news/2/7226?ch=news"),
        ]


class MoneyUnitedDailyNewsRSS(RSSBase):
    @staticmethod
    def is_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def get_id(self):
        return "money-udn"

    def get_desc(self):
        return "經濟日報-聯合新聞網"

    def get_rss_links(self):
        resultList = []
        try:
            rss_list_url = "https://money.udn.com/rssfeed/lists/1001"
            doc = html.document_fromstring(read_http_page(rss_list_url))
            for aLink in doc.get_element_by_id("rss_list").xpath("div/div/dl/dt/a"):
                if aLink.xpath("text()") and MoneyUnitedDailyNewsRSS.is_url(
                    aLink.get("href")
                ):
                    resultList.append((aLink.xpath("text()"), aLink.get("href")))
        except Exception as e:
            logger.exception("Problem fetching rss links: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList


class AppleDailyTaiwan(BaseSource):
    _base_url = "https://tw.appledaily.com"

    def _find_date_id(self, raw_page):
        m_d = re.search(r"Fusion\.deployment\=\"([0-9]+)\"", str(raw_page))

        tw_time = datetime.now(pytz.timezone("Hongkong"))  # same tz as hk
        if tw_time.hour < 4:
            tw_time = tw_time - timedelta(days=1)
        result_date = tw_time.strftime("%Y%m%d")

        result_d = 0
        if m_d:
            result_d = m_d.group(1)

        return result_date, result_d

    def _get_collection(self, section_id, date_id, d):
        payload_query = {
            "feedOffset": 0,
            "feedQuery": 'taxonomy.primary_section._id:"{}" AND type:story AND editor_note:"{}"'.format(
                section_id, date_id
            ),
            "feedSize": 100,
            "sort": "location:asc",
        }
        payload_query = urllib.parse.quote(json.dumps(payload_query))

        query_url = (
            self._base_url
            + "/pf/api/v3/content/fetch/query-feed?query={}&d={}&_website=hk-appledaily".format(
                payload_query, d
            )
        )
        return read_http_page(query_url)

    def get_id(self):
        return "appledailytw"

    def get_desc(self):
        return "蘋果日報(台灣)"

    def get_articles(self):
        resultList = []
        sections = [
            ("要聞", "/daily/headline", self._base_url + "/daily/headline/"),
            ("娛樂", "/daily/entertainment", self._base_url + "/daily/entertainment/"),
            ("國際", "/daily/international", self._base_url + "/daily/international/"),
            ("財經", "/daily/finance", self._base_url + "/daily/finance/"),
            ("副刊", "/daily/lifestyle", self._base_url + "/daily/lifestyle/"),
            ("體育", "/daily/sports", self._base_url + "/daily/sports/"),
            ("地產", "/daily/home", self._base_url + "/daily/home/"),
        ]

        try:
            for (title, section_id, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then retrieve the json content
                raw_page = read_http_page(url)
                date_id, d = self._find_date_id(raw_page)
                if date_id and d:
                    raw_result = self._get_collection(section_id, date_id, d)
                    result = json.loads(raw_result)
                    for article in result["content_elements"]:
                        desc = article["headlines"]["basic"]
                        href = article["website_url"]
                        abstract = None
                        if (
                            "content_elements" in article
                            and len(article["content_elements"]) > 1
                            and "content" in article["content_elements"][0]
                        ):
                            abstract = article["content_elements"][0]["content"]
                        if desc and href:
                            resultList.append(
                                self.create_article(
                                    desc.strip(), self._base_url + href, abstract
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList


class TaipeiTimes(RDFBase):
    def get_id(self):
        return "taipeitimes"

    def get_desc(self):
        return "Taipei Times(臺北時報)"

    def get_rss_links(self):
        return [
            ("Front Page", "http://www.taipeitimes.com/xml/front.rss"),
            ("Taiwan News", "http://www.taipeitimes.com/xml/taiwan.rss"),
            ("World News", "http://www.taipeitimes.com/xml/world.rss"),
            ("Business", "http://www.taipeitimes.com/xml/biz.rss"),
            ("Sports", "http://www.taipeitimes.com/xml/sport.rss"),
            ("Features", "http://www.taipeitimes.com/xml/feat.rss"),
        ]


class ChinaTimes(BaseSource):
    def get_id(self):
        return "chinatimes"

    def get_desc(self):
        return "中國時報"

    def get_articles(self):
        resultList = []
        baseUrl = "https://www.chinatimes.com"

        sections = [
            ("政治", baseUrl + "/politic/?chdtv"),
            ("言論", baseUrl + "/opinion/?chdtv"),
            ("生活", baseUrl + "/life/?chdtv"),
            ("娛樂", baseUrl + "/star/?chdtv"),
            ("財經", baseUrl + "/money/?chdtv"),
            ("社會", baseUrl + "/society/?chdtv"),
            ("話題", baseUrl + "/hottopic/?chdtv"),
            ("國際", baseUrl + "/world/?chdtv"),
            ("軍事", baseUrl + "/armament/?chdtv"),
            ("兩岸", baseUrl + "/chinese/?chdtv"),
            ("時尚", baseUrl + "/fashion/?chdtv"),
            ("體育", baseUrl + "/sports/?chdtv"),
            ("科技", baseUrl + "/technologynews/?chdtv"),
            ("玩食", baseUrl + "/travel/?chdtv"),
            ("新聞專輯", baseUrl + "/album/?chdtv"),
        ]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.xpath(
                    '//section[contains(@class, "article-list")]/ul//li//h3[contains(@class, "title")]//a'
                ):
                    if topic.text and topic.get("href"):
                        resultList.append(
                            self.create_article(topic.text.strip(), topic.get("href"))
                        )

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList


class CommercialTimes(RSSBase):
    def get_id(self):
        return "commercialtimes"

    def get_desc(self):
        return "工商時報"

    def get_rss_links(self):
        return [
            ("財經要聞", "https://ctee.com.tw/feed"),
        ]


class Storm(BaseSource):
    def get_id(self):
        return "storm"

    def get_desc(self):
        return "風傳媒"

    def get_articles(self):
        resultList = []

        pages = 3
        sections = [
            ("新聞", "https://www.storm.mg/articles"),
            ("評論", "https://www.storm.mg/all-comment"),
            ("財經", "https://www.storm.mg/category/23083"),
            ("生活", "https://www.storm.mg/category/104"),
            ("人物", "https://www.storm.mg/category/171151"),
            ("華爾街日報", "https://www.storm.mg/category/173479"),
            ("新新聞", "https://www.storm.mg/category/87726"),
        ]

        try:
            for (title, url) in sections:
                resultList.append(self.create_section(title))
                for page in range(1, pages + 1):
                    # for each section, insert a title...
                    # ... then parse the page and extract article links
                    doc = html.document_fromstring(
                        read_http_page(url + "/" + str(page))
                    )

                    # get the first featured article
                    topic = doc.xpath(
                        '//div[contains(@class, "category_top_card")]/div[contains(@class, "card_img_wrapper")]'
                    )
                    if topic:
                        title = topic[0].xpath(
                            'div[contains(@class, "card_inner_wrapper")]/a[contains(@class, "link_title")]'
                        )
                        intro = topic[0].xpath(
                            'div[contains(@class, "card_inner_wrapper")]/a[contains(@class, "card_substance")]'
                        )
                        title_text = title[0].xpath("h2/text()") if title else None
                        if title and title_text and title[0].get("href"):
                            resultList.append(
                                self.create_article(
                                    title_text[0].strip(),
                                    title[0].get("href"),
                                    intro[0].text.strip()
                                    if intro and intro[0].text
                                    else None,
                                )
                            )

                    for topic in doc.xpath(
                        '//div[contains(@class, "category_cards_wrapper")]/div[contains(@class, "category_card")]'
                    ):
                        title = topic.xpath(
                            'div[contains(@class, "card_inner_wrapper")]/a[contains(@class, "link_title")]'
                        )
                        intro = topic.xpath(
                            'div[contains(@class, "card_inner_wrapper")]/a[contains(@class, "card_substance")]'
                        )
                        title_text = title[0].xpath("h3/text()") if title else None

                        if title and title_text and title[0].get("href"):
                            resultList.append(
                                self.create_article(
                                    title_text[0].strip(),
                                    title[0].get("href"),
                                    intro[0].text.strip()
                                    if intro and intro[0].text
                                    else None,
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing url: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return resultList
