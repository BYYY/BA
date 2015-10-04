__author__ = 'Yuchen Liu'

import HTMLParser

class urlfinder(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for name,value in attrs:
        if name == 'href':
          print value

