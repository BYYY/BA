"""
this is the main service for the server side, it's centralized and not memoryless
"""

from SimpleXMLRPCServer import SimpleXMLRPCServer
import Queue
import pybloom

import utils.PathHelper

utils.PathHelper.configure_dir()

import src.DB.DAL as DAL
import src.config.ConfigConstant as ConfigConstant

__author__ = 'Sapocaly'

db_config = ConfigConstant.DB_CONFIG
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [db_config.DB_HOST, db_config.DB_USER, db_config.DB_PASSWORD, db_config.DB_NAME]))
DAL.create_engine(**config_args)

deploy_config = ConfigConstant.DEPLOY_CONFIG

QUEUE = Queue.Queue()
BLOOM_FILTER = pybloom.BloomFilter(capacity=10000000, error_rate=0.000001)
HASH_MAP = {}

SERVICE_MAP = {'DATA-SERVICE': [], 'LOG-SERVICE': []}


def get_config():
    """
    client side get all server side config from this centralized service
    :return:
    """
    global  SERVICE_MAP
    return SERVICE_MAP


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
        global QUEUE
        QUEUE.put(url)
        ##todo: add check condition here
        return True
    except Exception:
        return False


def register_service(service_name, address, port):
    """
    register all other service to core
    :param service_name:
    :param address:
    :param port:
    :return:
    """
    try:
        global SERVICE_MAP
        SERVICE_MAP[service_name].append((address, port))
        return True
    except Exception:
        return False


def admin(adminCode):

    return True

def save():
    try:
        global QUEUE, BLOOM_FILTER, HASH_MAP
        return True
    except Exception:
        return False



server = SimpleXMLRPCServer((deploy_config.BINDING_ADDRESS, int(deploy_config.CORE_PORT)))
server.register_multicall_functions()
server.register_function(put, 'put')
server.register_function(get, 'get')
server.register_function(put_again, 'put_again')
server.register_function(get_config, 'get_config')
server.register_function(admin, 'admin')
server.register_function(register_service, 'register_service')
print "Service name: core-service"
print "binding address:", deploy_config.BINDING_ADDRESS + ":" + deploy_config.CORE_PORT
server.serve_forever()
