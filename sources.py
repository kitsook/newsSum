# -*- coding: utf-8 -*-
import re
import datetime
from lxml import html
from lxml import etree

from logger import logger
from fetcher import readHttpPage

class BaseSource:

    def createSection(self, title):
        return {'title': title}

    def createArticle(self, title, url, abstract=None):
        return {'title': title, 'url': url, 'abstract': abstract}

    def parseRSS(self, sections):
        resultList = []
        for (title, url) in sections:
            # for each section, insert a title...
            resultList.append(self.createSection(title))
            # ... then parse the page and extract article links
            doc = etree.fromstring(readHttpPage(url))
            for entry in doc.xpath('//rss/channel/item'):
                title = entry.xpath('title')[0].text
                link = entry.xpath('link')[0].text
                abstract = entry.xpath('description')[0].text
                resultList.append(self.createArticle(title.strip(), link, abstract))
        return resultList


class TheProvince(BaseSource):

    def getId(self):
        return 'theprovince'

    def getDesc(self):
        return 'The Province'

    def getArticles(self):
        resultList = []
        sections = [('Vancouver', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|metro%20vancouver'),
                    ('Fraser Valley', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|fraser%20valley'),
                    ('B.C.', 'http://www.theprovince.com/scripts/Sp6Query.aspx?catalog=VAPR&tags=category|news|subcategory|b.c.'),]
        relSections = [('Canada', 'http://www.theprovince.com/7588609.atom'),
                    ('World', 'http://www.theprovince.com/7589147.atom'), ]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = etree.fromstring(readHttpPage(url))
                for entry in doc.xpath('//ns:entry[@Status="FREE"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'}):
                    title = entry.xpath('ns:title[@type="html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].text
                    link = 'http://www.theprovince.com' + entry.xpath('ns:link[@type="text/html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('href')
                    abstract = entry.xpath('ns:link[@type="text/html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('Abstract')
                    resultList.append(self.createArticle(title.strip(), link, abstract))

            for (title, url) in relSections:
                # for each section, insert a title...
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = etree.fromstring(readHttpPage(url))
                for entry in doc.xpath('//ns:entry[@Status="FREE"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'}):
                    title = entry.xpath('ns:title[@type="html"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].text
                    link = 'http://www.theprovince.com' + entry.xpath('ns:link[@type="text/xml"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('href')
                    abstract = entry.xpath('ns:link[@type="text/xml"]', namespaces={'ns': 'http://www.w3.org/2005/Atom'})[0].get('Abstract')
                    resultList.append(self.createArticle(title.strip(), link, abstract))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class VancouverSun(BaseSource):

    def getId(self):
        return 'vancouversun'

    def getDesc(self):
        return 'Vancouver Sun'

    def getArticles(self):
        resultList = []
        sections = [('News Home Page', 'http://rss.canada.com/get/?F229'),
                    ('Regional', 'http://rss.canada.com/get/?F259'),
                    ('National', 'http://rss.canada.com/get/?F7431'),
                    ('World', 'http://rss.canada.com/get/?F7432'),]

        try:
            resultList = self.parseRSS(sections)
        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class BBCWorld(BaseSource):

    def getId(self):
        return 'bbcworld'

    def getDesc(self):
        return 'BBC World'

    def getArticles(self):
        resultList = []
        sections = [('World', 'http://feeds.bbci.co.uk/news/world/rss.xml'),
                    ('Asia', 'http://feeds.bbci.co.uk/news/world/asia/rss.xml'),]

        try:
            resultList = self.parseRSS(sections)
        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class AppleDaily(BaseSource):

    def getId(self):
            return 'appledaily'

    def getDesc(self):
        return '蘋果日報(香港)'

    def getArticles(self):
        resultList = []
        sections = [('要聞港聞', 'http://hk.apple.nextmedia.com/news/index/'),
                    ('兩岸國際', 'http://hk.apple.nextmedia.com/international/index/'),
                    ('財經地產', 'http://hk.apple.nextmedia.com/financeestate/index/'),
                    ('娛樂名人', 'http://hk.apple.nextmedia.com/entertainment/index/'),
                    ('果籽', 'http://hk.apple.nextmedia.com/supplement/index/'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(readHttpPage(url))
                for option in doc.get_element_by_id('article_ddl').xpath('//option'):
                    if option.text and option.get('value'):
                        resultList.append(self.createArticle(option.text.strip(), option.get('value')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class SingTaoVancouver(BaseSource):

    def getId(self):
        return 'singtaovancouver'

    def getDesc(self):
        return '星島日報(溫哥華)'

    def getArticles(self):
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
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(readHttpPage(url))
                for option in doc.get_element_by_id('news').xpath('//option'):
                    if option.text and option.get('value'):
                        resultList.append(self.createArticle(option.text.strip(), option.get('value')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class SingTaoToronto(BaseSource):

    def getId(self):
        return 'singtaotoronto'

    def getDesc(self):
        return '星島日報(多倫多)'

    def getArticles(self):
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
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(readHttpPage(url))
                for option in doc.get_element_by_id('news').xpath('//option'):
                    if option.text and option.get('value'):
                        resultList.append(self.createArticle(option.text.strip(), option.get('value')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class MingPaoVancouver(BaseSource):

    def getId(self):
        return 'mingpaovancouver'

    def getDesc(self):
        return '明報加西版(溫哥華)'

    def getArticles(self):
        # get date first
        dateUrl = 'http://www.mingpaocanada.com/Van/'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(readHttpPage(dateUrl))
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
        sections = [('要聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VAindex.htm'),
                    ('加國新聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VBindex.htm'),
                    ('社區新聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VDindex.htm'),
                    ('港聞','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/HK-VGindex.htm'),
                    ('國際','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VTindex.htm'),
                    ('中國','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VCindex.htm'),
                    ('體育','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/VSindex.htm'),
                    ('影視','http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/HK-MAindex.htm'),]

        baseUrl = 'http://www.mingpaocanada.com/Van/htm/News/' + theDate + '/'
        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(readHttpPage(url))
                for topic in doc.xpath('//a[contains(@class, "ListContentLargeLink") or contains(@class, "ListContentSmallLink")]'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.createArticle(topic.text.strip(), baseUrl+topic.get('href')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class MingPaoHK(BaseSource):

    def getId(self):
        return 'mingpaohk'

    def getDesc(self):
        return '明報(香港)'

    def getArticles(self):
        resultList = []
        sections = [('要聞','http://news.mingpao.com/rss/pns/s00001.xml'),
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

        try:
            resultList = self.parseRSS(sections)
        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class OrientalDaily(BaseSource):

    def getId(self):
        return 'orientaldaily'

    def getDesc(self):
        return '東方日報(香港)'

    def getArticles(self):
        # get date first
        dateUrl = 'http://orientaldaily.on.cc/'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(readHttpPage(dateUrl))
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
                resultList.append(self.createSection(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(readHttpPage(url))
                for topic in doc.get_element_by_id('articleList').xpath('//ul[contains(@class, "commonBigList")]/li/a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.createArticle(topic.text.strip(), baseUrl+topic.get('href')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList
