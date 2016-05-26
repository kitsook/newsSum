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
            doc = html.document_fromstring(read_http_page(baseUrl + '/newspaper/'))
            cal =  doc.get_element_by_id('box300B')
            theDate = cal.attrib['title']
        except Exception as e:
            logger.exception('Problem getting date')

        resultList = []
        sections = [('焦點', baseUrl + '/newspaper/focus/' + theDate),
                    ('政治', baseUrl + '/newspaper/politics/' + theDate),
                    ('社會', baseUrl + '/newspaper/society/' + theDate),
                    ('地方', baseUrl + '/newspaper/local/' + theDate),
                    ('生活', baseUrl + '/newspaper/life/' + theDate),
                    ('言論', baseUrl + '/newspaper/opinion/' + theDate),
                    ('國際', baseUrl + '/newspaper/world/' + theDate),
                    ('財經', baseUrl + '/newspaper/business/' + theDate),
                    ('體育', baseUrl + '/newspaper/sports/' + theDate),
                    ('娛樂', baseUrl + '/newspaper/entertainment/' + theDate),
                    ('消費', baseUrl + '/newspaper/consumer/' + theDate),
                    ('副刊', baseUrl + '/newspaper/supplement/' + theDate),]

        try:
            for (title, url) in sections:
                # for each section, insert a title...
                resultList.append(self.create_section(title))
                curPage = 1
                maxPage = 1
                while curPage <= maxPage:
                    # ... then parse the page and extract article links
                    doc = html.document_fromstring(read_http_page(url + '?page=' + str(curPage)))
                    for link in doc.get_element_by_id('newslistul').xpath('//a[contains(@class, "picword")]'):
                        if link.text and link.get('href'):
                            resultList.append(self.create_article(link.text.strip(), baseUrl + link.get('href')))
                    curPage += 1
                    for pageNum in doc.get_element_by_id('page').xpath('//*[contains(@class, "p_num")]'):
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
        return [('要聞','http://www.appledaily.com.tw/rss/create/kind/sec/type/5'),
                ('國際','http://www.appledaily.com.tw/rss/create/kind/sec/type/7'),
                ('娛樂','http://www.appledaily.com.tw/rss/create/kind/sec/type/9'),
                ('體育','http://www.appledaily.com.tw/rss/create/kind/sec/type/10'),
                ('財經','http://www.appledaily.com.tw/rss/create/kind/sec/type/8'),
                ('房市地產','http://www.appledaily.com.tw/rss/newcreate/kind/sec/type/31488836'),
                ('論壇與專欄','http://www.appledaily.com.tw/rss/newcreate/kind/sec/type/forum'),
                ('副刊','http://www.appledaily.com.tw/rss/create/kind/sec/type/17'),
                ('旅遊與美食總','http://www.appledaily.com.tw/rss/create/kind/sec/type/ALL24'),
                ('家庭與健康','http://www.appledaily.com.tw/rss/create/kind/sec/type/19'),
                ('科技3C','http://www.appledaily.com.tw/rss/create/kind/sec/type/18'),]
