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

from abc import ABCMeta, abstractmethod
from lxml import etree
import traceback

from logger import logger
from fetcher import read_http_page


class BaseSource:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_desc(self):
        pass

    @abstractmethod
    def get_articles(self):
        pass

    def create_section(self, title):
        return {"title": title}

    def create_article(self, title, url, abstract=None):
        return {"title": title, "url": url, "abstract": abstract}


class RSSBase(BaseSource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rss_links(self):
        return []

    def get_articles(self):
        result_list = []
        for name, url in self.get_rss_links():
            try:
                # for each section, insert a title...
                result_list.append(self.create_section(name))
                # ... then parse the page and extract article links
                data = read_http_page(url)
                if data:
                    doc = etree.fromstring(data, parser=etree.XMLParser(recover=True))
                    for entry in doc.xpath("//rss/channel/item"):
                        title = entry.xpath("title")[0].text
                        link = entry.xpath("link")[0].text
                        abstract = entry.xpath("description")[0].text
                        result_list.append(
                            self.create_article(title.strip(), link, abstract)
                        )
            except Exception as e:
                logger.exception("Problem processing rss: " + str(e))
                logger.exception(
                    traceback.format_exception(e)
                )
        return result_list


class RDFBase(RSSBase):
    __metaclass__ = ABCMeta

    def get_articles(self):
        result_list = []
        for name, url in self.get_rss_links():
            try:
                # for each section, insert a title...
                result_list.append(self.create_section(name))
                # ... then parse the page and extract article links
                doc = etree.fromstring(
                    read_http_page(url), parser=etree.XMLParser(recover=True)
                )

                for entry in doc.xpath(
                    '//*[local-name()="RDF"]/*[local-name()="item"]'
                ):
                    titles = entry.xpath('*[local-name()="title"]')
                    links = entry.xpath('*[local-name()="link"]')
                    abstracts = entry.xpath('*[local-name()="description"]')
                    if titles and links:
                        title = titles[0].text
                        link = links[0].text
                        abstract = abstracts[0].text if abstracts else ""
                        result_list.append(
                            self.create_article(title.strip(), link, abstract)
                        )
            except Exception as e:
                logger.exception("Problem processing rdf: " + str(e))
                logger.exception(
                    traceback.format_exception(e)
                )
        return result_list
