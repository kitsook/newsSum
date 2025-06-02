# -*- coding: utf-8 -*-

# Copyright (c) 2022 Clarence Ho (clarenceho at gmail dot com)
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

from .base import RSSBase


class TheIndependent(RSSBase):
    """The Independent"""

    def get_id(self):
        return "the_independent"

    def get_desc(self):
        return "The Independent"

    def get_rss_links(self):
        return [
            ("News", "https://www.independent.co.uk/news/rss"),
            ("Sport", "https://www.independent.co.uk/sport/rss"),
            ("Life & Style", "https://www.independent.co.uk/life-style/rss"),
            (
                "Arts & Entertainment",
                "https://www.independent.co.uk/arts-entertainment/rss",
            ),
            ("Travel", "https://www.independent.co.uk/travel/rss"),
            ("Money", "https://www.independent.co.uk/money/rss"),
        ]

    def get_icon_url(self):
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAS1BMVEVHcEzsHzHuKzvsHzHtIDHsHS/sHjDsHC/sIDLsHC//+/vsGS3+6+383eDrAR76w8b70tTvSVTsDyb3qq71lpvyeoHuMD/xYmvrAAceMjFuAAAACnRSTlMAwA3/LqHffkpiO8fdzwAAAUBJREFUKJFtkouOhSAMRFVQoAXKW///SxcQH9fsJBrCSVtn7DQ94koIxad/JGc2NMsP4ht7afspV+wj8TDh8Qch4nrX+cxeFIv3fh+1vOREAR+256g9nnO3PWpHxeJgOUWdLGPdQ8jGGTKxdBr2FJ076klVOCMzjozWYE9GBDk0QxXWi+ycAwd0sOCj0wBHn7BMvL7tHmupgWx9IgAazuTpH0Pq1EcAnQ68khDn4aA2VkN7yJ536wWxkDPQuXGj7XrHim1cba012rstv5Kxx+5qofbhupHNSlfI0FX9h4GXGsKYaUybSFAwp964hSDPwhRjylZnY2oc0D5J9eAbLMxaT6bFYyj2nM9fdn1AporSfljb2o5NGlZZ1BBvH/cqrMOMDRdi82uJ2Efr9BL/Zd/NVffmbuqfnV+kWFchl+fmD510FLQDWTohAAAAAElFTkSuQmCC"
