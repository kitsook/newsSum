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

import urllib3
import ssl
from urllib3.util.ssl_ import create_urllib3_context

from logger import logger

URL_TIMEOUT = 15

ctx = create_urllib3_context()
# change the TLS signature, so that cloudflare won't consider us as bot and block us for some sites
ctx.set_ciphers('ECDHE+CHACHA20:ECDHE+AESGCM')
ctx.load_default_certs()
ctx.options |= ssl.OP_NO_TLSv1_3
if ctx.options & ssl.OP_NO_COMPRESSION == ssl.OP_NO_COMPRESSION:
    ctx.options ^= ssl.OP_NO_COMPRESSION
http = urllib3.PoolManager(timeout=URL_TIMEOUT, ssl_context=ctx)

def read_http_page(url, cookies=None, headers=None, method="GET", body=None):
    the_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    }

    if cookies:
        the_headers["Cookie"] = ";".join(
            ["%s=%s" % (key, value) for (key, value) in cookies.items()]
        )

    if headers:
        the_headers.update(headers)

    try:
        resp = http.request(method, url, headers=the_headers, body=body)
        return resp.data
    except Exception as e:
        logger.exception("Problem reading http page: " + str(e))

    return None
