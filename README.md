# newsSum

A Google App Engine application to parse RSS feeds and HTML pages to extract
headlines.  Result is available via JSON. Memcache is used to reduce process
time.

UI is implemented with jQuery and Bootstrap.

A sample instance is hosted at https://news-sum.appspot.com/

Feel free to fork and add more sources (refer to the `sources` folder).
Classes under the `sources` folder that extend the `BaseSource` class will
be automatically discovered by the `get_sources` function and added to the
list.
