##
##     LAAMAJ - IRC BOT
##
##  Commented out an attempt to limit the rate of message sends to avoid flood but
##  time() and clock() don't appear to be working. Also began regex to pull appart
##  message but only got as far as username atm.
##


import time
import dictionary
import sys
import sqlite3

import irc
import message
import database


server = "IRC.COLOSOLUTIONS.COM"  # EFNet - this server DOES NOT have a kaptcha ;)
default_channel = "#perthroad"
nick = "laamaj"
ident = "lamaaj"
realname = "made from gurders"
send_lag = 3.4    # time between each IRC message (to avoid flood)
channels = [default_channel]

    

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
    #print(msg.message)

    # do some logic.  to be moved to a seperate file.

    if msg.message_action == "dict":            # someone has asked for a definition
        print("dictionary time")
        if msg.message_focus:
            connection.send_msg(msg.channel, msg.message_focus)
            connection.send_msg(msg.channel, "*" * len(msg.message_focus))
            matches = dictionary.lookup_definition(msg.message_focus)
            if matches:
                for match in matches:
                    connection.send_msg(msg.channel, " " * len(msg.message_focus) + match)
                    time.sleep(send_lag)
            else:
                connection.send_msg(msg.channel, "" * len(msg.message_focus) + "No definition found")

    #if msg.message_action == "chnls":          # fire out the channels you're listening to
        #output = ""
        #for channel in channels:
            #if output:      
                #output = output + ", " + channel
            #else:
                #output = channel
            #sendmsg(msg.channel, output)

    #if msg.message_action == "NO ACTION":       # found a url (to save)
        #if msg.message.find("http://") != -1 or msg.message.find("www.") != -1:
            #print ("URL : "+msg.message)
            ##sendmsg(msg.channel, "It looks like " + msg.handle + " posted a URL")
            #try:
                #db.connect()
                #db.run_query("insert into websites (ws_date, ws_user, ws_chan, ws_url)  values (date(\'now\'),\'"+msg.handle+"\',\'"+msg.channel+"\',\'"+msg.message+"\');")
                #db.commit()   
            #except sqlite3.Error, e:
                #print("Error : "+e.args[0])
            #finally:
        #db.close()

    if msg.message_action == "NO ACTION":       # found a url (to save)
        for word in msg.message.split():
            if word.find("http") != -1:
                db.add_website(msg.handle, msg.channel, word)


    if msg.message_action == "sites":
        sites = db.list_last_sites()
        for site in sites:
            connection.send_msg(msg.channel, str(site[0]))
            time.sleep(send_lag)

db = database.Database()

con = irc.Irc(server, 6667, nick, ident, realname)
con.add_on_raw_handler(rawHandler)
con.add_on_connected_handler(connectHandler)
con.add_on_text_handler(textHandler)
con.add_on_join_handler(joinHandler)
con.add_on_part_handler(partHandler)
con.connect()
con.process()
