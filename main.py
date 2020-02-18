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

from flask import jsonify, send_from_directory
from flask import Flask
from flask_cors import CORS
# from google.appengine.api import memcache

from logger import logger
from util import get_sources

allSources = get_sources()

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# route for source listing
@app.route('/list', methods=['GET'])
def route_list():
    src = []
    for id in allSources:
        src.append({'path': id, 'desc': allSources[id].get_desc()})

    return jsonify(src)

# route for sources
def route_source():
    articles = []

    from flask import request
    thePath = request.path.strip('/')
    if thePath in allSources:
        # try to retrieve from cache
        # encodedArticles = memcache.get(thePath)
        encodedArticles = None
        if (encodedArticles == None):
            articles.extend(allSources[thePath].get_articles())

    return jsonify(articles)

# register routes for available sources
for id in allSources:
    app.route('/' + id, methods=['GET'])(route_source)


# since we don't have memcache in GCP py3, tell browsers to cache everything to minimize our traffic
@app.after_request
def add_header(response):
    response.cache_control.public = True
    response.cache_control.max_age = 300
    return response


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    @app.route('/js/<path:path>', methods=['GET'])
    def send_js(path):
        return send_from_directory('static/js', path)

    @app.route('/', methods=['GET'])
    def root():
        return app.send_static_file('index.html')

    app.run(host='127.0.0.1', port=8080, debug=True)
