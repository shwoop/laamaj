#!/usr/bin/python
# vim: set fileencoding=utf-8 :
##
##     LAAMAJ - IRC BOT
##

## standard library imports
#from __future__ import print_function   ## for lambda print
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
    print(u'Connected to {0}'.format(server))
    #[connection.join(channel) for channel in channels]
    for channel in channels:
           connection.join(channel)

@laamaj.add_on_text
def terminal_echo(connection, msgfrom, target, text):
    print(u'{0}: <{1}> {2}'.format(target, msgfrom, text))

def get_url_title(url):
    try:
        page = urllib2.urlopen(url.encode(u'utf-8'))
        tree = lxml.html.parse(page)
        title = tree.findtext(u'.//title')
    except urllib2.URLError:
        title = u'URLError'
    except urllib2.HTTPError:
        title = u'HTTPError'

    return title

@laamaj.add_on_text
def url_handling(connection, msgfrom, target, text):
    if msgfrom in ignorelist:
        print(u'Ignoring')
        return

    for word in text.split():
        if re.search(u'\Ahttps?://.*', word):
            
            title = get_url_title(word)
            if title:
                connection.send_msg(target, u'< %s >' % (title))

            res, out = db.add_website(msgfrom, target, word)
            print (res, out)
            if res == u'repost':
                msg = u'{0}: The cycle continues...'.format(msgfrom)
                connection.send_msg(target, msg)

laamaj.connect()
laamaj.process()
