# -*- coding: utf-8 -*-
from Crypto.Cipher import XOR
import base64
import config


key = config.key


def encrypt(pwd, key=key):
    """
    Шифровать
    """
    pwd = pwd.encode('utf-8')
    cipher = XOR.new(key)
    encrypt = base64.b64encode(cipher.encrypt(pwd))
    encrypt = encrypt.decode('utf-8')
    return encrypt


def decrypt(cryptpwd, key=key):
    """
    Расшифровывать
    """
    cipher = XOR.new(key)
    decrypt = cipher.decrypt(base64.b64decode(cryptpwd))
    decrypt = decrypt.decode('utf-8')
    return decrypt
