#!/usr/bin/python
# vim: set fileencoding=utf8 :

##
##     LAAMAJ - IRC BOT
##

## standard library imports
import time, sys, sqlite3, re

## local imports
from url_handling import get_url_title 
from irc import Irc
from database import Database
from config import get_parameters

#send_lag = 1 #depricated?
# by default ignore the other bot jamaal
ignorelist = [u'jamaal']
# grap config
options = get_parameters()
# seed channels list with default from config
channels = ['#%s' % (options[u'CHANNEL'])]
# get 'default' database object
db = Database()
# get IRC object
laamaj = Irc(options['SERVER'],
            6667,
            options['NICK'],
            options['IDENT'],
            options['REALNAME'])


@laamaj.add_on_connected
def connectHandler(connection, server):
    ''' Join channels when connecting. '''

    print(u'Connected to %s' % (server))
    for channel in channels:
           connection.join(channel)
           print(u'Joined channel %s' % (channel))


@laamaj.add_on_text
def debug_echo(connection, msgfrom, target, text):
    ''' echo irc to terminal for debugging. '''

    print(u'%s: <%s> %s' % (target, msgfrom, text))


@laamaj.add_on_text
def url_handling(connection, msgfrom, target, text):
    ''' Catch url's from messages and store to database. '''

    if msgfrom in ignorelist:
        print(u'Ignoring')
        return

    for word in text.split():
        if re.search(u'\Ahttps?://.*', word):
            
            # Fetch title and post to channel
            title = get_url_title(word)
            if title:
                mess = u'< %s >' % (title)
                mess = mess.encode('ascii', 'replace')
                connection.send_msg(target, mess)

            # Add website to database
            res, out = db.add_website(msgfrom, target, word)
            print (res, out)
            # removed because of Gary tears
            # post to channel if url is a repost
            #if res == u'repost':
                #msg = u'{0}: The cycle continues...'.format(msgfrom)
                #connection.send_msg(target, msg)


laamaj.connect()
laamaj.process()
