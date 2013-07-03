##
##     LAAMAJ - IRC BOT
##

## standard library imports
import time
import sys
import sqlite3

## local imports
import irc
import message
import database
from config import get_parameters

## globals
send_lag = 3.4    # time between each IRC message (to avoid flood)
db = False
options = {}    
channels = []


def connectHandler(connection, server):
    print('Connected to ' + server)
    for channel in channels:
           connection.join(channel)


def textHandler(connection, msgfrom, target, text):
    print(target + ': <' + msgfrom + '> ' + text)


def joinHandler(connection, who, channel):
    print(who + ' has joined ' + channel)


def partHandler(connection, who, channel):
    print(who + ' has left ' + channel)


def rawHandler(connection, ircmsg):
    #  parse the message into the Message class for easy access    
    msg = message.Message()
    msg.parse_msg(ircmsg)

    if msg.message_action == "NO ACTION":       # found a url (to save)
        for word in msg.message.split():
            if word.find("http") != -1:
                db.add_website(msg.handle, msg.channel, word)


    if msg.message_action == "sites":
        sites = db.list_last_sites()
        for site in sites:
            connection.send_msg(msg.channel, str(site[0]))
            time.sleep(send_lag)


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
    con.add_on_raw_handler(rawHandler)
    con.add_on_connected_handler(connectHandler)
    con.add_on_text_handler(textHandler)
    con.add_on_join_handler(joinHandler)
    con.add_on_part_handler(partHandler)
    con.connect()
    con.process()


if __name__ == '__main__':
    main()
