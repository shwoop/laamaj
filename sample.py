#import some necessary libraries.
import socket 
import re
from datetime import datetime


# Some basic variables used to configure the bot        
server = "IRC.COLOSOLUTIONS.COM" # Server
channel = "#laamaj" # Channel
botnick = "laamaj" # Your bots nick


def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Fuck You!\n")
                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :made from gurders.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server

  #while we're at it lets extract the users name using regular expressions
  usrname = re.match(":(\w+)!",ircmsg)
  if usrname:
    sendmsg(channel, usrname.group(1))
  else:
    sendmsg(channel, "Failure")

  if ircmsg.find(":Hello "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello()
    hello()
 
   
  if (ircmsg.find("!time") != -1) or (ircmsg.find("!date") != -1):
    sendmsg(channel, str(datetime.now()))




#if ircmsg.find(":jamaal!") != -1:
  #  gsmcri = ircmsg.strip(":jamaal!~jamaal@mossad.golani.eu PRIVMSG #perthroad :")
  #  gsmcri = gsmcri[::-1]
  #  sendmsg(channel, gcri)

  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()


