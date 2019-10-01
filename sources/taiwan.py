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

import datetime
from lxml import html
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from logger import logger
from fetcher import read_http_page

from base import BaseSource
from base import RSSBase
from base import RDFBase

class LibertyTimes(BaseSource):

    def get_id(self):
        return 'libertytimes'

    def get_desc(self):
        return '自由時報'

    def get_articles(self):
        # get date first
        baseUrl = 'http://news.ltn.com.tw'
        theDate = datetime.datetime.today().strftime('%Y%m%d')
        try:
            doc = html.document_fromstring(read_http_page(baseUrl + '/list/newspaper'))
            cal =  doc.get_element_by_id('newspaperdate')
            theDate = cal.attrib['title']
        except Exception as e:
            logger.exception('Problem getting date')

        resultList = []
        sections = [('焦點', baseUrl + '/list/newspaper/focus/' + theDate),
                    ('政治', baseUrl + '/list/newspaper/politics/' + theDate),
                    ('社會', baseUrl + '/list/newspaper/society/' + theDate),
                    ('地方', baseUrl + '/list/newspaper/local/' + theDate),
                    ('生活', baseUrl + '/list/newspaper/life/' + theDate),
                    ('言論', baseUrl + '/list/newspaper/opinion/' + theDate),
                    ('國際', baseUrl + '/list/newspaper/world/' + theDate),
                    ('財經', baseUrl + '/list/newspaper/business/' + theDate),
                    ('體育', baseUrl + '/list/newspaper/sports/' + theDate),
                    ('娛樂', baseUrl + '/list/newspaper/entertainment/' + theDate),
                    ('消費', baseUrl + '/list/newspaper/consumer/' + theDate),
                    ('副刊', baseUrl + '/list/newspaper/supplement/' + theDate),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                curPage = 1
                maxPage = 1
                while curPage <= maxPage:
                    # ... then parse the page and extract article links
                    # the encoding of libertytimes is messed up... forcing utf-8 when reading
                    doc = html.document_fromstring(read_http_page(url + '?page=' + str(curPage)).decode('utf-8'))
                    for link in doc.xpath('//div[contains(@class, "whitecon")]//a[contains(@class, "tit")]'):
                        if link.xpath('p') and link.get('href'):
                            resultList.append(self.create_article(link.xpath('p')[0].text.strip(), baseUrl + '/' + link.get('href')))
                    curPage += 1
                    for pageNum in doc.xpath('//*[contains(@class, "p_num")]'):
                        maxPage = int(pageNum.text.strip())


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class UnitedDailyNewsRSS(RSSBase):

    def get_id(self):
        return 'udn'

    def get_desc(self):
        return '聯合新聞網'

    def get_rss_links(self):
        return [('要聞','http://udn.com/rssfeed/news/2/6638?ch=news'),
                ('全球','http://udn.com/rssfeed/news/2/7225?ch=news'),
                ('兩岸','http://udn.com/rssfeed/news/2/6640?ch=news'),
                ('地方','http://udn.com/rssfeed/news/2/6641?ch=news'),
                ('評論','http://udn.com/rssfeed/news/2/6643?ch=news'),
                ('產經','http://udn.com/rssfeed/news/2/6644?ch=news'),
                ('股市','http://udn.com/rssfeed/news/2/6645?ch=news'),
                ('娛樂','http://udn.com/rssfeed/news/2/6648?ch=news'),
                ('運動','http://udn.com/rssfeed/news/2/7227?ch=news'),
                ('社會','http://udn.com/rssfeed/news/2/6639?ch=news'),
                ('生活','http://udn.com/rssfeed/news/2/6649?ch=news'),
                ('數位','http://udn.com/rssfeed/news/2/7226?ch=news'),]

class MoneyUnitedDailyNewsRSS(RSSBase):

    @staticmethod
    def is_url(url):
      try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
      except ValueError:
        return False

    def get_id(self):
        return 'money-udn'

    def get_desc(self):
        return '經濟日報-聯合新聞網'

    def get_rss_links(self):
        resultList = []
        try:
            rss_list_url = 'https://money.udn.com/rssfeed/lists/1001';
            doc = html.document_fromstring(read_http_page(rss_list_url).decode('utf-8'))
            for aLink in doc.get_element_by_id("rss_list").xpath('div/div/dl/dt/a'):
                if aLink.xpath('text()') and MoneyUnitedDailyNewsRSS.is_url(aLink.get('href')):
                    resultList.append((aLink.xpath('text()'), aLink.get('href')))
        except Exception as e:
            logger.exception('Problem fetching rss links')

        return resultList

class AppleDailyTaiwan(BaseSource):

    def get_id(self):
        return 'appledailytw'

    def get_desc(self):
        return '蘋果日報(台灣)'

    def get_articles(self):
        # get article lists
        summary_url = 'https://tw.appledaily.com/daily'
        doc = html.document_fromstring(read_http_page(summary_url))

        resultList = []
        sections = [('頭條', u'//article[contains(@class, "nclns")]//h2[contains(text(), "頭條")]/following-sibling::ul/li/a'),
                    ('要聞', u'//article[contains(@class, "nclns")]//h2[contains(text(), "要聞")]/following-sibling::ul/li/a'),
                    ('政治', u'//article[contains(@class, "nclns")]//h2[contains(text(), "政治")]/following-sibling::ul/li/a'),
                    ('社會', u'//article[contains(@class, "nclns")]//h2[contains(text(), "社會")]/following-sibling::ul/li/a'),
                    ('蘋果爆破社', u'//article[contains(@class, "nclns")]//h2[contains(text(), "蘋果爆破社")]/following-sibling::ul/li/a'),
                    ('蘋論陣線', u'//article[contains(@class, "nclns")]//h2[contains(text(), "蘋論陣線")]/following-sibling::ul/li/a'),
                    ('暖流', u'//article[contains(@class, "nclns")]//h2[contains(text(), "暖流")]/following-sibling::ul/li/a'),
                    ('娛樂名人', u'//article[contains(@class, "nclns")]//h2[contains(text(), "娛樂名人")]/following-sibling::ul/li/a'),
                    ('木瓜霞吐槽', u'//article[contains(@class, "nclns")]//h2[contains(text(), "木瓜霞吐槽")]/following-sibling::ul/li/a'),
                    ('直擊好萊塢', u'//article[contains(@class, "nclns")]//h2[contains(text(), "直擊好萊塢")]/following-sibling::ul/li/a'),
                    ('亞洲哈燒星', u'//article[contains(@class, "nclns")]//h2[contains(text(), "亞洲哈燒星")]/following-sibling::ul/li/a'),
                    ('名人時尚', u'//article[contains(@class, "nclns")]//h2[contains(text(), "名人時尚")]/following-sibling::ul/li/a'),
                    ('國際頭條', u'//article[contains(@class, "nclns")]//h2[contains(text(), "國際頭條")]/following-sibling::ul/li/a'),
                    ('國際新聞', u'//article[contains(@class, "nclns")]//h2[contains(text(), "國際新聞")]/following-sibling::ul/li/a'),
                    ('雙語天下', u'//article[contains(@class, "nclns")]//h2[contains(text(), "雙語天下")]/following-sibling::ul/li/a'),
                    ('體育焦點', u'//article[contains(@class, "nclns")]//h2[contains(text(), "體育焦點")]/following-sibling::ul/li/a'),
                    ('大運動場', u'//article[contains(@class, "nclns")]//h2[contains(text(), "大運動場")]/following-sibling::ul/li/a'),
                    ('籃球瘋', u'//article[contains(@class, "nclns")]//h2[contains(text(), "籃球瘋")]/following-sibling::ul/li/a'),
                    ('投打對決', u'//article[contains(@class, "nclns")]//h2[contains(text(), "投打對決")]/following-sibling::ul/li/a'),
                    ('足球新聞', u'//article[contains(@class, "nclns")]//h2[contains(text(), "足球新聞")]/following-sibling::ul/li/a'),
                    ('運彩分析', u'//article[contains(@class, "nclns")]//h2[contains(text(), "運彩分析")]/following-sibling::ul/li/a'),
                    ('財經焦點', u'//article[contains(@class, "nclns")]//h2[contains(text(), "財經焦點")]/following-sibling::ul/li/a'),
                    ('頭家人生', u'//article[contains(@class, "nclns")]//h2[contains(text(), "頭家人生")]/following-sibling::ul/li/a'),
                    ('投資理財', u'//article[contains(@class, "nclns")]//h2[contains(text(), "投資理財")]/following-sibling::ul/li/a'),
                    ('卡該這樣刷', u'//article[contains(@class, "nclns")]//h2[contains(text(), "卡該這樣刷")]/following-sibling::ul/li/a'),
                    ('地產焦點', u'//article[contains(@class, "nclns")]//h2[contains(text(), "地產焦點")]/following-sibling::ul/li/a'),
                    ('副刊焦點', u'//article[contains(@class, "nclns")]//h2[contains(text(), "副刊焦點")]/following-sibling::ul/li/a'),
                    ('美食天地', u'//article[contains(@class, "nclns")]//h2[contains(text(), "美食天地")]/following-sibling::ul/li/a'),
                    ('車市3C', u'//article[contains(@class, "nclns")]//h2[contains(text(), "車市3C")]/following-sibling::ul/li/a'),
                    ('家庭與健康', u'//article[contains(@class, "nclns")]//h2[contains(text(), "家庭與健康")]/following-sibling::ul/li/a'),
                    ]

        try:
            for (title, path) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                for link in doc.xpath(path):
                    if link.get('title') and link.get('href'):
                        resultList.append(self.create_article(link.get('title').strip(), link.get('href')))

        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class TaipeiTimes(RDFBase):

    def get_id(self):
        return 'taipeitimes'

    def get_desc(self):
        return 'Taipei Times(臺北時報)'

    def get_rss_links(self):
        return [('Front Page', 'http://www.taipeitimes.com/xml/front.rss'),
                ('Taiwan News','http://www.taipeitimes.com/xml/taiwan.rss'),
                ('World News','http://www.taipeitimes.com/xml/world.rss'),
                ('Business','http://www.taipeitimes.com/xml/biz.rss'),
                ('Sports','http://www.taipeitimes.com/xml/sport.rss'),
                ('Features','http://www.taipeitimes.com/xml/feat.rss'),]

class ChinaTimes(BaseSource):

    def get_id(self):
        return 'chinatimes'

    def get_desc(self):
        return '中國時報'

    def get_articles(self):
        resultList = []
        baseUrl = 'https://www.chinatimes.com'

        sections = [('政治', baseUrl + '/politic/?chdtv'),
                    ('言論', baseUrl + '/opinion/?chdtv'),
                    ('生活', baseUrl + '/life/?chdtv'),
                    ('娛樂', baseUrl + '/star/?chdtv'),
                    ('財經', baseUrl + '/money/?chdtv'),
                    ('社會', baseUrl + '/society/?chdtv'),
                    ('話題', baseUrl + '/hottopic/?chdtv'),
                    ('國際', baseUrl + '/world/?chdtv'),
                    ('軍事', baseUrl + '/armament/?chdtv'),
                    ('兩岸', baseUrl + '/chinese/?chdtv'),
                    ('時尚', baseUrl + '/fashion/?chdtv'),
                    ('體育', baseUrl + '/sports/?chdtv'),
                    ('科技', baseUrl + '/technologynews/?chdtv'),
                    ('玩食', baseUrl + '/travel/?chdtv'),
                    ('新聞專輯', baseUrl + '/album/?chdtv'),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                # ... then parse the page and extract article links
                doc = html.document_fromstring(read_http_page(url))
                for topic in doc.xpath('//section[contains(@class, "article-list")]/ul//li//h3[contains(@class, "title")]//a'):
                    if topic.text and topic.get('href'):
                        resultList.append(self.create_article(topic.text.strip(), topic.get('href')))


        except Exception as e:
            logger.exception('Problem processing url')

        return resultList

class CommercialTimes(RSSBase):

    def get_id(self):
        return 'commercialtimes'

    def get_desc(self):
        return '工商時報'

    def get_rss_links(self):
        return [('財經要聞', 'https://ctee.com.tw/feed'),]
