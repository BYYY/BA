__author__ = 'Yifan Li'

import base64
import src.DB.Entry as Entry


from src.utils import DBconfig

import src.DB.DAL as DAL

class Transactor:

    def __init__(self):
        print "Transactor Created"


    def insert_html(self,url,html):

        encoded_html = base64.b64encode(html)
        t = Entry.Page(url=url, content=encoded_html)
        Entry.Page.add(t)

    def save_html(self,id):
        f = open("html/"+str(id)+".html",'w')
        t = Entry.Page.get(id=id)[0]
        decoded_html = base64.b64decode(t['_content'])
        f.write(decoded_html)
        f.close()


def main():
    config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
    config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                           [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
    DAL.create_engine(**config_args)

    trans = Transactor()
    trans.save_html()
if __name__ == '__main__':
    main()
