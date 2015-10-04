import src.DB.DAL as DAL
import urllib2
from utils import DBconfig
import src.DB.Entry as Entry
__author__ = 'Sapocaly'

config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                          [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)




# with DAL.connection():
#     for i in range(10):
#         t = Entry.Page(url='test_url', content='test_content')
#         Entry.Page.add(t)
#         del (t)
#
# with DAL.transaction():
#     Entry.Page.remove(Entry.Page.get())

def fetch(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def save_html(url,html):
    import base64
    encoded_html = base64.b64decode(html)
    with DAL.connection():
        t = Entry.Page(url=url, content=encoded_html)
        Entry.Page.add(t)
        del(t)

url = "www.centre.edu"
html = fetch(url)
save_html(url,html)