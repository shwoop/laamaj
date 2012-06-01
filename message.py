##
##    message class
##

import re

class message:
  _handle
  _user
  _locale
  _type
  _channel
  _message

  def parse(raw_message):
    parsed = re.match(":(\w+)!~(\w+)@(.*) (\w+) (#\w+) :(.*)",ircmsg)
    if parsed:
      _handle = parsed.group(1)
      _user = parsed.group(2)
      _locale = parsed.group(3)
      _msg_type = parsed.group(4)
      _channel = parsed.group(5)
      _message = parsed.group(6)
      return 1
    else:
      return -1
