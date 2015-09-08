#!/usr/bin/python2

# Based on script from http://breakingcode.wordpress.com/2010/06/29/google-search-python/

__all__ = ['search']

from bs4 import BeautifulSoup
import http.cookiejar
import urllib
import os
import time
import re

# URL templates to make Google searches.
url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = http.cookiejar.LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urllib.request.urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    #try:

        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urllib.parse.urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = urllib.parse.parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urllib.parse.urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link


PAGE, COUNT = 1, 2

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0):
    for type_, result in search_helper(query, tld, lang, num, start, stop, pause):
        print((type_, result))
        if type_==PAGE:
            yield result

# Returns an integer number of results
def search_results_for(query): 
    for type_, result in search_helper(query):
        if type_==COUNT:
            return result 

def search_helper(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0):
    """
    Search the given query string using Google.
    query: Query string. Must NOT be url-encoded.
    """

    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Prepare the search string.
    query = urllib.parse.quote_plus(query)

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first request.
    if num == 10:
        url = url_search % vars()
    else:
        url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or start < stop:

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url)

        # Parse the response and process every anchored URL.
        soup = BeautifulSoup(html)

        # Figure out the number of search results
        b = re.compile('''bout\\s+([0-9,]+)\\s+results''')
        num_results = soup.find_all(text=b)
        if num_results:
            assert(len(num_results)==1)
            r = num_results[0]
            c = int(b.search(r).group(1).replace(',',''))
            yield (COUNT, c)
        elif soup.find_all(text=re.compile("did not match any documents")):
                yield (COUNT, 0)
        else:
            pass

        # Process every anchored URL
        anchors = soup.findAll('a')
        for a in anchors:

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            yield (PAGE, link)

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

# When run as a script, take all arguments as a search query and run it.
if __name__ == "__main__":
    import sys
    query = ' '.join(sys.argv[1:])
    if query:
        #for url in search(query, stop=20):
        #    print(url)
        #print("{0} search results found".format(search_results_for(query)))
        print("{0}".format(search_results_for(query)))
