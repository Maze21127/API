import binascii
import os
import hashlib
from settings import SALT


def get_key():
    return binascii.hexlify(os.urandom(20)).decode()


def get_hash(string):
    temp = string + SALT
    return hashlib.md5(temp.encode()).hexdigest()


