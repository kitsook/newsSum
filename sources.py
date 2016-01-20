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

class BaseSource():

    def create_section(self, title):
        return {'title': title}

    def create_article(self, title, url, abstract=None):
        return {'title': title, 'url': url, 'abstract': abstract}

class RSSBase(BaseSource):

    def get_rss_links(self):
        return [];

    def get_articles(self):
        resultList = []
        for (title, url) in self.get_rss_links():
            try:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = etree.fromstring(read_http_page(url))
                for entry in doc.xpath('//rss/channel/item'):
                    title = entry.xpath('title')[0].text
                    link = entry.xpath('link')[0].text
                    abstract = entry.xpath('description')[0].text
                    resultList.append(self.create_article(title.strip(), link, abstract))
            except Exception as e:
                logger.exception('Problem processing rss')
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
        return [('News Home Page', 'http://rss.canada.com/get/?F229'),
                ('Regional', 'http://rss.canada.com/get/?F259'),
                ('National', 'http://rss.canada.com/get/?F7431'),
                ('World', 'http://rss.canada.com/get/?F7432'),]

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

class BBCWorld(RSSBase):

    def get_id(self):
        return 'bbcworld'

    def get_desc(self):
        return 'BBC World'

    def get_rss_links(self):
        return [('World', 'http://feeds.bbci.co.uk/news/world/rss.xml'),
                ('Asia', 'http://feeds.bbci.co.uk/news/world/asia/rss.xml'),]

class FTChinese(RSSBase):
        def get_id(self):
            return 'ftchinese'

        def get_desc(self):
            return 'FT中文网'

        def get_rss_links(self):
            return [('今日焦点', 'http://big5.ftchinese.com/rss/news'),]

class AppleDaily(BaseSource):

    def get_id(self):
            return 'appledaily'

    def get_desc(self):
        return '蘋果日報(香港)'

    def get_articles(self):
        resultList = []
        sections = [('要聞港聞', 'http://hk.apple.nextmedia.com/news/index/'),
                    ('兩岸國際', 'http://hk.apple.nextmedia.com/international/index/'),
                    ('財經地產', 'http://hk.apple.nextmedia.com/financeestate/index/'),
                    ('娛樂名人', 'http://hk.apple.nextmedia.com/entertainment/index/'),
                    ('果籽', 'http://hk.apple.nextmedia.com/supplement/index/'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for option in doc.get_element_by_id('article_ddl').xpath('//option'):
                    if option.text and option.get('value'):
                        resultList.append(self.create_article(option.text.strip(), option.get('value')))

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
        sections = [('要聞', 'http://vancouver.singtao.ca/category/%E8%A6%81%E8%81%9E/?variant=zh-hk'),
                    ('省市', 'http://vancouver.singtao.ca/category/%E7%9C%81%E5%B8%82/?variant=zh-hk'),
                    ('加國', 'http://vancouver.singtao.ca/category/%e5%8a%a0%e5%9c%8b/?variant=zh-hk'),
                    ('社區', 'http://vancouver.singtao.ca/category/%e7%a4%be%e5%8d%80/?variant=zh-hk'),
                    ('國際', 'http://vancouver.singtao.ca/category/%e5%9c%8b%e9%9a%9b/?variant=zh-hk'),
                    ('港聞', 'http://vancouver.singtao.ca/category/%e6%b8%af%e8%81%9e/?variant=zh-hk'),
                    ('中國', 'http://vancouver.singtao.ca/category/%e4%b8%ad%e5%9c%8b/?variant=zh-hk'),
                    ('台灣', 'http://vancouver.singtao.ca/category/%e5%8f%b0%e7%81%a3/?variant=zh-hk'),
                    ('體育', 'http://vancouver.singtao.ca/category/%e9%ab%94%e8%82%b2/?variant=zh-hk'),
                    ('財經', 'http://vancouver.singtao.ca/category/%e8%b2%a1%e7%b6%93/?variant=zh-hk'),
                    ('娛樂', 'http://vancouver.singtao.ca/category/%e5%a8%9b%e6%a8%82/?variant=zh-hk'),
                    ('社論', 'http://vancouver.singtao.ca/category/%e7%a4%be%e8%ab%96/?variant=zh-hk'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for option in doc.get_element_by_id('news').xpath('option'):
                    if option.text and option.get('value'):
                        resultList.append(self.create_article(option.text.strip(), option.get('value')))


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
        sections = [('要聞', 'http://toronto.singtao.ca/category/%e8%a6%81%e8%81%9e/?variant=zh-hk'),
                    ('城市', 'http://toronto.singtao.ca/category/%e5%9f%8e%e5%b8%82/?variant=zh-hk'),
                    ('加國', 'http://toronto.singtao.ca/category/%e5%8a%a0%e5%9c%8b/?variant=zh-hk'),
                    ('國際', 'http://toronto.singtao.ca/category/%e5%9c%8b%e9%9a%9b/?variant=zh-hk'),
                    ('港聞', 'http://toronto.singtao.ca/category/%e6%b8%af%e8%81%9e/?variant=zh-hk'),
                    ('中國', 'http://toronto.singtao.ca/category/%e4%b8%ad%e5%9c%8b/?variant=zh-hk'),
                    ('台灣', 'http://toronto.singtao.ca/category/%e5%8f%b0%e7%81%a3/?variant=zh-hk'),
                    ('體育', 'http://toronto.singtao.ca/category/%e9%ab%94%e8%82%b2/?variant=zh-hk'),
                    ('財經', 'http://toronto.singtao.ca/category/%e8%b2%a1%e7%b6%93/?variant=zh-hk'),
                    ('娛樂', 'http://toronto.singtao.ca/category/%e5%a8%9b%e6%a8%82/?variant=zh-hk'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for option in doc.get_element_by_id('news').xpath('option'):
                    if option.text and option.get('value'):
                        resultList.append(self.create_article(option.text.strip(), option.get('value')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

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

class MingPaoHK(RSSBase):

    def get_id(self):
        return 'mingpaohk'

    def get_desc(self):
        return '明報(香港)'

    def get_rss_links(self):
        return [('要聞','http://news.mingpao.com/rss/pns/s00001.xml'),
                ('港聞','http://news.mingpao.com/rss/pns/s00002.xml'),
                ('經濟','http://news.mingpao.com/rss/pns/s00004.xml'),
                ('娛樂','http://news.mingpao.com/rss/pns/s00016.xml'),
                ('社評‧筆陣','http://news.mingpao.com/rss/pns/s00003.xml'),
                ('觀點','http://news.mingpao.com/rss/pns/s00012.xml'),
                ('國際','http://news.mingpao.com/rss/pns/s00014.xml'),
                ('體育','http://news.mingpao.com/rss/pns/s00015.xml'),
                ('副刊','http://news.mingpao.com/rss/pns/s00005.xml'),
                ('深度報道','http://news.mingpao.com/rss/pns/s00285.xml'),
                ('偵查報道','http://news.mingpao.com/rss/pns/s00287.xml'),]

class OrientalDailyRSS(RSSBase):

    def get_id(self):
        return 'orientaldailyrss'

    def get_desc(self):
        return '東方日報RSS(香港)'

    def get_rss_links(self):
        return [('要聞港聞','http://orientaldaily.on.cc/rss/news.xml'),
                ('兩岸國際','http://orientaldaily.on.cc/rss/china_world.xml'),
                ('財經','http://orientaldaily.on.cc/rss/finance.xml'),
                ('娛樂','http://orientaldaily.on.cc/rss/entertainment.xml'),
                ('副刊','http://orientaldaily.on.cc/rss/lifestyle.xml'),]

class OrientalDaily(BaseSource):

    def get_id(self):
        return 'orientaldaily'

    def get_desc(self):
        return '東方日報(香港)'

    def get_articles(self):
        # get date first
        dateUrl = 'http://orientaldaily.on.cc/'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(read_http_page(dateUrl))
            for aLink in doc.get_element_by_id('topMenu').xpath('//ul[contains(@class, "menuList clear")]/li/a[contains(@class, "news")]'):
                href = aLink.attrib['href']
                match = re.match('\/cnt\/news\/([0-9]{8})\/index\.html', href)
                if match and match.lastindex == 1:
                    theDate = match.group(1)
                else:
                    logger.info('no date found. using system date: ' + theDate)
        except Exception as e:
            logger.exception('Problem getting date')

        resultList = []
        baseUrl = dateUrl

        sections = [('要聞港聞','http://orientaldaily.on.cc/cnt/news/' + theDate + '/index.html'),
                    ('兩岸國際','http://orientaldaily.on.cc/cnt/china_world/' + theDate + '/index.html'),
                    ('財經','http://orientaldaily.on.cc/cnt/finance/' + theDate + '/index.html'),
                    ('娛樂','http://orientaldaily.on.cc/cnt/entertainment/' + theDate + '/index.html'),
                    ('副刊','http://orientaldaily.on.cc/cnt/lifestyle/' + theDate + '/index.html'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.get_element_by_id('articleList').xpath('//ul[contains(@class, "commonBigList")]/li/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), baseUrl+topic.get('href')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class MetroHK(RSSBase):

    def get_id(self):
        return 'metrohk'

    def get_desc(self):
        return '香港都市日報 (Metro Daily)'

    def get_rss_links(self):
        return [('香港都市日報','http://www.metrohk.com.hk/desktopRSS.php'),]

class SingPao(BaseSource):

    def get_id(self):
        return 'singpao'

    def get_desc(self):
        return '香港成報'

    def get_articles(self):
        resultList = []
        sections = [('成報新聞', 'http://www.singpao.com/index.php/spnews/sphknews'),
                    ('成報社評', 'http://www.singpao.com/index.php/spcpnews'),
                    ('成報財經', 'http://www.singpao.com/index.php/spfinance'),
                    ('成報娛樂', 'http://www.singpao.com/index.php/spent'),
                    ('成報體育', 'http://www.singpao.com/index.php/spsport'),
                    ('成報副刊', 'http://www.singpao.com/index.php/spmagazine'),]
        baseUrl = 'http://www.singpao.com'

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.get_element_by_id('jsn-pos-mainbody-top').xpath('//a[contains(@class, "title")]'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), baseUrl+topic.get('href')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class AM730(BaseSource):

    def get_id(self):
        return 'am730'

    def get_desc(self):
        return 'AM730'

    def get_articles(self):
        resultList = []
        # build the list
        listUrl = 'http://www.am730.com.hk/home'
        baseUrl = 'http://www.am730.com.hk/'
        try:
            doc = html.document_fromstring(read_http_page(listUrl))
            for optGroup in doc.get_element_by_id('listnews').xpath('optgroup'):
                if optGroup.get('label'):
                    resultList.append(self.create_section(optGroup.get('label')))
                for opt in optGroup.xpath('option'):
                    if opt.get('value') and opt.text:
                        resultList.append(self.create_article(opt.text.strip(), baseUrl+opt.get('value')))
        except Exception as e:
            logger.exception('Problem getting date')

        return resultList
