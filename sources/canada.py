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
import traceback
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import pytz
from lxml import html

from fetcher import read_http_page
from logger import logger

from .base import BaseSource, RSSBase


class MingPaoVancouver(BaseSource):
    def get_id(self):
        return "mingpaovancouver"

    def get_desc(self):
        return "明報加西版(溫哥華)"

    def get_articles(self):
        # get date first
        date_url = "http://www.mingpaocanada.com/Van/"
        van_time = datetime.now(pytz.timezone("America/Vancouver"))
        if van_time.hour < 4:
            van_time = van_time - timedelta(days=1)
        the_date = van_time.strftime("%Y%m%d")

        try:
            doc = html.document_fromstring(read_http_page(date_url))
            for a_link in doc.get_element_by_id("mp-menu").xpath("//div/ul/li/a"):
                if a_link.text_content() == "明報首頁":
                    href = a_link.attrib["href"]
                    match = re.match(r"htm\/News\/(\d{8})\/main_r\.htm", href)
                    if match and match.lastindex == 1:
                        the_date = match.group(1)
                    else:
                        logger.info("no date found. using system date: " + the_date)
        except Exception as e:
            logger.exception("Problem getting date: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        result_list = []
        news_url = "http://www.mingpaocanada.com/Van/htm/News/"
        sections = [
            (
                "要聞",
                news_url + the_date + "/VAindex_r.htm",
            ),
            (
                "加國新聞",
                news_url + the_date + "/VBindex_r.htm",
            ),
            (
                "社區新聞",
                news_url + the_date + "/VDindex_r.htm",
            ),
            (
                "港聞",
                news_url + the_date + "/HK-VGindex_r.htm",
            ),
            (
                "國際",
                news_url + the_date + "/VTindex_r.htm",
            ),
            (
                "中國",
                news_url + the_date + "/VCindex_r.htm",
            ),
            (
                "經濟",
                news_url + the_date + "/VEindex_r.htm",
            ),
            (
                "體育",
                news_url + the_date + "/VSindex_r.htm",
            ),
            (
                "影視",
                news_url + the_date + "/HK-MAindex_r.htm",
            ),
            (
                "副刊",
                news_url + the_date + "/WWindex_r.htm",
            ),
        ]

        base_url = news_url + the_date + "/"
        try:
            for title, url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(
                    read_http_page(url).decode("big5-hkscs", errors="ignore")
                )
                for topic in doc.xpath('//h4[contains(@class, "listing-link")]/a'):
                    if topic.text and topic.get("href"):
                        result_list.append(
                            self.create_article(
                                topic.text.strip(), base_url + topic.get("href")
                            )
                        )

        except Exception as e:
            logger.exception("Problem processing MingPaoVancouver: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "https://news.mingpao.com/favicon.ico"


class SingTaoCanada(BaseSource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_sections(self):
        pass

    def get_articles(self):
        result_list = []
        sections = self.get_sections()

        try:
            for title, url, pages in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                for page in range(1, pages + 1):
                    # ... then parse the page and extract article links
                    doc = html.document_fromstring(
                        read_http_page(
                            url + "&page=" + str(page), {"edition": "vancouver"}
                        ).decode("utf-8")
                    )

                    # top story
                    top_story_link = doc.xpath(
                        '(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a'
                    )
                    top_story_text = doc.xpath(
                        '(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a/div/h3'
                    )
                    if top_story_link and top_story_text:
                        result_list.append(
                            self.create_article(
                                top_story_text[0].text.strip(),
                                top_story_link[0].get("href"),
                            )
                        )

                    for topic in doc.xpath(
                        '(//div[@class="td-ss-main-content"])[1]/div[contains(@class, "td-animation-stack")]/div[@class="item-details"]/h3/a'
                    ):
                        if topic.text and topic.get("href"):
                            result_list.append(
                                self.create_article(
                                    topic.text.strip(), topic.get("href")
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing SingTaoCanada: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAflBMVEU2THk2THk2THk2THk2THk2THkySXd8iKN0gJ1LWH4rRHQkQ3RRZ4wAA0ceO25CR3CIkKi1h5rDdYTXg4w2THllcJD////BxtK3vMvEAB/RSVjT1t9/c5DEDy2TnLKgqbzNMkPrur7RXGnk5uv57u/kp62rssLxzc/DorEFLWeqHjCtAAAAFXRSTlMCK6X/42f//////////////////9iJg58gAAAByklEQVR4AYWTh2KbMBBAMXK0rZ6HpCO4Og+ihP//wR5hdLePLb0brKZpdq34M/t21zAv4h+8cDwf5Mrvxq6Z8iu9YKSQ1m1wQNtwvDeHQ/gyAd7642nl7KW4sCBYiCkjYk7ZnbuNVxb2SwZI/UTqr93XjVUQn0LhRmASuk35MUOgUlKvr+p6uz+Y19ffMvTPNPRPhDS8McPQ/ZzBYMX0rJWuw0/CliFcIyeJESbhfr+/v/0oiHiA50yehImfBKn9YSGycJ/4OYP1eiHCuUtvt/OZe+gePMXChFxxJb2nYUjvQ9fdjm4TNqQ+Tnz0H6ejdlsGZxlnBW/BuTAGx2sIm+CQSBUsFjKRsCVX23uTKdtFCAmJR5OpgwYhxsHrnONzTHIRrIZEmeBJiSdlGHympH4UCqEuMKJGQiMtRjUW4PO1hAh25P7kZ2OSj9ZKbjeErcl+7KPyqqqohEE+0yrKqNRWgmpFVXWhQtpUQkkaQy3FrCU8RK08QFTgRQHtALRSCGIVuK50BYLj6lzb6RCklMZ+CnsxY+sISEAFSRNlnpSCuTTtKqAiQE+18EnF9Sdr+ddbDWElL7wKLiQW/vfz7hpm1172f+TS8uw3poU3cVjsnpwAAAAASUVORK5CYII="


class SingTaoVancouver(SingTaoCanada):
    def get_id(self):
        return "singtaovancouver"

    def get_desc(self):
        return "星島日報(溫哥華)"

    def get_sections(self):
        return [
            (
                "焦點",
                "https://www.singtao.ca/category/2235233-%E6%BA%AB%E5%93%A5%E8%8F%AF%E7%84%A6%E9%BB%9E/?variant=zh-hk",
                1,
            ),
            (
                "省市",
                "https://www.singtao.ca/category/65-%E6%BA%AB%E5%93%A5%E8%8F%AF%E7%9C%81%E5%B8%82/?variant=zh-hk",
                1,
            ),
            (
                "港聞",
                "https://www.singtao.ca/category/57-%E6%BA%AB%E5%93%A5%E8%8F%AF%E6%B8%AF%E8%81%9E/?variant=zh-hk",
                3,
            ),
            (
                "國際",
                "https://www.singtao.ca/category/56-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%9C%8B%E9%9A%9B/?variant=zh-hk",
                1,
            ),
            (
                "兩岸",
                "https://www.singtao.ca/category/1611587-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%85%A9%E5%B2%B8/?variant=zh-hk",
                1,
            ),
            (
                "新移民",
                "https://www.singtao.ca/category/2038601-%E6%BA%AB%E5%93%A5%E8%8F%AF%E6%96%B0%E7%A7%BB%E6%B0%91/?variant=zh-hk",
                1,
            ),
            (
                "科技",
                "https://www.singtao.ca/category/2054189-%E6%BA%AB%E5%93%A5%E8%8F%AF%E7%A7%91%E6%8A%80/?variant=zh-hk",
                1,
            ),
            (
                "財經",
                "https://www.singtao.ca/category/61-%E6%BA%AB%E5%93%A5%E8%8F%AF%E8%B2%A1%E7%B6%93/?variant=zh-hk",
                1,
            ),
            (
                "體育",
                "https://www.singtao.ca/category/60-%E6%BA%AB%E5%93%A5%E8%8F%AF%E9%AB%94%E8%82%B2/?variant=zh-hk",
                1,
            ),
            (
                "娛樂",
                "https://www.singtao.ca/category/62-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%A8%9B%E6%A8%82/?variant=zh-hk",
                1,
            ),
        ]


class SingTaoToronto(SingTaoCanada):
    def get_id(self):
        return "singtaotoronto"

    def get_desc(self):
        return "星島日報(多倫多)"

    def get_sections(self):
        return [
            (
                "焦點",
                "https://www.singtao.ca/category/2235233-%E5%A4%9A%E5%80%AB%E5%A4%9A%E7%84%A6%E9%BB%9E/?variant=zh-hk",
                1,
            ),
            (
                "城市",
                "https://www.singtao.ca/category/53-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%9F%8E%E5%B8%82/?variant=zh-hk",
                1,
            ),
            (
                "港聞",
                "https://www.singtao.ca/category/57-%E5%A4%9A%E5%80%AB%E5%A4%9A%E6%B8%AF%E8%81%9E/?variant=zh-hk",
                1,
            ),
            (
                "國際",
                "https://www.singtao.ca/category/56-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%9C%8B%E9%9A%9B/?variant=zh-hk",
                1,
            ),
            (
                "兩岸",
                "https://www.singtao.ca/category/1611587-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%85%A9%E5%B2%B8/?variant=zh-hk",
                1,
            ),
            (
                "財經",
                "https://www.singtao.ca/category/61-%E5%A4%9A%E5%80%AB%E5%A4%9A%E8%B2%A1%E7%B6%93/?variant=zh-hk",
                1,
            ),
            (
                "體育",
                "https://www.singtao.ca/category/60-%E5%A4%9A%E5%80%AB%E5%A4%9A%E9%AB%94%E8%82%B2/?variant=zh-hk",
                1,
            ),
            (
                "娛樂",
                "https://www.singtao.ca/category/62-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%A8%9B%E6%A8%82/?variant=zh-hk",
                1,
            ),
        ]


class SingTaoCalgary(SingTaoCanada):
    def get_id(self):
        return "singtaocalgary"

    def get_desc(self):
        return "星島日報(卡加利)"

    def get_sections(self):
        return [
            (
                "焦點",
                "https://www.singtao.ca/category/2235233-%E5%8D%A1%E5%8A%A0%E5%88%A9%E7%84%A6%E9%BB%9E/?variant=zh-hk",
                1,
            ),
            (
                "省市",
                "https://www.singtao.ca/category/65-%E5%8D%A1%E5%8A%A0%E5%88%A9%E7%9C%81%E5%B8%82/?variant=zh-hk",
                1,
            ),
            (
                "港聞",
                "https://www.singtao.ca/category/57-%E5%8D%A1%E5%8A%A0%E5%88%A9%E6%B8%AF%E8%81%9E/?variant=zh-hk",
                3,
            ),
            (
                "國際",
                "https://www.singtao.ca/category/56-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%9C%8B%E9%9A%9B/?variant=zh-hk",
                1,
            ),
            (
                "兩岸",
                "https://www.singtao.ca/category/1611587-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%85%A9%E5%B2%B8/?variant=zh-hk",
                1,
            ),
            (
                "財經",
                "https://www.singtao.ca/category/61-%E5%8D%A1%E5%8A%A0%E5%88%A9%E8%B2%A1%E7%B6%93/?variant=zh-hk",
                1,
            ),
            (
                "體育",
                "https://www.singtao.ca/category/60-%E5%8D%A1%E5%8A%A0%E5%88%A9%E9%AB%94%E8%82%B2/?variant=zh-hk",
                1,
            ),
            (
                "娛樂",
                "https://www.singtao.ca/category/62-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%A8%9B%E6%A8%82/?variant=zh-hk",
                1,
            ),
        ]


class TheProvince(RSSBase):
    def get_id(self):
        return "theprovince"

    def get_desc(self):
        return "The Province"

    def get_rss_links(self):
        return [
            ("The Province", "https://theprovince.com/feed"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcBAMAAACAI8KnAAAAHlBMVEUAc60Ac60AbKpMiLinwNiCpslvm8L////K1+bo7vQ2JTR1AAAAAXRSTlP9g+pWxwAAAFtJREFUeAFjQAOCKIAMrpKSEhJX2MXFNQnBVS0HAiNUbhESt6K9vFQRwS1TKy9B5iqjclVRuJXTy8tQTZ6Ewq1QROKWGoNciTAKKEceV23mNGTvCykpoQcO5VwAakox2FOHH7sAAAAASUVORK5CYII="


class VancouverSun(RSSBase):
    def get_id(self):
        return "vancouversun"

    def get_desc(self):
        return "Vancouver Sun"

    def get_rss_links(self):
        return [
            ("Vancouver News, Top Stories", "https://vancouversun.com/feed"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAaVBMVEUwZFAsYk0nX0o9bFlvjoJmiHpgg3VDcF4TVz+Pppw7a1g0Z1OEnpP////s8O60w70ZWULG0czc4+BJdGMAUjn4+vl+mY5Zfm/P2NQgXEa5x8HI0s4mX0p3k4ebr6YOVj6muLCYraTf5eOe0JixAAAA20lEQVR4Ac2Ph5EEIQwEpfVuWG9hbf5Bvri38AkcHnVNdYnedHDAbM/X4bEwiuOEOY6iNIvzoiwdWgEpc6rqpq3Tuuv5LxxGSKFphwkDD2p2YLMgX2ndBq0GMtXueNcDuuEkHxakAZWxk+QZ42muvtmgyoCYnHECQhrugbE3UvClWS3aCUAiSk/azrlEmkoou5ATqDu1xSYCrtWlGdA2RMUr+2Qe7LCJ0maGUZ2e9IK03jwCs8dPBjFY6upoJOk7aVWZ7eiZsmr0GfHM9jjv+jJM/+jnYVZD7zo+ADD1DZyObvrPAAAAAElFTkSuQmCC"


class CBCNews(RSSBase):
    def get_id(self):
        return "cbcnews"

    def get_desc(self):
        return "CBC News"

    def get_rss_links(self):
        return [
            ("Top Stories", "http://rss.cbc.ca/lineup/topstories.xml"),
            ("World", "http://rss.cbc.ca/lineup/world.xml"),
            ("Canada", "http://rss.cbc.ca/lineup/canada.xml"),
            ("Technology & Science", "http://rss.cbc.ca/lineup/technology.xml"),
            ("Politics", "http://rss.cbc.ca/lineup/politics.xml"),
            ("Business", "http://rss.cbc.ca/lineup/business.xml"),
            ("Health", "http://rss.cbc.ca/lineup/health.xml"),
            ("Art & Entertainment", "http://rss.cbc.ca/lineup/arts.xml"),
            ("Offbeat", "http://rss.cbc.ca/lineup/offbeat.xml"),
            ("Aboriginal", "http://www.cbc.ca/cmlink/rss-cbcaboriginal"),
        ]

    def get_icon_url(self):
        return "https://rss.cbc.ca/favicon.ico"


class MingPaoToronto(BaseSource):
    def get_id(self):
        return "mingpaotoronto"

    def get_desc(self):
        return "明報加東版(多倫多)"

    def get_articles(self):
        # get date first
        date_url = "http://www.mingpaocanada.com/TOR/"
        tor_time = datetime.now(pytz.timezone("America/Toronto"))
        if tor_time.hour < 4:
            tor_time = tor_time - timedelta(days=1)
        the_date = tor_time.strftime("%Y%m%d")

        try:
            doc = html.document_fromstring(read_http_page(date_url))
            for a_link in doc.get_element_by_id("mp-menu").xpath("//div/ul/li/a"):
                if a_link.text_content() == "明報首頁":
                    href = a_link.attrib["href"]
                    match = re.match(r"htm\/News\/(\d{8})\/main_r\.htm", href)
                    if match and match.lastindex == 1:
                        the_date = match.group(1)
                    else:
                        logger.info("no date found. using system date: " + the_date)
        except Exception as e:
            logger.exception("Problem getting date: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        result_list = []
        news_url = "http://www.mingpaocanada.com/TOR/htm/News/"
        sections = [
            (
                "要聞",
                news_url + the_date + "/TAindex_r.htm",
            ),
            (
                "加國新聞",
                news_url + the_date + "/TDindex_r.htm",
            ),
            (
                "中國",
                news_url + the_date + "/TCAindex_r.htm",
            ),
            (
                "國際",
                news_url + the_date + "/TTAindex_r.htm",
            ),
            (
                "港聞",
                news_url + the_date + "/HK-GAindex_r.htm",
            ),
            (
                "經濟",
                news_url + the_date + "/THindex_r.htm",
            ),
            (
                "體育",
                news_url + the_date + "/TSindex_r.htm",
            ),
            (
                "影視",
                news_url + the_date + "/HK-MAindex_r.htm",
            ),
            (
                "副刊",
                news_url + the_date + "/WWindex_r.htm",
            ),
        ]

        base_url = news_url + the_date + "/"
        try:
            for title, url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(
                    read_http_page(url).decode("big5-hkscs", errors="ignore")
                )
                for topic in doc.xpath('//h4[contains(@class, "listing-link")]/a'):
                    if topic.text and topic.get("href"):
                        result_list.append(
                            self.create_article(
                                topic.text.strip(), base_url + topic.get("href")
                            )
                        )

        except Exception as e:
            logger.exception("Problem processing MingPaoToronto: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "https://news.mingpao.com/favicon.ico"


class TorontoStar(RSSBase):
    def get_id(self):
        return "torontostar"

    def get_desc(self):
        return "Toronto Star"

    def get_rss_links(self):
        return [
            ("Canada", "https://www.thestar.com/search/?f=rss&t=article&c=news/canada*&l=50&s=start_time&sd=desc"),
            ("World", "https://www.thestar.com/search/?f=rss&t=article&c=news/world*&l=50&s=start_time&sd=desc"),
            ("GTA", "https://www.thestar.com/search/?f=rss&t=article&c=news/gta*&l=50&s=start_time&sd=desc"),
            ("Business", "https://www.thestar.com/search/?f=rss&t=article&c=business*&l=50&s=start_time&sd=desc"),
            ("Entertainment", "https://www.thestar.com/search/?f=rss&t=article&c=entertainment*&l=50&s=start_time&sd=desc"),
        ]

    def get_icon_url(self):
        return "https://www.thestar.com/favicon.ico"


# class NationalPost(RSSBase):
#     def get_id(self):
#         return "nationalpost"

#     def get_desc(self):
#         return "National Post"

#     def get_rss_links(self):
#         return [
#             ("News", "http://news.nationalpost.com/category/news/feed"),
#             ("Comment", "http://news.nationalpost.com/category/full-comment/feed"),
#             (
#                 "Personal Finance",
#                 "http://business.financialpost.com/category/personal-finance/feed",
#             ),
#             ("Tech", "http://business.financialpost.com/category/fp-tech-desk/feed"),
#             ("Sports", "http://news.nationalpost.com/category/sports/feed"),
#             ("Arts", "http://news.nationalpost.com/category/arts/feed"),
#             ("Life", "http://news.nationalpost.com/category/life/feed"),
#             ("Health", "http://news.nationalpost.com/category/health/feed"),
#         ]


class TorontoSun(RSSBase):
    def get_id(self):
        return "torontosun"

    def get_desc(self):
        return "Toronto Sun"

    def get_rss_links(self):
        return [
            ("Toronto & GTA", "https://torontosun.com/category/news/local-news/feed"),
            ("Ontario", "https://torontosun.com/category/news/provincial/feed"),
            ("Canada", "https://torontosun.com/category/news/national/feed"),
            ("World", "https://torontosun.com/category/news/world/feed"),
            ("Business", "https://torontosun.com/category/business/feed"),
            ("Sports", "https://torontosun.com/category/sports/feed"),
            ("Entertainment", "https://torontosun.com/category/entertainment/feed"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAjVBMVEX////8/Pz09PTo7Ozg4uLv9fX3/v7y+Pjc3d397u/rqKnbbW/YSU7XQ0jcZGjnmZv43N3+8fHed3nOAADQCxbRGSLRHSXQDxrPAAjSICjSIyrTKzHUOT7vwMHrr7Dzzc7kiozooaPstbblkZPQABDxw8TZWFvjh4n4+PjllJX24eLbbG3if4Lss7XVOT9MDU8xAAABU0lEQVR4Aa3SBZbCQBAE0Jr0xD09Qgx32L3/7XB98JyK5yfj+EmEQ+SIr0SSXM/zScoPdwIvjOIkzfICkt6NqKxYaWO05aTwgzdzi4Gt67ppmrrWHHkv6lDBddo2Xd2YrutO6tMDA1hT98N+FEWjqB/GmotHqxx3bBs7nkz7fDKdzaaZMSnk/UcxsCrlObPlc/TpMrqjXHAFYFkINRSRiHiCbEXriwnasMAMoy3mUwyBJMIu8eiCa3fPI4QrDm8YThBbyDvaNt9iugX/nTDCGrG+oaCcgT22I8y2yDGe4Vks5IgnOPESQF8h5y12M1rfx0DN22VjtVr+D9qurU3HhXwMQq5qcx5YY05H3dR2CfkcvtY0r+EwEHdcy3D+ojX3Lr1OZ9iou2leePJ9jWAzmFutreK4pDcD1oEr+nGW7YelFzj4XEWSXN8lSfiateOsBX6RIwQ1HfKKG9KPAAAAAElFTkSuQmCC"

class LaPresse(RSSBase):
    def get_id(self):
        return "lapresse"

    def get_desc(self):
        return "La Presse"

    def get_rss_links(self):
        return [
            ("Actualités", "https://www.lapresse.ca/actualites/rss"),
            ("Actualités internationales", "https://www.lapresse.ca/international/rss"),
            ("Dialogue", "https://www.lapresse.ca/dialogue/rss"),
            ("Contexte", "https://www.lapresse.ca/contexte/rss"),
            ("Actualités affaires", "https://www.lapresse.ca/affaires/rss"),
            ("Actualités sports", "https://www.lapresse.ca/sports/rss"),
        ]

    def get_icon_url(self):
        return "https://www.lapresse.ca/favicon.ico"
