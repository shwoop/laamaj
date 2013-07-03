"""
Irc Message Parsing Module
"""

##  todo:
##    make more pythonic
##    strip out the regular expressions (?)
##    move to the irc module (?)

import re

class Message:
    """ Message parsing class. """
    handle = ''
    user = ''
    locale = ''
    mtype = ''
    channel = ''
    message = ''
    message_action = ''
    message_focus = ''
    def parse_msg(self, raw_message):
        """
        Parses provided raw irc message.
        
        Extracts:
            handle
            user
            locale
            mtype
            channel
            message
            message_action (commands prefixed with !)
            message_focus (parameters following the command)
        """
        parsed = re.match(":(\w+)!~(\w+)@(.*) (\w+) (#\w+) :(.*)",raw_message)
        if parsed:
            self.handle = parsed.group(1)
            self.user = parsed.group(2)
            self.locale = parsed.group(3)
            self.mtype = parsed.group(4)
            self.channel = parsed.group(5)
            self.message = parsed.group(6)
            parsed = re.match("!(\w+) *(\w*)", self.message)    # analyse message to look for actions !dict etc
            if parsed:
                self.message_action = parsed.group(1)
                if parsed.group(2):    # need to check as there doesn't need to be a focus for the action
                    self.message_focus = parsed.group(2)
            else:
                self.message_action = "NO ACTION"
                self.message_focus = "NO FOCUS"
            return 1
        else:
            return -1

# Quick Test
if __name__ == "__main__":
    m = Message()
    m.parse_msg(":SHWOOP!~SHWOOP@192.168.0.1 PRIVMSG #PERTHROAD :!dict lead")
    print (m.message_action+" "+m.message_focus)
