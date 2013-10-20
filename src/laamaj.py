##
##     LAAMAJ - IRC BOT
##

## standard library imports
from __future__ import print_function   ## for lambda print
import time
import sys
import sqlite3

## local imports
import irc
#import message
import database
from config import get_parameters

## globals
send_lag = 1
db = False
options = {}
channels = []


def connectHandler(connection, server):
    print('Connected to ' + server)
    for channel in channels:
           connection.join(channel)


def textHandler(connection, msgfrom, target, text):
    print(target + ': <' + msgfrom + '> ' + text)
    
    ## Check for commands (!<command>) 
    if (text.startswith('!')):
        
        command = text.split(' ',1)[0]
        
        if command == "!sites":
            sites = db.list_last_sites()
            for site in sites:
                connection.send_msg(target, str(site[0]))
                time.sleep(send_lag)
    
    else:
        ## Parse for url's
        for word in text.split():
            if "http" in word:
                db.add_website(msgfrom, target, word)


def main():
    """
    Entry point to Laamaj
    """
    
    global options
    global channels
    global db

    options = get_parameters()
    channels = ['#{0}'.format(options['CHANNEL'])]

    db = database.Database()

    con = irc.Irc(options['SERVER'],
        6667,
        options['NICK'],
        options['IDENT'],
        options['REALNAME']
        )
    
    con.add_on_raw_handler(lambda con, msg: None)
    con.add_on_connected_handler(connectHandler)
    con.add_on_text_handler(textHandler)
    con.add_on_join_handler(lambda con, who, chan: print("{0} has joined {1}".format(who, chan)))
    con.add_on_part_handler(lambda con, who, chan: print("{0} has left {1}".format(who, chan)))

    con.connect()
    con.process()


if __name__ == '__main__':
    main()
