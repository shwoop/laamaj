##
##    message class
##

import re

class Message:
  handle = ''
  user = ''
  locale = ''
  mtype = ''
  channel = ''
  message = ''
  def parse_msg(self, raw_message):
    parsed = re.match(":(\w+)!~(\w+)@(.*) (\w+) (#\w+) :(.*)",raw_message)
    if parsed:
      self.handle = parsed.group(1)
      self.user = parsed.group(2)
      self.locale = parsed.group(3)
      self.mtype = parsed.group(4)
      self.channel = parsed.group(5)
      self.message = parsed.group(6)
      return 1
    else:
      return -1
