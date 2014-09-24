#!/usr/bin/python
# vim: set fileencoding=utf8 :

##
##      LAAMAJ
##      Url handling
##


import urllib2, lxml.html


def parse_title_from_html(page):
    ''' Extract contents of title tag from given html. '''

    try:
        tree = lxml.html.parse(page)
        title = tree.findtext('.//title')
        if type(title) is str:
            title = title.decode('utf8')

    except:
        title = u'ParseError'

    return title


def fetch_url(url, nick = u'laamaj'):
    ''' Fetch given url. '''

    try:
        # reddit seems to redirect on trailing '/' so trim
        if url.endswith('/'):
            url = url[:-1]

        request = urllib2.Request(url.encode('utf8'))
        request.add_header('User-Agent', 'Laamaj/1.0')
        opener = urllib2.build_opener()
        page = opener.open(request)

    except urllib2.URLError:
        page = u'URLError'

    except urllib2.HTTPError:
        page = u'HTTPError'

    return page


def get_url_title(url):
    ''' open url and return the title in utf8. '''

    try:
        page = fetch_url(url)
        if page in {u'URLError', u'HTTPError'}:
            title = page
        else:
            title = parse_title_from_html(page)

    except:
        title = u'Fatal url title exception.'

    return title

