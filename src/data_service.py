"""
this is a memoryless service for saving data
can be distributed
"""
from SimpleXMLRPCServer import SimpleXMLRPCServer
import hashlib
import os

import utils.PathHelper
from src.DB.Entry import UrlMap
import src.DB.DAL as DAL
from src.config import DBconfig

config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)

def hash_with_sha224(url):
    return hashlib.sha224(url).hexdigest()

def hash_with_md5(url):
    return hashlib.md5(url).hexdigest()

def get_name_and_folder(url):
    return hash_with_md5(url), hash_with_sha224(url)[-2:]



def __save_to_file(content, path, fname):
    #may want to assume that dir is exist
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(path + fname + '.html', 'w') as f:
        f.write(content)


def save(url, html):
    """
    this is the only open api for saving fetched content.
    main reason for using an api service instead of letting client connect to the datacenter is security
    also, we may define any save function later for different content
    :param url:
    :param html:
    :return:
    """
    try:
        name, folder = get_name_and_folder(url)
        map = UrlMap(url=url, hashed_name=name, hashed_folder=folder)
        UrlMap.add(map)
        path = 'data/html/{}/'.format(folder)
        __save_to_file(html, path, name)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("127.0.0.1", 8001))
    print "starting service......"
    server.register_multicall_functions()
    server.register_function(save, 'save')
    print 'ready for service "save"'
    server.serve_forever()
