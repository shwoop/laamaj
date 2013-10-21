#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import socket
import string
import sys
import time

IRCVERSION = u'python Irc'
DEBUG_IRC = False 

class Irc:
    def __init__(self, server, port, nick, ident, realname):
        self.server = server
        self.port = port
        self.nick = nick
        self.ident = ident
        self.realname = realname
        
        self.onRawHandlers = []
        self.onConnectedHandlers = []
        self.onTextHandlers = []
        self.onCtcpHandlers = []
        self.onJoinHandlers = []
        self.onPartHandlers = []
        self.onQuitHandlers = []
        
        self.connected = False

        self.reconnectWait = 10 
        self.wantNick = nick

    def connect(self):
        self.__connect_to_server(self.server, self.port, self.nick,
                self.ident, self.realname)
        self.state = self.stateConnect

    def __connect_to_server(self, server, port, nick, ident, realname):
        self.server = server
        self.port = port
        self.nick = nick
        self.ident = ident
        self.realname = realname
    
    def add_on_raw_handler(self, obj):
        self.onRawHandlers.append(obj)

    def add_on_connected_handler(self, obj):
        self.onConnectedHandlers.append(obj)

    def add_on_text_handler(self, obj):
        self.onTextHandlers.append(obj)

    def add_on_ctcp_handler(self, obj):
        self.onCtcpHandlers.append(obj)

    def add_on_join_handler(self, obj):
        self.onJoinHandlers.append(obj)

    def add_on_part_handler(self, obj):
        self.onPartHandlers.append(obj)

    def __call_on_raw_handlers(self, text):
        for obj in self.onRawHandlers:
            obj(self, text)

    def __call_on_connected_handlers(self, server):
        for obj in self.onConnectedHandlers:
            obj(self, server)

    def __call_on_text_handlers(self, msgfrom, target, text):
        for obj in self.onTextHandlers:
            obj(self, msgfrom, target, text)

    def __call_on_ctcp_handlers(self, msgfrom, target, text):
        for obj in self.onCtcpHandlers:
            obj(self, msgfrom, target, text)

    def __call_on_join_handlers(self, who, channel):
        for obj in self.onJoinHandlers:
            obj(self, who, channel)

    def __call_on_part_handlers(self, who, channel):
        for obj in self.onPartHandlers:
            obj(self, who, channel)

    def __call_on_quit_handlers(self, who, message):
        for obj in self.onQuitHandlers:
            obj(self, who, message)

    def __on_raw(self, text):
        if (DEBUG_IRC):
            print(text)
        self.__call_on_raw_handlers(text)

    def __on_connected(self, server):
        self.__call_on_connected_handlers(server)

    def __on_ctcp(self, msgfrom, target, text):
        #can't rely on handlers to implement this, it's
        #required or some servers might boot us off
        if (text == chr(1) + 'VERSION' + chr(1)):
            self.send_ctcp_msg(msgfrom, 'VERSION ' + IRCVERSION)

        self.__call_on_ctcp_handlers(msgfrom, target, text)

    def __on_text(self, msgfrom, target, text):
        if (self.__is_ctcp_msg(text)):
            self.__on_ctcp(msgfrom, target, text)
        else:
            self.__call_on_text_handlers(msgfrom, target, text)

    def __on_join(self, who, channel):
        self.__call_on_join_handlers(who, channel)

    def __on_part(self, who, channel):
        self.__call_on_part_handlers(who, channel)

    def __on_quit(self, who, message):
        if who == self.wantNick:
            self.send(u'NICK ' + self.wantNick)
        self.__call_on_quit_handlers(who, message)

    def __is_ctcp_msg(self, msg):
        if (len(msg) > 0):
            if (msg[0] == chr(1) and msg.endswith(chr(1))):
                return True
        return False
    
    def join(self, channel):
        self.send(u'JOIN ' + channel)

    def part(self, channel):
        self.send(u'PART ' + channel)

    def send_msg(self, target, text):
        self.send(u'PRIVMSG ' + target + u' :' + text)

    def send_ctcp_msg(self, target, command):
        reply = u'NOTICE ' + target + u' :' + chr(1) + command + chr(1)
        self.send(reply)

    def send(self, text):
        if (DEBUG_IRC):
            print(u'-> ' + text)
        self.s.send(text + u'\r\n')

    def stateConnect(self):
        try:
            print(u'Connecting to %s' % self.server)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.server, self.port))
            self.state = self.stateConnecting
        except socket.error:
            print(u'Unable to connect to %s' % self.server)
            self.s.close()
            self.state = self.stateReconnect
        
    def stateConnecting(self):
        self.send(u'NICK %s' % self.nick)
        self.send(u'USER %s %s %s :%s' % (self.ident, self.server,
            self.nick, self.realname))
        self.readbuf = u''

        self.connected = False

        nickTemp = 0;

        try:
            while not self.connected:
                self.readbuf = (self.readbuf +
                        unicode(self.s.recv(2048), u'ISO-8859-1'))
                temp = string.split(self.readbuf, u'\n');
                self.readbuf = temp.pop();

                for line in temp:
                    line = string.rstrip(line)
                    fullline = line
                    line = string.split(line)

                    if fullline.find(u'Nickname is already in use') != -1:
                        self.nick = self.wantNick + str(nickTemp)
                        nickTemp += 1
                        self.send(u'NICK %s' % self.nick)
                        self.send(u'USER %s %s %s :%s' % (self.ident,
                            self.server, self.nick, self.realname))

                    if (line[1] == u'001'):
                        self.connected = True
                        self.__on_connected(self.server)
                        self.state = self.stateConnected
        except socket.error:
            print(u'Lost connection to %s' % self.server)
            self.s.close()
            self.state = self.stateReconnect

    def stateConnected(self):
        try:
            #this next 3 lines of apparent madness are to
            #ensure we only parse full lines.  We have no
            #guarantee that each chunk of data coming in
            #will be in any way complete...
            self.readbuf = (self.readbuf +
                unicode(self.s.recv(2048), u'ISO-8859-1'))
            temp = unicode.split(self.readbuf, u'\n');
            self.readbuf = temp.pop();
            
            for line in temp:
                line = unicode.rstrip(line)
                fullline = line
                line = unicode.split(line)

                if (line[0] == u'PING'):
                    self.send(u'PONG %s' % line[1])

                self.__on_raw(fullline)
                
                msgfrom = line[0].split(u'!')[0].strip(u':')

                if (line[1] == u'PRIVMSG'):
                    target = line[2]
                    if (target == self.nick):
                        target = u''
                    msg = u' '.join(line[3:])[1:]    
                    self.__on_text(msgfrom, target, msg)
                
                if (line[1] == u'JOIN'):
                    channel = line[2][1:]
                    self.__on_join(msgfrom, channel)

                if (line[1] == u'PART'):
                    channel = line[2]
                    self.__on_part(msgfrom, channel)

                if (line[1] == u'QUIT'):
                    msg = u' '.join(line[2:])[1:]
                    self.__on_quit(msgfrom, msg)

        except socket.error:
            print(u'Lost connection to %s' % self.server)
            self.s.close()
            self.state = self.stateReconnect

    def stateDisconnected(self):
        print(u'Disconnected from %s' % self.server)
        self.state = self.stateReconnect

    def stateReconnect(self):
        time.sleep(self.reconnectWait)
        print(u'Reconnecting to %s' % self.server)
        self.state = self.stateConnect

    def process(self):
        while 1:
            self.state()

