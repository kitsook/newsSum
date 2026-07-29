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

from urllib.parse import urlparse
from curl_cffi import requests
from logger import logger

URL_TIMEOUT = 15


def read_http_page(url, cookies=None, headers=None, method="GET", body=None):
    """Fetch a http page using curl_cffi to impersonate a browser"""
    parsed_url = urlparse(url)
    referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    the_headers = {
        "referer": referer,
    }

    if headers:
        the_headers.update(headers)

    try:
        resp = requests.request(
            method,
            url,
            headers=the_headers,
            cookies=cookies,
            data=body,
            impersonate="chrome",
            timeout=URL_TIMEOUT
        )
        if resp.status_code != 200:
            logger.warning(f"HTTP {resp.status_code} when fetching {url}. Content: {resp.content[:500]}")
        return resp.content
    except Exception as e:
        logger.exception("Problem reading http page: " + str(e))

    return None

