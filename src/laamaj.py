#!/usr/bin/python
# vim: set fileencoding=utf-8 :
##
##     LAAMAJ - IRC BOT
##

## standard library imports
#from __future__ import print_function   ## for lambda print
import time, sys, sqlite3, re

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
def textHandler(connection, msgfrom, target, text):
    print(u'{0}: <{1}> {2}'.format(target, msgfrom, text))

    if msgfrom in ignorelist:
        print(u'Ignoring')
        return

    ## Check for commands (!<command>) 
    if text.startswith(u'!'):
        pass
        '''
        command = text.split(u' ',1)[0]
        if command == u'!sites':
            sites = db.list_last_sites()
            for site in sites:
                connection.send_msg(target, unicode(site[0]))
                time.sleep(send_lag)
        '''
    
    else:
        ## Parse for url's
        for word in text.split():
            #if u'http' in word:
            if re.search(u'\Ahttps?://.*',word):
                res, out = db.add_website(msgfrom, target, word)
                print (res, out)
                if res == u'repost':
                    msg = u'{0}: The cycle continues...'.format(msgfrom,
                                                        out[0])
                    connection.send_msg(target, msg)

laamaj.connect()
laamaj.process()
