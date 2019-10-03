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

from logger import logger
from fetcher import read_http_page

from .base import BaseSource
from .base import RSSBase

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
