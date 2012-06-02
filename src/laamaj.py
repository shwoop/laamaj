##
##     LAAMAJ - IRC BOT
##
##  Commented out an attempt to limit the rate of message sends to avoid flood but
##  time() and clock() don't appear to be working. Also began regex to pull appart
##  message but only got as far as username atm.
##

import socket 
import re
from datetime import datetime
import time
import dictionary
import message

server = "IRC.COLOSOLUTIONS.COM"  # EFNet - this server DOES NOT have a kaptcha ;)
default_channel = "#laamaj"
nick = "laamaj"
#last_send_time = time.time()
#send_lag = 3.4    # time between each IRC message (to avoid flood)
channels = [default_channel]

def sendmsg(chan , msg):
  # pick a default_channel and send it a message
  #global last_send_time
  #time_since_last = time.time() - last_send_time 
  #if time_since_last < send_lag:
  #  time.sleep(time_since_last)
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")
  #last_send_time = time.time()
    
def joinchan(chan):
  ircsock.send("JOIN " + chan + "\n")
              
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) 
ircsock.send("USER "+ nick +" "+ nick +" "+ nick +" :made from gurders.\n")
ircsock.send("NICK "+ nick +"\n") 
ircsock.send("JOIN "+ default_channel +"\n")

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

  #  parse the message against a number of keywords
  #parsed = re.match("!where", msg.message)
  #if parsed:
  #  sendmsg("Current Channels: " + channels)

  parsed = re.match("!fuckoffto (#\w+)", msg.message)
  if parsed:
    print("f.off")
    newchan = parsed.group(1)
    joinchan(newchan)
    print("Joining channel " + newchan)
    sendmsg(newchan, "Sup Bitches!\n")
    channels.append(newchan)
    
  parsed = re.match("!time", msg.message)
  if parsed:
    print("time")
    sendmsg(msg.channel, str(datetime.now()))

  parsed = re.match("!dict (\w+)", msg.message)
  if parsed:
    print("dict")
    keyword = parsed.group(1)
    matches =  dictionary.lookup_synset(keyword)
    if matches:
      sendmsg(msg.channel, keyword.upper())
      sendmsg(msg.channel, "*" * len(keyword))
      for match in matches:
        sendmsg(msg.channel, " " * len(keyword) + match.definition)
        time.sleep(2.5)
    else:
      sendmsg(msg.channel, "  No definition found.")
  #else:
    #sendmsg(msg.channel, "  Please use the format '!dict <word>'")


