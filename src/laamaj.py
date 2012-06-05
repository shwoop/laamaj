##
##     LAAMAJ - IRC BOT
##
##  Commented out an attempt to limit the rate of message sends to avoid flood but
##  time() and clock() don't appear to be working. Also began regex to pull appart
##  message but only got as far as username atm.
##

import socket 
import time
import dictionary
import message
import database
import sys
import sqlite3


server = "IRC.COLOSOLUTIONS.COM"  # EFNet - this server DOES NOT have a kaptcha ;)
default_channel = "#laamaj"
nick = "laamaj"
send_lag = 3.4    # time between each IRC message (to avoid flood)
channels = [default_channel]

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")
    
def joinchan(chan):
  ircsock.send("JOIN " + chan + "\n")
              
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) 
ircsock.send("USER "+ nick +" "+ nick +" "+ nick +" :made from gurders.\n")
ircsock.send("NICK "+ nick +"\n") 
ircsock.send("JOIN "+ default_channel +"\n")



db = database.Database()

while 1:
  ircmsg = ircsock.recv(2048)
  ircmsg = ircmsg.strip('\n\r')
  print(ircmsg)

  if ircmsg.find("PING :") != 1:
    ircsock.send("PONG :pingis\n")  

  #  parse the message into the Message class for easy access    
  msg = message.Message()
  msg.parse_msg(ircmsg)
  print(msg.message)

  # do some logic.  to be moved to a seperate file.

  if msg.message_action == "dict":            # someone has asked for a definition
    print("dictionary time")
    if msg.message_focus:
      sendmsg(msg.channel, msg.message_focus)
      sendmsg(msg.channel, "*" * len(msg.message_focus))
      matches = dictionary.lookup_definition(msg.message_focus)
      if matches:
        for match in matches:
          sendmsg(msg.channel, " " * len(msg.message_focus) + match)
          time.sleep(send_lag)
      else:
        sendmsg(msg.channel, "" * len(msg.message_focus) + "No definition found")

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
    if msg.message.find("http://") != -1 or msg.message.find("www.") != -1:
      db.add_website(msg.handle, msg.channel, msg.message)


  if msg.message_action == "sites":
    sites = db.list_last_sites()
    for site in sites:
      sendmsg(msg.channel, str(site[0]))
      time.sleep(send_lag)

