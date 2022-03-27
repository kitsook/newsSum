# newsSum

A Google App Engine application to parse RSS feeds and HTML pages to extract headlines.  Result is available via JSON.

~~Memcache is used to reduce process time.~~ There is no memcache service for GCP Python 3 runtime and the Memorystore for Redis isn't free, so no caching is done on the server side. For now, use the `cache-control` header to have browser / proxy to do the caching.

UI is implemented with Vue. To generate the UI, run `npm run build` under the folder `newssum-ui`. Then copy all the content under `newssum-ui/dist` folder to the `static` folder under root.

A sample instance is hosted at https://news-sum.appspot.com/

Feel free to fork and add more sources (refer to the `sources` folder). Classes under the `sources` folder that extend the `BaseSource` class will be automatically discovered by the `get_sources` function and added to the list.

## Quickstart
Assuming gcloud sdk, python3, and npm are installed.
```
git clone https://github.com/kitsook/newssum.git
cd newssum
# install python packages
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
# compile UI
cd newssum-ui
npm install && npm run build
cp -r dist/* ../static
cd ..
# run local server
python main.py
```
