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

import json
import sys
import inspect

import webapp2
from google.appengine.api import memcache

from logger import logger
import sources

def get_sources():
    result = {}

    for item in inspect.getmembers(sys.modules['sources'], inspect.isclass):
        cls = item[1]
        if (cls.__name__ != 'BaseSource' and cls.__name__ != 'RSSBase'  and issubclass(cls, sources.BaseSource)):
            obj = cls()
            if hasattr(obj, 'get_id') and hasattr(obj, 'get_desc') and hasattr(obj, 'get_articles'):
                result[obj.get_id()] = obj

    return result

allSources = get_sources()

class MainPage(webapp2.RequestHandler):

    def get(self):
        articles = []
        encodedArticles = json.dumps(articles)

        thePath = self.request.path.strip('/')
        if thePath in allSources:
            # try to retrieve from cache
            encodedArticles = memcache.get(thePath)
            if (encodedArticles == None):
                articles.extend(allSources[thePath].get_articles())
                encodedArticles = json.dumps(articles)
                memcache.add(key=thePath, value=encodedArticles, time=900)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(encodedArticles)

class ListSource(webapp2.RequestHandler):

    def get(self):
        src = []
        for id in allSources:
            src.append({'path': id, 'desc': allSources[id].get_desc()})

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(src))


app = webapp2.WSGIApplication(debug=True)

# route for source listing
app.router.add(('/list', ListSource))

# register routes for available sources
for id in allSources:
    app.router.add(('/' + id , MainPage))
