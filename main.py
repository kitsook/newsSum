import json
import sys
import inspect

import webapp2

from logger import logger
import sources

def getSources():
    result = {}

    for item in inspect.getmembers(sys.modules['sources'], inspect.isclass):
        cls = item[1]
        if (cls.__name__ != 'BaseSource' and issubclass(cls, sources.BaseSource)):
            obj = cls()
            if hasattr(obj, 'getId') and hasattr(obj, 'getDesc') and hasattr(obj, 'getArticles'):
                result[obj.getId()] = obj

    return result

allSources = getSources()

class MainPage(webapp2.RequestHandler):

    def get(self):
        articles = []

        thePath = self.request.path.strip('/')
        if thePath in allSources:
            articles.extend(allSources[thePath].getArticles())
        # for s in allSources:
        #     articles.extend(s.getArticles())

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(articles))

class ListSource(webapp2.RequestHandler):

    def get(self):
        src = []
        for id in allSources:
            src.append({'path': id, 'desc': allSources[id].getDesc()})

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(src))


app = webapp2.WSGIApplication(debug=True)

# route for source listing
app.router.add(('/list', ListSource))

# register routes for available sources
for id in allSources:
    app.router.add(('/' + id , MainPage))
