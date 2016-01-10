from urllib2 import urlopen
import urllib2

URL_TIMEOUT = 60

def readHttpPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    urlPath = urlopen(req, timeout=URL_TIMEOUT)
    return urlPath.read()
