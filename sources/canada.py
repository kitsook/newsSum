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


class VancouverSun(RSSBase):
    def get_id(self):
        return "vancouversun"

    def get_desc(self):
        return "Vancouver Sun"

    def get_rss_links(self):
        return [
            ("Vancouver News, Top Stories", "https://vancouversun.com/feed"),
        ]


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
