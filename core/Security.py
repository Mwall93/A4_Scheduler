import binascii
import hashlib
import os

def randomString(len):
    return binascii.hexlify(os.urandom(len)).decode()

def generateSalt():
    return randomString(8)

def randomPassword():
    return randomString(32)

def hashPassword(password, salt):
    hash = password + salt
    return hashlib.sha256(hash.encode('utf-8')).hexdigest()