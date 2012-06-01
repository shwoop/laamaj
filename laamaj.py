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
channel = "#laamaj"
botnick = "laamaj2"
#last_send_time = time.time()
#send_lag = 3.4    # time between each IRC message (to avoid flood)

def sendmsg(chan , msg):
  # pick a channel and send it a message
  #global last_send_time
  #time_since_last = time.time() - last_send_time 
  #if time_since_last < send_lag:
  #  time.sleep(time_since_last)
  ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n")
  #last_send_time = time.time()
                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) 
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :made from gurders.\n")
ircsock.send("NICK "+ botnick +"\n") 
ircsock.send("JOIN "+ channel +"\n")

while 1:
  ircmsg = ircsock.recv(2048)
  ircmsg = ircmsg.strip('\n\r')
  print(ircmsg)

  if ircmsg.find("PING :") != 1:
    ircsock.send("PONG :pingis\n")  
    
  #parsed = re.match(":(\w+)!~(\w+)@(.*) (\w+) (#\w+) :(.*)",ircmsg)
  #if parsed:
  #  handle = parsed.group(1)
  #  user = parsed.group(2)
  #  locale = parsed.group(3)
  #  msg_type = parsed.group(4)
  #  channel = parsed.group(5)
  #  message = parsed.group(6)
 
  if (ircmsg.find("!time") != -1) or (ircmsg.find("!date") != -1):
    sendmsg(channel, str(datetime.now()))
    print("date/time")
    
  if ircmsg.find("!dict") != -1:
    print("Dictionary")
    print(ircmsg)
    define_word = re.search("!dict (\w+)", ircmsg)
    if define_word:
      key_word = define_word.group(1)
      matches = dictionary.lookup_dictionary(key_word)
      if matches:
        sendmsg(channel, key_word.upper())
        sendmsg(channel, "*" * len(key_word))
        for match in matches:
          sendmsg(channel, " " * len(key_word) + match.definition)
          time.sleep(2.5)
      else:
        sendmsg(channel, "  No definition exists for that word.")
    else:
      sendmsg(channel, '  Please use the format "!dict <word>"')
 
 
