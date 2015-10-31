"""
this is the main service for the server side, it's centralized and not memoryless
"""

from SimpleXMLRPCServer import SimpleXMLRPCServer
import Queue

import utils.PathHelper
import src.DB.DAL as DAL
from src.config import DBconfig

__author__ = 'Sapocaly'

config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)

QUEUE = Queue.Queue()
BLOOM_FILTER = set()
HASH_MAP = {}


def get_config():
    """
    client side get all server side config from this centralized service
    :return:
    """
    return None


def put(url):
    """
    put the url to the queue
    :param url:
    :return:
    """
    try:
        global QUEUE, BLOOM_FILTER
        if not (url in BLOOM_FILTER):
            QUEUE.put(url)
            BLOOM_FILTER.add(url)
        return True
    except Exception:
        return False


def get():
    """
    get the top url from the queue
    :return:
    """
    try:
        global QUEUE
        return QUEUE.get()
    except Exception:
        return False


def put_again(url):
    """
    put the failed url to the queue again, will check the failure counts by the hashtable
    :param url:
    :return:
    """
    try:
        return True
    except Exception:
        return False


def admin(adminCode):
    return True


server = SimpleXMLRPCServer(("127.0.0.1", 8001))
print "Listening on port 8000..."
server.register_multicall_functions()
server.register_function(put, 'put')
server.register_function(get, 'get')
server.register_function(put_again, 'put_again')
server.register_function(get_config, 'get_config')
server.register_function(admin, 'admin')
print 'ready'
server.serve_forever()
