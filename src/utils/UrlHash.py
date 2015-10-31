import hashlib

__author__ = 'Sapocaly'


def hash_with_sha224(url):
    return hashlib.sha224(url).hexdigest()

def hash_with_md5(url):
    return hashlib.md5(url).hexdigest()

def get_name_and_folder(url):
    return hash_with_md5(url), hash_with_sha224(url)[-2:]



