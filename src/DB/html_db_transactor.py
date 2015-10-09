__author__ = 'Yifan Li'

import base64
import src.DB.Entry as Entry

class Transactor:

    def __init__(self):
        print "Transactor Created"


    def insert_html(self,url,html):

        encoded_html = base64.b64encode(html)
        t = Entry.Page(url=url, content=encoded_html)
        Entry.Page.add(t)

    
