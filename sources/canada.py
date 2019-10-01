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
import datetime
from lxml import html
from lxml import etree

from logger import logger
from fetcher import read_http_page

from base import BaseSource
from base import RSSBase

class MingPaoVancouver(BaseSource):

    def get_id(self):
        return 'mingpaovancouver'

    def get_desc(self):
        return '明報加西版(溫哥華)'

    def get_articles(self):
        # get date first
        dateUrl = 'http://www.mingpaocanada.com/Van/'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(read_http_page(dateUrl))
            for aLink in doc.get_element_by_id('mp-menu').xpath('//div/ul/li/a'):
                if aLink.text_content().encode('utf-8') == '明報首頁':
                    href = aLink.attrib['href']
                    match = re.match('htm\/News\/([0-9]{8})\/main_r\.htm', href)
                    if match and match.lastindex == 1:
                        theDate = match.group(1)
                    else:
                        logger.info('no date found. using system date: ' + theDate)
        except Exception as e:
            logger.exception('Problem getting date')

        resultList = []
        sections = [('要聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VAindex_r.htm'),
                    ('加國新聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VBindex_r.htm'),
                    ('社區新聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VDindex_r.htm'),
                    ('港聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/HK-VGindex_r.htm'),
                    ('國際','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VTindex_r.htm'),
                    ('中國','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VCindex_r.htm'),
                    ('經濟','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VEindex_r.htm'),
                    ('體育','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VSindex_r.htm'),
                    ('影視','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/HK-MAindex_r.htm'),
                    ('副刊','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/WWindex_r.htm'),]

        baseUrl = 'http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/'
        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(unicode(read_http_page(url), 'big5', errors='ignore'))
                for topic in doc.xpath('//h4[contains(@class, "listing-link")]/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), baseUrl+topic.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class SingTaoVancouver(BaseSource):
    def get_id(self):
        return 'singtaovancouver'

    def get_desc(self):
        return '星島日報(溫哥華)'

    def get_articles(self):
        resultList = []
        sections = [('要聞','https://www.singtao.ca/category/52-%E6%BA%AB%E5%93%A5%E8%8F%AF%E8%A6%81%E8%81%9E/?variant=zh-hk'),
                    ('加國新聞','https://www.singtao.ca/category/54-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%8A%A0%E5%9C%8B/?variant=zh-hk'),
                    ('省市', 'https://www.singtao.ca/category/65-%E6%BA%AB%E5%93%A5%E8%8F%AF%E7%9C%81%E5%B8%82/?variant=zh-hk'),
                    ('社區新聞','https://www.singtao.ca/category/55-%E6%BA%AB%E5%93%A5%E8%8F%AF%E7%A4%BE%E5%8D%80/?variant=zh-hk'),
                    ('港聞','https://www.singtao.ca/category/57-%E6%BA%AB%E5%93%A5%E8%8F%AF%E6%B8%AF%E8%81%9E/?variant=zh-hk'),
                    ('國際','https://www.singtao.ca/category/56-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%9C%8B%E9%9A%9B/?variant=zh-hk'),
                    ('中國','https://www.singtao.ca/category/58-%E6%BA%AB%E5%93%A5%E8%8F%AF%E4%B8%AD%E5%9C%8B/?variant=zh-hk'),
                    ('台灣','https://www.singtao.ca/category/59-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%8F%B0%E7%81%A3/?variant=zh-hk'),
                    ('財經','https://www.singtao.ca/category/61-%E6%BA%AB%E5%93%A5%E8%8F%AF%E8%B2%A1%E7%B6%93/?variant=zh-hk'),
                    ('體育','https://www.singtao.ca/category/60-%E6%BA%AB%E5%93%A5%E8%8F%AF%E9%AB%94%E8%82%B2/?variant=zh-hk'),
                    ('娛樂','https://www.singtao.ca/category/62-%E6%BA%AB%E5%93%A5%E8%8F%AF%E5%A8%9B%E6%A8%82/?variant=zh-hk'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url, {'edition': 'vancouver'}).decode('utf-8'))

                # top story
                top_story_link = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a')
                top_story_text = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a/div/h3')
                if top_story_link and top_story_text:
                    resultList.append(self.create_article(top_story_text[0].text.strip(), top_story_link[0].get('href')))

                for topic in doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[contains(@class, "td-animation-stack")]/div[@class="item-details"]/h3/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), topic.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class SingTaoToronto(BaseSource):
    def get_id(self):
        return 'singtaotoronto'

    def get_desc(self):
        return '星島日報(多倫多)'

    def get_articles(self):
        resultList = []
        sections = [('要聞','https://www.singtao.ca/category/52-%E5%A4%9A%E5%80%AB%E5%A4%9A%E8%A6%81%E8%81%9E/?variant=zh-hk'),
                    ('加國新聞','https://www.singtao.ca/category/54-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%8A%A0%E5%9C%8B/?variant=zh-hk'),
                    ('城市', 'https://www.singtao.ca/category/53-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%9F%8E%E5%B8%82/?variant=zh-hk'),
                    ('港聞','https://www.singtao.ca/category/57-%E5%A4%9A%E5%80%AB%E5%A4%9A%E6%B8%AF%E8%81%9E/?variant=zh-hk'),
                    ('國際','https://www.singtao.ca/category/56-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%9C%8B%E9%9A%9B/?variant=zh-hk'),
                    ('中國','https://www.singtao.ca/category/58-%E5%A4%9A%E5%80%AB%E5%A4%9A%E4%B8%AD%E5%9C%8B/?variant=zh-hk'),
                    ('台灣','https://www.singtao.ca/category/59-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%8F%B0%E7%81%A3/?variant=zh-hk'),
                    ('財經','https://www.singtao.ca/category/61-%E5%A4%9A%E5%80%AB%E5%A4%9A%E8%B2%A1%E7%B6%93/?variant=zh-hk'),
                    ('體育','https://www.singtao.ca/category/60-%E5%A4%9A%E5%80%AB%E5%A4%9A%E9%AB%94%E8%82%B2/?variant=zh-hk'),
                    ('娛樂','https://www.singtao.ca/category/62-%E5%A4%9A%E5%80%AB%E5%A4%9A%E5%A8%9B%E6%A8%82/?variant=zh-hk'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url, {'edition': 'toronto'}).decode('utf-8'))

                # top story
                top_story_link = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a')
                top_story_text = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a/div/h3')
                if top_story_link and top_story_text:
                    resultList.append(self.create_article(top_story_text[0].text.strip(), top_story_link[0].get('href')))

                for topic in doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[contains(@class, "td-animation-stack")]/div[@class="item-details"]/h3/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), topic.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class SingTaoCalgary(BaseSource):
    def get_id(self):
        return 'singtaocalgary'

    def get_desc(self):
        return '星島日報(卡加利)'

    def get_articles(self):
        resultList = []
        sections = [('要聞','https://www.singtao.ca/category/52-%E5%8D%A1%E5%8A%A0%E5%88%A9%E8%A6%81%E8%81%9E/?variant=zh-hk'),
                    ('加國新聞','https://www.singtao.ca/category/54-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%8A%A0%E5%9C%8B/?variant=zh-hk'),
                    ('省市', 'https://www.singtao.ca/category/65-%E5%8D%A1%E5%8A%A0%E5%88%A9%E7%9C%81%E5%B8%82/?variant=zh-hk'),
                    ('港聞','https://www.singtao.ca/category/57-%E5%8D%A1%E5%8A%A0%E5%88%A9%E6%B8%AF%E8%81%9E/?variant=zh-hk'),
                    ('國際','https://www.singtao.ca/category/56-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%9C%8B%E9%9A%9B/?variant=zh-hk'),
                    ('中國','https://www.singtao.ca/category/58-%E5%8D%A1%E5%8A%A0%E5%88%A9%E4%B8%AD%E5%9C%8B/?variant=zh-hk'),
                    ('台灣','https://www.singtao.ca/category/59-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%8F%B0%E7%81%A3/?variant=zh-hk'),
                    ('財經','https://www.singtao.ca/category/61-%E5%8D%A1%E5%8A%A0%E5%88%A9%E8%B2%A1%E7%B6%93/?variant=zh-hk'),
                    ('體育','https://www.singtao.ca/category/60-%E5%8D%A1%E5%8A%A0%E5%88%A9%E9%AB%94%E8%82%B2/?variant=zh-hk'),
                    ('娛樂','https://www.singtao.ca/category/62-%E5%8D%A1%E5%8A%A0%E5%88%A9%E5%A8%9B%E6%A8%82/?variant=zh-hk'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url, {'edition': 'calgary'}).decode('utf-8'))

                # top story
                top_story_link = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a')
                top_story_text = doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[@class="cat-header-image"]/a/div/h3')
                if top_story_link and top_story_text:
                    resultList.append(self.create_article(top_story_text[0].text.strip(), top_story_link[0].get('href')))

                for topic in doc.xpath('(//div[@class="td-ss-main-content"])[1]/div[contains(@class, "td-animation-stack")]/div[@class="item-details"]/h3/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), topic.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class TheProvince(BaseSource):

    def get_id(self):
        return 'theprovince'

    def get_desc(self):
        return 'The Province'

    def get_articles(self):
        resultList = []
        sections = [('Vancouver', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|metro%20vancouver'),
                    ('Fraser Valley', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|fraser%20valley'),
                    ('B.C.', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|b.c.'),]
        relSections = [('Canada', 'http://www.theprovince.com/7588609.atom'),
                    ('World', 'http://www.theprovince.com/7589147.atom'), ]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = etree.fromstring(read_http_page(url))
                for entry in doc.xpath('//ns:entry[@Status="FREE"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'}):
                    title = entry.xpath('ns:title[@type="html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].text
                    link = 'http://www.theprovince.com' + entry.xpath('ns:link[@type="text/html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('href')
                    abstract = entry.xpath('ns:link[@type="text/html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('Abstract')
                    resultList.append(self.create_article(title.strip(), link, abstract))

            for (title, url) in relSections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = etree.fromstring(read_http_page(url))
                for entry in doc.xpath('//ns:entry[@Status="FREE"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'}):
                    title = entry.xpath('ns:title[@type="html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].text
                    link = 'http://www.theprovince.com' + entry.xpath('ns:link[@type="text/xml"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('href')
                    abstract = entry.xpath('ns:link[@type="text/xml"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('Abstract')
                    resultList.append(self.create_article(title.strip(), link, abstract))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class VancouverSun(RSSBase):

    def get_id(self):
        return 'vancouversun'

    def get_desc(self):
        return 'Vancouver Sun'

    def get_rss_links(self):
        return [('Vancouver News, Top Stories', 'https://vancouversun.com/feed'),]

class CBCNews(RSSBase):
    def get_id(self):
        return 'cbcnews'

    def get_desc(self):
        return 'CBC News'

    def get_rss_links(self):
        return [('Top Stories', 'http://rss.cbc.ca/lineup/topstories.xml'),
                ('World', 'http://rss.cbc.ca/lineup/world.xml'),
                ('Canada', 'http://rss.cbc.ca/lineup/canada.xml'),
                ('Technology & Science', 'http://rss.cbc.ca/lineup/technology.xml'),
                ('Politics', 'http://rss.cbc.ca/lineup/politics.xml'),
                ('Business', 'http://rss.cbc.ca/lineup/business.xml'),
                ('Health', 'http://rss.cbc.ca/lineup/health.xml'),
                ('Art & Entertainment', 'http://rss.cbc.ca/lineup/arts.xml'),
                ('Offbeat', 'http://rss.cbc.ca/lineup/offbeat.xml'),
                ('Aboriginal', 'http://www.cbc.ca/cmlink/rss-cbcaboriginal'),]

class MingPaoToronto(BaseSource):

    def get_id(self):
        return 'mingpaotoronto'

    def get_desc(self):
        return '明報加東版(多倫多)'

    def get_articles(self):
        # get date first
        dateUrl = 'http://www.mingpaocanada.com/TOR/'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(read_http_page(dateUrl))
            for aLink in doc.get_element_by_id('mp-menu').xpath('//div/ul/li/a'):
                if aLink.text_content().encode('utf-8') == '明報首頁':
                    href = aLink.attrib['href']
                    match = re.match('htm\/News\/([0-9]{8})\/main_r\.htm', href)
                    if match and match.lastindex == 1:
                        theDate = match.group(1)
                    else:
                        logger.info('no date found. using system date: ' + theDate)
        except Exception as e:
            logger.exception('Problem getting date')

        resultList = []
        sections = [('要聞','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TAindex_r.htm'),
                    ('加國新聞','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TDindex_r.htm'),
                    ('地產','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TRindex_r.htm'),
                    ('中國','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TCAindex_r.htm'),
                    ('國際','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TTAindex_r.htm'),
                    ('港聞','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/HK-GAindex_r.htm'),
                    ('經濟','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/THindex_r.htm'),
                    ('體育','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/TSindex_r.htm'),
                    ('影視','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/HK-MAindex_r.htm'),
                    ('副刊','http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/WWindex_r.htm'),]


        baseUrl = 'http://www.mingpaocanada.com/TOR/htm/News/' + theDate + '/'
        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(unicode(read_http_page(url), 'big5', errors='ignore'))
                for topic in doc.xpath('//h4[contains(@class, "listing-link")]/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), baseUrl+topic.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class TorontoStar(RSSBase):

    def get_id(self):
        return 'torontostar'

    def get_desc(self):
        return 'Toronto Star'

    def get_rss_links(self):
        return [('News','http://www.thestar.com/feeds.articles.news.rss'),
                ('Your Toronto','http://www.thestar.com/feeds.articles.yourtoronto.rss'),
                ('Opinion','http://www.thestar.com/feeds.articles.opinion.rss'),
                ('Sports','http://www.thestar.com/feeds.articles.sports.rss'),
                ('Business','http://www.thestar.com/feeds.articles.business.rss'),
                ('Entertainment','http://www.thestar.com/feeds.articles.entertainment.rss'),
                ('Life','http://www.thestar.com/feeds.articles.life.rss'),
                ('Autos', 'http://www.thestar.com/feeds.articles.autos.rss'),]

class NationalPost(RSSBase):

    def get_id(self):
        return 'nationalpost'

    def get_desc(self):
        return 'National Post'

    def get_rss_links(self):
        return [('News','http://news.nationalpost.com/category/news/feed'),
                ('Comment','http://news.nationalpost.com/category/full-comment/feed'),
                ('Personal Finance','http://business.financialpost.com/category/personal-finance/feed'),
                ('Tech','http://business.financialpost.com/category/fp-tech-desk/feed'),
                ('Sports','http://news.nationalpost.com/category/sports/feed'),
                ('Arts','http://news.nationalpost.com/category/arts/feed'),
                ('Life','http://news.nationalpost.com/category/life/feed'),
                ('Health','http://news.nationalpost.com/category/health/feed'),]
