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

    def get_icon_url(self):
        return "https://www.bbc.com/favicon.ico"


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

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAnCAMAAAC7faEHAAAAtFBMVEX80bP90bT80bT90bP80rT90rT70bP80LL70rT80LP80rL/17b80bb/2bn/3r/90bFsYVr/3LkIFyL/3sGnkIDLsJv/4cDqxKrtx6n/48LTr5YXIir/2LynjoB0aGJ8bWaId21hWVdoXlcABxe2monWtJ5WUU4ABxIPGB8pKzE1OD3cuKCwmIYAAACTgnQDER48PDlOSUW+n4j/7sgaICp5b2GKfG4uNDYeJyxHRUTYu6HGqZZ/BmS/AAADkklEQVQ4jT1Ui0LiOhQ8OcnJq2njorYiXRRXfIALu16vr/v//3XnFDSU0obJnEcmQykkjOBjzj5TzTXkipEzeX1IgaLnGCmEgGfmTPjk4L3XW/DZ10qhhioUORcKRCH7EiMAGaQx4sILBnkOZB3YXCFhZlIcALlwPAzvmQtzKrhKYSrkIsvYdV2Lb396etq1ObZd3/cdnrtT3E/HyBG4GH8ul1dXy+XJNK4uxuvV6ubkOHdzc3PWOsXlPKxXv/Yvt+v1+vbu/mEYH+9Xz+vzza/7q+366e33SYd6JUdq5pez2cZr5PluAdyu79r5zX7/1Ld9vznpgUN1PjeXi9nmokEK7fA2xD9DG3N7t5+d/ch5vlvNlc87tkdcjiWOf4fhzjUxN3ezCdc9r+boOupwcsQ1cWzH3cVw1kRbv3DN9mebveYXv+M2w2UTtQNs7BdOTDI2E1NMFbiHTe37f3bLHqxR2NpmNeGcGGOsEGFfCbiXx9d/d2eP133jdOu45gOfY+DIELbRhgPu9fV6cT1vxCFr85UfK84U8EWe+DZ5Pte4SMgm+sYJl5IS+IAzWscb+jKiDkuYdiYd4wqAnBjKgx6+cFEazBtI6LteBxCEDLZS6IhDK2NxurKw4h6Ai06Fpzho+YgDEAgz4XjCtc7hsSDupMrm8mXiw5zWB1wxrfavUzbmgP5xFOmf97P3bQc+dqJxzdjSx2x/NY6ijMGS816eTjYv74s/qx32kK1xXMbb1cfiffH+sdoKSgUOJ8t9nn9+Dtv1f+vGkUl6YmQ4/xww1ucXgmUhkZ7Upm3HcWzbVhyBzhqx05TDXTThkHF+Sc+systZMSQihvUScWKtsaitBqwPCXN56o8jshASFII+W4gGDdbdDcivVkkG8RyDCpogkEFHpuInTThsBqyhVjYZOMQQ6xw8QGySLDkjqEk2mcShZrKVAEC8ZK0WAT36hEWYTJZTCNjthDpAiUlrCHuYLBJD51mlZRhNC/hH2IMvG6upTjYDPTmGMlEOJIx69GOR4JQfck3IH33Eky7S9BPDKNgZrT1JDVRhfzBAJIheIDicTO2QwKyyEwRhqegLGh3AQlA2qWfWilckCnkGjWNgbgFxE/J1GgYk6sEHPgcVxpSwVuuaFuCYsPojs/eJYZC4IKZ4kB5Ohx4kdIs98cFHObL67dFTFTQJHPJ1KBNG7zNMSwdeISDGj0543GKZHPl/uYhFT4hjXHMAAAAASUVORK5CYII="


class DeutscheWelle(RDFBase):
    def get_id(self):
        return "dw"

    def get_desc(self):
        return "德國之聲"

    def get_rss_links(self):
        return [
            ("德國之聲", "http://rss.dw.com/rdf/rss-chi-all"),
        ]

    def get_icon_url(self):
        return "https://rss.dw.com/favicon.ico"


class WSJChinese(RSSBase):
    def get_id(self):
        return "wsjcn"

    def get_desc(self):
        return "華爾街日報"

    def get_rss_links(self):
        return [
            ("華爾街日報", "https://cn.wsj.com/zh-hant/rss"),
        ]

    def get_icon_url(self):
        return "https://www.wsj.com/favicon.ico"


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

    def get_icon_url(self):
        return "https://apnews.com/favicon.ico"


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
            (
                "Reuters Agency",
                "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"
            ),
        ]

    def get_icon_url(self):
        return "https://www.reuters.com/favicon.ico"

class CNBC(RSSBase):
    def get_id(self):
        return "cnbc"

    def get_desc(self):
        return "CNBC"

    def get_rss_links(self):
        return [
            (
                "Top News",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
            ),
            (
                "World News",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362",
            ),
            (
                "US News",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362",
            ),
            (
                "Asia News",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19832390",
            ),
            (
                "Europe News",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19794221",
            ),
            (
                "Business",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147",
            ),
            (
                "Earnings",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135",
            ),
            (
                "Commentary",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100370673",
            ),
            (
                "Economy",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
            ),
            (
                "Finance",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
            ),
            (
                "Technology",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
            ),
            (
                "Politics",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113",
            ),
            (
                "Health Care",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000108",
            ),
            (
                "Real Estate",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000115",
            ),
            (
                "Wealth",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001054",
            ),
            (
                "Autos",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000101",
            ),
            (
                "Energy",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19836768",
            ),
            (
                "Media",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000110",
            ),
            (
                "Retail",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000116",
            ),
            (
                "Travel",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000739",
            ),
            (
                "Small Business",
                "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=44877279",
            ),
        ]

    def get_icon_url(self):
        return "https://www.cnbc.com/favicon.ico"

class TheWashingtonTimes(RSSBase):
    def get_id(self):
        return "washingtontimes"

    def get_desc(self):
        return "The Washington Times"

    def get_rss_links(self):
        return [
            (
                "News",
                "https://www.washingtontimes.com/rss/headlines/news/",
            ),
        ]

    def get_icon_url(self):
        return "https://www.washingtontimes.com/favicon.ico"

class WashingtonPost(RSSBase):
    def get_id(self):
        return "washingtonpost"

    def get_desc(self):
        return "Washington Post"

    def get_rss_links(self):
        return [
            (
                "Local",
                "https://feeds.washingtonpost.com/rss/local",
            ),
            (
                "National",
                "http://feeds.washingtonpost.com/rss/national",
            ),
            (
                "World",
                "https://feeds.washingtonpost.com/rss/world",
            ),
            (
                "Politics",
                "https://www.washingtonpost.com/arcio/rss/category/politics/",
            ),
            (
                "Opinions",
                "https://www.washingtonpost.com/arcio/rss/category/opinions/",
            ),
            (
                "Business",
                "http://feeds.washingtonpost.com/rss/business",
            ),
            (
                "Lifestyle",
                "https://feeds.washingtonpost.com/rss/lifestyle",
            ),
            (
                "Entertainment",
                "http://feeds.washingtonpost.com/rss/entertainment",
            ),
            (
                "Technology",
                "https://feeds.washingtonpost.com/rss/business/technology",
            ),
            (
                "Sport",
                "https://feeds.washingtonpost.com/rss/sports"
            )
        ]

    def get_icon_url(self):
        return "https://www.washingtonpost.com/favicon.ico"

class Npr(RSSBase):
    def get_id(self):
        return "npr"

    def get_desc(self):
        return "NPR"

    def get_rss_links(self):
        return [
            (
                "News",
                "https://feeds.npr.org/1001/rss.xml",
            ),
            (
                "World",
                "https://feeds.npr.org/1004/rss.xml",
            ),
            (
                "Business",
                "https://feeds.npr.org/1006/rss.xml",
            ),
            (
                "Science",
                "https://feeds.npr.org/1007/rss.xml",
            ),
            (
                "Economy",
                "https://feeds.npr.org/1017/rss.xml",
            ),
            (
                "Technology",
                "https://feeds.npr.org/1019/rss.xml",
            ),
        ]

    def get_icon_url(self):
        return "https://www.npr.org/favicon.ico"

class SeattleTimes(RSSBase):
    def get_id(self):
        return "seattletimes"

    def get_desc(self):
        return "Seattle Times"

    def get_rss_links(self):
        return [
            ("Seattle News", "https://www.seattletimes.com/seattle-news/feed/"),
            ("Nation and World", "https://www.seattletimes.com/nation-world/feed/"),
            ("Business", "https://www.seattletimes.com/business/feed/"),
            ("Sports", "https://www.seattletimes.com/sports/feed/"),
            ("Entertainment", "https://www.seattletimes.com/entertainment/feed/"),
            ("Life", "https://www.seattletimes.com/life/feed/"),
            ("Opinion", "https://www.seattletimes.com/opinion/feed/"),
            ("Photo and Video", "https://www.seattletimes.com/photo-video/feed"),
        ]

    def get_icon_url(self):
        return "data:image/webp;base64,UklGRloDAABXRUJQVlA4WAoAAAAQAAAAGgAAGgAAQUxQSAECAAARkC1Jtmlb3WvtY9u2ce+jbdu2bdu2bdu2bdv22nM8bNz7CRExAbCXBEiCIPHPhCVBEqQNkgRhm6ANhlRoUtJHg00SluEAHFq9UmJcaeCe2mJQ9yrpHhoB0nU8YOp2ft9LJfJ773OzKOPTqZmNsgP8c2fVAatvCzBF9Pss8uPp0y+GiIj6+uDhhxEmBN1YbgL0ah9P5nh5JtQYsvezElFP2zuBncw/2roCeovKoFvTZi75ToxZNrlSAAG/FSJ/VqdqcHSGz+JN7tU/qSoDCoEgywz7KyJPm7kSbss/59VWi6o0sCBAokCH7X+UyJ91CVoHY6+TvlVUxUEFAZCO7fuOe65E5EHjuzIE2kp74NRwcqtlX0Xkt1LNwYmiKg4uYAFASxs1qvtZQ0RUC6K/qIqDCoIgAcKx4Ixei36LyAiis5hLDC4EWOgJ2Z6ad4tei/6K7HTSh/1Z5zewEEDC1OzFl7NNPRzy9bgn8jqxxIrarhhYEABR+ouIGHsynDKOKTHPKONPYGAhUAN2KrMSkVctow89VPKtrg6gfyEWiwHWdK7fe9c3EePl2LgrIt/6B2jsW7bKVD/AldTcK1+VvyOckbj3t5jvLR5zZG9nfwIgCMZcmedEwLPy/LN3b+/onKDDTqb5wpK6i6eHg0ZYEiABAiQIS5IgaAWWJGxbI/4zAQAAVlA4IDIBAAAQBgCdASobABsAPpEepFIloSWlmACwEgljAKkUikmqN4FvkKsQ7N9D9FNqt7qtgF7rmqXNFCs06+AA/rn+auW9Kg7fCIlgcmrRMsrktsdRdkOGldcirAeSZPMDrSgVGeD81MfSSRa731mt5JVXIjXiFlSHvzrdvVrf0lnZUbWWqHe55M78sbeF3Tv6jKhW3BV4He0KSoh96yOPhCpEZ5ZCUyJ/VBx6FtEifhrBimjHyGcobzegJ8+z/g7K/KVDsOfySBO3AMj6EoCJQLE4teUD3phX1wF6vkjnYUGIZP0edd3ozhLo5RLtQVswF4TMlwGIxu23LYtr/f4FVB/UgDEGJe8rUtg03kvK5GjGbMi3Wb2grdlevv4OWow7StRJW89mFi6Bdd5RSJT9orwuR2QAAAA="

class SFGate(RSSBase):
    def get_id(self):
        return "sfgate"

    def get_desc(self):
        return "SFGate"

    def get_rss_links(self):
        return [
            ("Bay Area News", "https://www.sfgate.com/bayarea/feed/bay-area-news-429.php"),
            ("Business and Technology News", "https://www.sfgate.com/rss/feed/business-and-technology-news-448.php"),
            ("Entertainment", "https://www.sfgate.com/rss/feed/culture-530.php"),
            ("Food & Dining", "https://www.sfgate.com/rss/feed/food-dining-550.php"),
            ("Top Sports Stories", "https://www.sfgate.com/rss/feed/top-sports-stories-rss-feed-487.php"),
        ]

    def get_icon_url(self):
        return "https://www.sfgate.com/favicon.ico"

