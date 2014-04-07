#!/usr/bin/python
# vim: set fileencoding=utf8 :
##
##     LAAMAJ - IRC BOT
##

## standard library imports
import time, sys, sqlite3, re, urllib2, lxml.html

## local imports
import irc, database
from config import get_parameters

send_lag = 1
ignorelist = [u'jamaal']

options = get_parameters()
channels = [u'#{0}'.format(options[u'CHANNEL'])]
db = database.Database()
laamaj = irc.Irc(options[u'SERVER'],
                6667,
                options[u'NICK'],
                options[u'IDENT'],
                options[u'REALNAME'])


@laamaj.add_on_connected
def connectHandler(connection, server):
    ''' Join channels when connecting. '''
    print(u'Connected to {0}'.format(server))
    for channel in channels:
           connection.join(channel)


@laamaj.add_on_text
def terminal_echo(connection, msgfrom, target, text):
    ''' echo irc to terminal. '''
    print(u'{0}: <{1}> {2}'.format(target, msgfrom, text))


def get_url_title(url):
    ''' open url and return the title in utf8. '''
    try:
        if url.endswith(u'/'):
            url = url[0:-1]
        request = urllib2.Request(url.encode(u'utf8'))
        request.add_header(u'User-Agent', u'Laamaj/1.0')
        opener = urllib2.build_opener()
        page = opener.open(request)
        tree = lxml.html.parse(page)
        title = tree.findtext(u'.//title')
        if type(title) is str:
            title = title.decode(u'utf8')

    except urllib2.URLError:
        title = u'URLError'

    except urllib2.HTTPError:
        title = u'HTTPError'

    except:
        title = u'Foqt'

    return title


@laamaj.add_on_text
def url_handling(connection, msgfrom, target, text):
    ''' if word is url: fetch it's title and check for reposts '''
    if msgfrom in ignorelist:
        print(u'Ignoring')
        return

    for word in text.split():
        if re.search(u'\Ahttps?://.*', word):
            
            title = get_url_title(word)
            if title:
                mess = u'< %s >' % (title)
                mess = mess.encode(u'ascii', 'replace')
                connection.send_msg(target, mess)

            res, out = db.add_website(msgfrom, target, word)
            print (res, out)
            #if res == u'repost':
                #msg = u'{0}: The cycle continues...'.format(msgfrom)
                #connection.send_msg(target, msg)


laamaj.connect()
laamaj.process()
