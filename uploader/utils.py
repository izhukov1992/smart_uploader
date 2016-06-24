import hashlib

def getSHA1Digest(file):
    sha1 = hashlib.sha1()
    sha1.update(file.read())
    return sha1.hexdigest()
