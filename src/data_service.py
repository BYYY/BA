"""
this is a memoryless service for saving data
can be distributed
"""
from SimpleXMLRPCServer import SimpleXMLRPCServer
import hashlib
import os
import xmlrpclib

import utils.PathHelper

utils.PathHelper.configure_dir()

from src.DB.Entry import UrlMap
import src.DB.DAL as DAL
import src.config.ConfigConstant as ConfigConstant
import src.utils.ip_helper

db_config = ConfigConstant.DB_CONFIG
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [db_config.DB_HOST, db_config.DB_USER, db_config.DB_PASSWORD, db_config.DB_NAME]))
DAL.create_engine(**config_args)

deploy_config = ConfigConstant.DEPLOY_CONFIG


def __hash_with_sha224(url):
    return hashlib.sha224(url).hexdigest()


def __hash_with_md5(url):
    return hashlib.md5(url).hexdigest()


def __get_name_and_folder(url):
    return __hash_with_md5(url), __hash_with_sha224(url)[-2:]


def __save_to_file(content, path, fname):
    # may want to assume that dir is exist
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(path + fname + '.html', 'w') as f:
        f.write(content)


def __register_service(core_address, core_port):
    global deploy_config
    ip = '127.0.0.1' if deploy_config.BINDING_ADDRESS == '127.0.0.1' else src.utils.ip_helper.get_lan_ip()
    proxy = xmlrpclib.ServerProxy('http://{}:{}/'.format(deploy_config.CORE_ADDRESS, deploy_config.CORE_PORT))
    multicall = xmlrpclib.MultiCall(proxy)
    multicall.register_service('DATA-SERVICE', ip, deploy_config.DATA_PORT)
    result = multicall()
    if not tuple(result)[0]:
        raise Exception()


def save(url, html):
    """
    this is the only open api for saving fetched content.
    main reason for using an api service instead of letting client connect to the datacenter is security
    also, we may define any save function later for different content
    :param url: url
    :param html: html string
    :return: true/false
    """
    try:
        name, folder = __get_name_and_folder(url)
        map = UrlMap(url=url, hashed_name=name, hashed_folder=folder)
        UrlMap.add(map)
        path = 'data/html/{}/'.format(folder)
        __save_to_file(html, path, name)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    server = SimpleXMLRPCServer((deploy_config.BINDING_ADDRESS, int(deploy_config.DATA_PORT)))
    server.register_multicall_functions()
    server.register_function(save, 'save')
    print "Service name: data-service"
    print "binding address:", deploy_config.BINDING_ADDRESS + ":" + deploy_config.DATA_PORT
    __register_service(deploy_config.CORE_ADDRESS, deploy_config.CORE_PORT)
    server.serve_forever()
