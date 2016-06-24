import hashlib

def getSHA1Digest(file):
    sha1 = hashlib.sha1()
    sha1.update(file.read())
    file.seek(0)
    return sha1.hexdigest()
