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
                            resultList.append(self.create_article(link.xpath('p')[0].text.strip(), baseUrl + link.get('href')))
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

class AppleDailyTaiwan(RSSBase):

    def get_id(self):
        return 'appledailytw'

    def get_desc(self):
        return '蘋果日報(台灣)'

    def get_rss_links(self):
        return [('要聞','https://tw.appledaily.com/rss/newcreate/kind/sec/type/5'),
                ('國際','https://tw.appledaily.com/rss/newcreate/kind/sec/type/7'),
                ('娛樂','https://tw.appledaily.com/rss/newcreate/kind/sec/type/9'),
                ('體育','https://tw.appledaily.com/rss/create/kind/sec/type/10'),
                ('財經','https://tw.appledaily.com/rss/create/kind/sec/type/8'),
                ('房市地產','https://tw.appledaily.com/rss/newcreate/kind/sec/type/31488836'),
                ('論壇與專欄','https://tw.appledaily.com/rss/newcreate/kind/sec/type/forum'),
                ('副刊','https://tw.appledaily.com/rss/create/kind/sec/type/17'),
                ('旅遊與美食總','https://tw.appledaily.com/rss/create/kind/sec/type/ALL24'),
                ('家庭與健康','https://tw.appledaily.com/rss/create/kind/sec/type/19'),
                ('科技3C','https://tw.appledaily.com/rss/create/kind/sec/type/18'),]

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

class ChinaTimes(RSSBase):

    def get_id(self):
        return 'chinatimes'

    def get_desc(self):
        return '中國時報'

    def get_rss_links(self):
        return [('中國時報', 'http://www.chinatimes.com/rss/chinatimes.xml'),]
