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

from lxml import html

from fetcher import read_http_page
from logger import logger

from .base import BaseSource, RDFBase, RSSBase


class LibertyTimes(BaseSource):
    def get_id(self):
        return "libertytimes"

    def get_desc(self):
        return "自由時報"

    def get_articles(self):
        num_pages = 2
        base_url = "https://news.ltn.com.tw"

        result_list = []
        sections = [
            ("熱門", base_url + "/ajax/breakingnews/popular/"),
            ("政治", base_url + "/ajax/breakingnews/politics/"),
            ("社會", base_url + "/ajax/breakingnews/society/"),
            ("地方", base_url + "/ajax/breakingnews/local/"),
            ("生活", base_url + "/ajax/breakingnews/life/"),
            ("國際", base_url + "/ajax/breakingnews/world/"),
        ]

        try:
            for page in range(1, num_pages):
                for title, url in sections:
                    url = url + str(page)
                    # for each section, insert a title...
                    result_list.append(self.create_section(title))
                    # ... then parse the page and extract article links
                    result = json.loads(read_http_page(url + str(page)).decode("UTF-8"))
                    if result.get("code", 0) == 200:
                        data = result.get("data", [])
                        for key in data.keys():
                            title = data[key].get("title", None)
                            url = data[key].get("url", None)
                            abstract = data[key].get("summary", None)
                            if title and url:
                                result_list.append(
                                    self.create_article(title, url, abstract)
                                )

        except Exception as e:
            logger.exception("Problem processing LibertyTimes: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAVCAMAAABi3H5uAAAAmVBMVEWkAgKnAgKuAgKxAgK0AgK3AgK5AgK7AgK9AgK+AgK/AgK4AgLBAgLEAgKlAgLKAACvAgLLAADFJyfLPDzNFBTTQ0PTPDzQJyfKMjLjpqb////ZYGD89vbhmZnjkJDVVFTyzs767+/NAADOAAD019fvxcXnoKD13NzsuLj56enTKyvUMzPkk5Prr6/hhYXUS0v23NzZbm7OGhrX+W8fAAABQElEQVR4AWzR1ZaEMAwAUJxSYENHcBtscPv/j9u065LXe+KSJMmKomq6YRKLYljENHRNVRRZ4iaj2SahjivCocS0UWXUF2HEEgQg2CLvKiueppuYhsIwhFOia57CUUW7XF243X3/HgQ+QHihpq4iYqJNaBS7LInjOM3yuHDLiIrCEk+0nOwBVc2yBqr8kbpt5liYKpA4LmJd192zqvN+6PrMdYhAzf6J7Ri3iFhXkTzNQOyGmz8JnEvWxRwNzeNoYWaaxkvVNTyzZgOiJVBkAlQV1q1qEQDvmW89oWD1WyR17cNF9PTep80zrNiv1bI+C2i2Xkz7sWefzJO/t6yMlnEeju5jT4/XzdaO9Q3iUlbnfizXtwvJInU7Fki2oqrOHqa8D0Oe+PMr8P4Vh39F4D//pB//fB1mSuCBpwS8aQgAzxklGzuYV2oAAAAASUVORK5CYII="


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

    def get_icon_url(self):
        return "https://udn.com/favicon.ico"


class MoneyUnitedDailyNewsRSS(RSSBase):
    def get_id(self):
        return "money-udn"

    def get_desc(self):
        return "經濟日報-聯合新聞網"

    def get_articles(self):
        site_base_url = "https://money.udn.com"
        base_url = site_base_url + "/money/cate/"

        result_list = []
        sections = [
            ("要聞", base_url + "10846"),
            ("國際", base_url + "5588"),
            ("兩岸", base_url + "5589"),
            ("產業", base_url + "5591"),
            ("證券", base_url + "5590"),
            ("金融", base_url + "12017"),
            ("期貨", base_url + "11111"),
            ("理財", base_url + "5592"),
            ("房市", base_url + "5593"),
            ("專欄", base_url + "5595"),
            ("商情", base_url + "5597"),
        ]

        try:
            for title, url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.xpath(
                    '//section[contains(@class, "cate-main__section")]/div[contains(@class, "story-headline-wrapper")]'
                ):
                    # main stories first...
                    link = topic.xpath('div[contains(@class, "story__content")]/a')
                    title = topic.xpath('div[contains(@class, "story__content")]/a/h3')
                    intro = topic.xpath('div[contains(@class, "story__content")]/a/p')
                    title_text = title[0].text if title else None

                    if title and title_text and link:
                        result_list.append(
                            self.create_article(
                                title_text.strip(),
                                site_base_url + link[0].get("href"),
                                intro[0].text.strip()
                                if intro and intro[0].text
                                else None,
                            )
                        )

                for topic in doc.xpath(
                    '//section[contains(@class, "cate-main__section")]/ul[contains(@class, "story-flex-bt-wrapper")]'
                ):
                    # ... then other stories
                    titles = topic.xpath('li[contains(@class, "story__item")]/a')
                    for title in titles:
                        title_text = title.text
                        if title_text:
                            result_list.append(
                                self.create_article(
                                    title_text.strip(),
                                    site_base_url + title.get("href"),
                                    None,
                                )
                            )

        except Exception as e:
            logger.exception("Problem processing MoneyUnitedDailyNewsRSS: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "https://money.udn.com/favicon.ico"


class TaipeiTimes(RDFBase):
    def get_id(self):
        return "taipeitimes"

    def get_desc(self):
        return "Taipei Times(臺北時報)"

    def get_rss_links(self):
        return [
            ("Taipei Times", "https://www.taipeitimes.com/xml/index.rss"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAk1BMVEX////8/Pzq6ury8vLv7+/4+Pj19fXZ2dnDwsKnpqaGhIXNzMzHxsazsrNBPj+ioaF2dHVIRUZsaWplY2SFhIWTkpK5uLmcm5zj4+PEw8OPjo6trKxaV1hfXV3w3N3dt7jp0tLNlJXOjI6jHB+sNDfGenu1bW6/cXOnOTqwQUS6dnenKS20UFK0WlrCbW/ft7jNm5ySIOF/AAAA/klEQVR4AbWRA6JFIRQA51x06lXPtq39b+7b5uQmx/8hSZpmuQhixKQpV+mqxi1qXcGHEEmLuJIrlW00lZR7vANXhRo2UG9kUOWpNM1W+0p2XFO7rRJVeSpj7HVvZ1LI5JksUYC+DLBNqCe51Hig09Me2NjIbYSSc0kj4xsMR1eM35GT6Wy+WL4jp6v1ZrV9b+Z6N9+/K8eH4/C9ZU+H1epw5htkzRCs+lxSyCT1HcVH4Za2CSXRAe0GdBMGolbb5tmXldG+SF+pQqjDC2mj9S4wiJFeX17IUl5vao8qQIwPstmACnUKPilTaQebRH2QSZtUM01zRI16TW2b/+MSqy0PJ4pdskwAAAAASUVORK5CYII="


class ChinaTimes(BaseSource):
    def get_id(self):
        return "chinatimes"

    def get_desc(self):
        return "中國時報"

    def get_articles(self):
        result_list = []
        base_url = "https://www.chinatimes.com"

        sections = [
            ("政治", base_url + "/politic/?chdtv"),
            ("言論", base_url + "/opinion/?chdtv"),
            ("生活", base_url + "/life/?chdtv"),
            ("娛樂", base_url + "/star/?chdtv"),
            ("財經", base_url + "/money/?chdtv"),
            ("社會", base_url + "/society/?chdtv"),
            ("話題", base_url + "/hottopic/?chdtv"),
            ("國際", base_url + "/world/?chdtv"),
            ("軍事", base_url + "/armament/?chdtv"),
            ("兩岸", base_url + "/chinese/?chdtv"),
            ("時尚", base_url + "/fashion/?chdtv"),
            ("體育", base_url + "/sports/?chdtv"),
            ("科技", base_url + "/technologynews/?chdtv"),
            ("玩食", base_url + "/travel/?chdtv"),
            ("新聞專輯", base_url + "/album/?chdtv"),
        ]

        try:
            for title, url in sections:
                # for each section, insert a title...
                result_list.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.xpath(
                    '//section[contains(@class, "article-list")]/ul//li//h3[contains(@class, "title")]//a'
                ):
                    if topic.text and topic.get("href"):
                        result_list.append(
                            self.create_article(topic.text.strip(), topic.get("href"))
                        )

        except Exception as e:
            logger.exception("Problem processing ChinaTimes: " + str(e))
            logger.exception(
                traceback.format_exception(e)
            )

        return result_list

    def get_icon_url(self):
        return "https://www.chinatimes.com/favicon.ico"


class Storm(RSSBase):
    def get_id(self):
        return "storm"

    def get_desc(self):
        return "風傳媒"

    def get_rss_links(self):
        return [
            ("新聞", "https://www.storm.mg/api/getRss/channel_id/2?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("國內", "https://www.storm.mg/api/getRss/channel_id/9?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("國際", "https://www.storm.mg/api/getRss/channel_id/10?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("兩岸", "https://www.storm.mg/api/getRss/channel_id/11?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("財經", "https://www.storm.mg/api/getRss/channel_id/4?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("風生活", "https://www.storm.mg/api/getRss/channel_id/5?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("政治", "https://www.storm.mg/api/getRss/channel_id/8?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("藝文", "https://www.storm.mg/api/getRss/channel_id/17?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("娛樂", "https://www.storm.mg/api/getRss/channel_id/62?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("旅遊", "https://www.storm.mg/api/getRss/channel_id/69?path=https%3A%2F%2Fwww.storm.mg/article"),
            ("新新聞", "https://www.storm.mg/api/getRss/channel_id/109?path=https%3A%2F%2Fwww.storm.mg/article"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAh1BMVEX/////6en/xcX//Pz/ycn/qKj/g4P/VFT/AAD/PT3/c3P/HBz/JSX/Kir/ERH/jY3/ODj/MjL/0dH/8vL/mpr/lpb6+vrr6+v/UFD/KSn1///AwL+gn555eHc1My//XFzR1tYrKCQdGhT/uLg7OTZZWFXNzs0MBQAoJiFsa2m4t7aurazj4+O+JNzhAAAAfklEQVR4AdXJxQHEMBAEwTEzM1t0nH98579WAbie3bg7y3bI7Hp+EEYWdHGSpFmWF6AkZVlWqQtKnZZlGjQgtVmZdLj0AzRjNtXzsm771muvCQ+cjDG+QCc6rFwyNYDQzIpJvoL0YPu+nyANT/l696B9GP/CZJM/mCfMHNzfH/zYCFXy5W+PAAAAAElFTkSuQmCC"
