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

  if msg.message_action == "dict":
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
      



#########
#  The below is depricated now the message is parsed in the call to parse_msg

#  parsed = re.match("(http://www\..*)", msg.message)
#  if parsed:
#    print("url" + parsed.group(0))
#    sendmsg(msg.channel, "nice url "+msg.handle+", better not be CP!")

#  parsed = re.match("!fuckoffto (#\w+)", msg.message)
#  if parsed:
#    print("f.off")
#    newchan = parsed.group(1)
#    joinchan(newchan)
#    print("Joining channel " + newchan)
#    sendmsg(newchan, "Sup Bitches!\n")
#    channels.append(newchan)

    
#  parsed = re.match("!time", msg.message)
#  if parsed:
#    print("time")
#    sendmsg(msg.channel, str(datetime.now()))

#  parsed = re.match("!dict (\w+)", msg.message)
#  if parsed:
#    print("dict")
#    keyword = parsed.group(1)
#    matches =  dictionary.lookup_synset(keyword)
#    if matches:
#      sendmsg(msg.channel, keyword.upper())
#      sendmsg(msg.channel, "*" * len(keyword))
#      for match in matches:
#        sendmsg(msg.channel, " " * len(keyword) + match.definition)
#        time.sleep(2.5)
#    else:
#      sendmsg(msg.channel, "  No definition found.")
