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
