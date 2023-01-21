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
from lxml import html
import traceback
import json
from urllib.parse import urlparse

from logger import logger
from fetcher import read_http_page

from .base import BaseSource
from .base import RSSBase

class MingPaoHK(RSSBase):
    def get_id(self):
        return "mingpaohk"

    def get_desc(self):
        return "明報(香港)"

    def get_rss_links(self):
        return [
            ("要聞", "http://news.mingpao.com/rss/pns/s00001.xml"),
            ("港聞", "http://news.mingpao.com/rss/pns/s00002.xml"),
            ("經濟", "http://news.mingpao.com/rss/pns/s00004.xml"),
            ("娛樂", "http://news.mingpao.com/rss/pns/s00016.xml"),
            ("社評‧筆陣", "http://news.mingpao.com/rss/pns/s00003.xml"),
            ("觀點", "http://news.mingpao.com/rss/pns/s00012.xml"),
            ("國際", "http://news.mingpao.com/rss/pns/s00014.xml"),
            ("體育", "http://news.mingpao.com/rss/pns/s00015.xml"),
            ("副刊", "http://news.mingpao.com/rss/pns/s00005.xml"),
            ("深度報道", "http://news.mingpao.com/rss/pns/s00285.xml"),
            ("偵查報道", "http://news.mingpao.com/rss/pns/s00287.xml"),
        ]


class OrientalDaily(BaseSource):
    def get_id(self):
        return "orientaldaily"

    def get_desc(self):
        return "東方日報(香港)"

    def get_articles(self):
        top_url = "http://orientaldaily.on.cc"
        sections = {
            'news': {
                'title': '要聞港聞',
                'url': ''
            },
            'china_world': {
                'title': '兩岸國際',
                'url': ''
            },
            'finance': {
                'title': '產經',
                'url': ''
            },
            'entertainment': {
                'title': '娛樂',
                'url': ''
            },
            'lifestyle': {
                'title': '副刊',
                'url': ''
            },
            'sport': {
                'title': '體育',
                'url': ''
            }
        }

        try:
            doc = html.document_fromstring(read_http_page(top_url))
            if doc is not None:
                menu = doc.xpath('//*[@id="pageCTN"]/header/div[contains(@class, "middle")]/ul[contains(@class, "menuList")]')
                if menu:
                    for the_link in menu[0].xpath('li/a'):
                        the_class = the_link.xpath('@class')
                        if the_link.xpath('@href') and the_class and the_class[0] in sections:
                            sections[the_class[0]]['url'] = top_url + the_link.xpath('@href')[0]
        except Exception as e:
            logger.exception("Problem getting OrientalDaily sections: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        result_list = []
        base_url = top_url

        try:
            for _, section in sections.items():
                title = section['title']
                section_url = section['url']
                if section_url:
                    # for each section, insert a title...
                    result_list.append(self.create_section(title))
                    # ... then parse the page and extract article links
                    doc = html.document_fromstring(read_http_page(section_url))
                    if doc is not None:
                        articles = doc.xpath('//div[contains(@class, "sectionList")]/div[contains(@class, "subsection")]/ul[contains(@class, "items")]/li[@articleid]')
                        for article in articles:
                            article_urls = article.xpath('a/@href')
                            article_texts = article.xpath('a/div[contains(@class, "text")]/text()')
                            if article_urls and article_texts:
                                result_list.append(
                                    self.create_article(
                                        article_texts[0].strip(), base_url + article_urls[0]
                                    )
                                )

        except Exception as e:
            logger.exception("Problem processing OrientalDaily: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list


class SingPao(BaseSource):
    def get_id(self):
        return "singpao"

    def get_desc(self):
        return "香港成報"

    def get_articles(self):
        max_page_per_section = 10
        result_list = []

        sections = [
            ("要聞港聞", "http://www.singpao.com.hk/index.php?fi=news1"),
            ("兩岸國際", "http://www.singpao.com.hk/index.php?fi=news8"),
            ("財經", "http://www.singpao.com.hk/index.php?fi=news3"),
            ("娛樂", "http://www.singpao.com.hk/index.php?fi=news4"),
            ("體育", "http://www.singpao.com.hk/index.php?fi=news5"),
            ("副刊", "http://www.singpao.com.hk/index.php?fi=news7"),
        ]
        base_url = "http://www.singpao.com.hk/"

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                page = 1
                max_page = 1
                while page <= max_page and page <= max_page_per_section:
                    doc = html.document_fromstring(
                        read_http_page(url + "&page=" + str(page))
                    )
                    page += 1

                    for topic in doc.xpath('//td/a[contains(@class, "list_title")]'):
                        if topic.text and topic.get("href"):
                            result_list.append(
                                self.create_article(
                                    topic.text.strip(), base_url + topic.get("href")
                                )
                            )

                    for page_index in doc.xpath(
                        '//a[contains(@class, "fpagelist_css")]'
                    ):
                        if page_index.text is not None:
                            match = re.match(r"^(\d+)$", page_index.text.strip())
                            if (
                                match
                                and match.lastindex == 1
                                and int(match.group(1)) > max_page
                            ):
                                max_page = int(match.group(1))

        except Exception as e:
            logger.exception("Problem processing SingPao: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list


class HeadlineDaily(RSSBase):
    def get_id(self):
        return "stheadline"

    def get_desc(self):
        return "頭條日報"

    def get_rss_links(self):
        return [
            ("頭條日報", "http://hd.stheadline.com/rss/news/daily/"),
        ]


class TaKungPao(BaseSource):
    def get_id(self):
        return "takungpao"

    def get_desc(self):
        return "大公網"

    def get_articles(self):
        result_list = []

        sections = [
            ("港聞", "http://www.takungpao.com.hk/hongkong/"),
            ("內地", "http://www.takungpao.com.hk/mainland/"),
            ("台灣", "http://www.takungpao.com.hk/taiwan/"),
            ("國際", "http://www.takungpao.com.hk/international/"),
            ("評論", "http://www.takungpao.com.hk/opinion/"),
            ("經濟", "http://www.takungpao.com.hk/finance/"),
            ("文化", "http://www.takungpao.com.hk/culture/"),
            ("體育", "http://www.takungpao.com.hk/sports/"),
            ("娛樂", "http://www.takungpao.com.hk/ent/"),
        ]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))

                for topic in doc.xpath(
                    '//div[contains(@class, "list_tuwen")]/div[contains(@class, "content")]'
                ):
                    title = topic.xpath('ul[contains(@class, "txt")]/li[contains(@class, "title")]/a')
                    intro = topic.xpath('ul[contains(@class, "txt")]/li[contains(@class, "intro")]/a')

                    if title and title[0].text and title[0].get("href"):
                        result_list.append(
                            self.create_article(
                                title[0].text.strip(),
                                title[0].get("href"),
                                intro[0].text.strip() if intro and intro[0].text else None,
                            )
                        )

        except Exception as e:
            logger.exception("Problem processing TaKungPao: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list


class Scmp(RSSBase):
    def get_id(self):
        return "scmp"

    def get_desc(self):
        return "South China Morning Post"

    def get_rss_links(self):
        return [
            ("News", "https://www.scmp.com/rss/91/feed"),
            ("Business", "https://www.scmp.com/rss/92/feed"),
            ("Tech", "https://www.scmp.com/rss/36/feed"),
            ("Life", "https://www.scmp.com/rss/94/feed"),
            ("Culture", "https://www.scmp.com/rss/322296/feed"),
            ("Sport", "https://www.scmp.com/rss/95/feed"),
        ]


class Etnet(RSSBase):
    def get_id(self):
        return "etnet"

    def get_desc(self):
        return "經濟通"

    def get_rss_links(self):
        return [
            ("精選新聞", "http://www.etnet.com.hk/www/tc/news/rss.php?section=editor"),
            ("焦點專題", "http://www.etnet.com.hk/www/tc/news/rss.php?section=special"),
            ("股市傳聞 	", "http://www.etnet.com.hk/www/tc/news/rss.php?section=rumour"),
            ("股票評論", "http://www.etnet.com.hk/www/tc/news/rss.php?section=commentary"),
        ]


class HkEt(BaseSource):
    def _is_absolute(self, url):
        return bool(urlparse(url).netloc)

    def get_id(self):
        return "hket"

    def get_desc(self):
        return "香港經濟日報"

    def get_articles(self):
        result_list = []
        sections = [
            ("金融經濟", "https://inews.hket.com", "/sran009/金融經濟", 3),
            ("理財", "https://wealth.hket.com", "/", 1),
            ("科技", "https://inews.hket.com", "/sran010/科技", 2),
            ("中國", "https://china.hket.com", "/", 1),
            ("國際", "https://inews.hket.com", "/sran011/國際", 2),
            ("商業", "https://inews.hket.com", "/sran012/商業", 2),
        ]
        seen_url = {}

        try:
            for (title, base_url, url, pages) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then get page and parse
                for page in range(1, pages + 1):
                    doc = html.document_fromstring(
                        read_http_page(base_url + url + "?p={}".format(page))
                    )
                    for topic in doc.xpath(
                        '//div[contains(@class, "listing-widget-33") or contains(@class, "listing-widget-4") or contains(@class, "listing-widget-9")]/a[contains(@class, "listing-overlay")]'
                    ):
                        if topic.text and topic.get("href"):
                            topic_url = (
                                topic.get("href")
                                if self._is_absolute(topic.get("href"))
                                else base_url + topic.get("href")
                            )
                            if topic_url not in seen_url:
                                seen_url[topic_url] = None
                                result_list.append(
                                    self.create_article(topic.text.strip(), topic_url)
                                )

        except Exception as e:
            logger.exception("Problem processing HkEt: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list

class CitizenNewss(BaseSource):
    def get_id(self):
        return "hkcnews"

    def get_desc(self):
        return "眾新聞 CitizenNews"

    def get_articles(self):
        result_list = []
        sections = [
            ("眾聞", "https://www.hkcnews.com", "https://www.hkcnews.com/data/newsposts", 3),
        ]

        try:
            for (title, base_url, data_url, pages) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then get page and parse
                for page in range(1, pages + 1):
                    raw_result = read_http_page(data_url + "?page={}".format(page))
                    result = json.loads(raw_result)
                    for item in result['items']:
                        doc = html.document_fromstring(item)
                        for article in doc.xpath('//div[contains(@class, "article-block")]'):
                            article_link = article.xpath('div[contains(@class, "article-block-body")]/a')
                            article_text = article.xpath('div[contains(@class, "article-block-body")]/a/p')
                            if article_link and article_text:
                                url = base_url + article_link[0].get("href")
                                text = article_text[0].text
                                if url and text:
                                    footer = article.xpath('a[contains(@class, "article-block-footer")]')
                                    date_str = ''
                                    if footer:
                                        divs = footer[0].xpath('div/div[contains(@class, "text-box")]/div')
                                        for div in divs:
                                            if div.text and re.match(r"\d{2}\.\d{2}\.\d{2}", div.text.strip()):
                                                date_str = div.text.strip()
                                    result_list.append(
                                        self.create_article(text.strip() + ' - {}'.format(date_str), url)
                                    )

        except Exception as e:
            logger.exception("Problem processing CitizenNewss: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list


class HKFP(RSSBase):
    def get_id(self):
        return "hkfp"

    def get_desc(self):
        return "Hong Kong Free Press"

    def get_rss_links(self):
        return [
            ("Hong Kong Free Press", "https://www.hongkongfp.com/feed/"),
        ]

class HKEJ(BaseSource):
    def get_id(self):
        return "hkej"

    def get_desc(self):
        return "信報財經"

    def get_articles(self):
        result_list = []
        root_url = "https://www1.hkej.com"
        sections = [
            ("要聞", "/dailynews"),
            ("理財投資", "/dailynews/investment"),
            ("時事評論", "/dailynews/commentary"),
            ("財經新聞", "/dailynews/finnews"),
            ("地產市道", "/dailynews/property"),
            ("政壇脈搏", "/dailynews/politics"),
            ("獨眼", "/dailynews/views"),
            ("兩岸消息", "/dailynews/cntw"),
            ("EJ Global", "/dailynews/international"),
            ("副刊文化", "/dailynews/culture"),
        ]
        try:
            for (title, base_url) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then get page and parse
                doc = html.document_fromstring(
                    read_http_page(root_url + base_url)
                )
                for article in doc.xpath(
                    '//div[contains(@class, "more-articles-dd-wrapper")]/form/select/option'
                ):
                    if article.get("value") and article.text:
                        article_url = root_url + article.get("value")
                        result_list.append(
                            self.create_article(article.text.strip(), article_url)
                        )
        except Exception as e:
            logger.exception("Problem processing HKEJ: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list

class AM730(BaseSource):
    def get_id(self):
        return "am730"

    def get_desc(self):
        return "AM730"

    def get_articles(self):
        result_list = []
        root_url = "https://www.am730.com.hk"
        sections = [
            ("本地", "/本地", 5),
            ("國際", "/國際", 3),
            ("娛樂", "/娛樂", 3),
            ("中國", "/中國", 2),
            ("財經", "/財經", 2),
            ("地產", "/地產", 2),
            ("體育", "/體育", 2),
            ("專欄", "/column", 5),
        ]
        try:
            for (title, base_url, num_pages) in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                for page in range(1, num_pages+1):
                    # ... then get page and parse
                    resp = json.loads(read_http_page(root_url + base_url,
                        method="POST",
                        headers = { "Accept": "application/json",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "X-Requested-With": "XMLHttpRequest" },
                        body = "page={}".format(page)))

                    for article in resp["data"]["data"]:
                        article_title = article["title"]
                        article_url = article["url"]
                        if article_title and article_url:
                            result_list.append(
                                self.create_article(article_title.strip(), root_url + article_url)
                            )
        except Exception as e:
            logger.exception("Problem processing AM730: " + str(e))
            logger.exception(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )

        return result_list