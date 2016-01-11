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
        if (cls.__name__ != 'BaseSource' and issubclass(cls, sources.BaseSource)):
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
