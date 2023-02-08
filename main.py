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

import os

from flask import jsonify, send_from_directory
from flask import Flask, request
from flask_cors import CORS

from util import get_sources

allSources = get_sources()

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app)


# route for source listing
@app.route("/list", methods=["GET"])
def route_list():
    sources = [ { "path": id, "desc": allSources[id].get_desc() } for id in allSources ]
    return jsonify(sources)


@app.route("/about", methods=["GET"])
def route_about():
    return jsonify(_get_app_properties())


# route for sources
def route_source():
    articles = []

    the_path = request.path.strip("/")
    if the_path in allSources:
        articles.extend(allSources[the_path].get_articles())

    return jsonify(articles)


# since we don't have memcache in GCP py3, tell browsers / proxy servers to cache everything to minimize our computation cost
@app.after_request
def add_header(response):
    if (request.path in ["/list", "/about"]):
        return response

    response.cache_control.public = True
    response.cache_control.max_age = 900
    return response


def _get_app_properties():
    return { key: os.environ.get(key) for key in [
        "GOOGLE_CLOUD_PROJECT",
        "GAE_VERSION",
        "GAE_RUNTIME",
    ] }


# register routes for available sources
for id in allSources:
    app.route("/" + id, methods=["GET"])(route_source)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    @app.route("/js/<path:path>", methods=["GET"])
    def send_js(path):
        return send_from_directory("static/js", path)

    @app.route("/", methods=["GET"])
    def root():
        return app.send_static_file("index.html")

    app.run(host="127.0.0.1", port=8080, debug=True)
