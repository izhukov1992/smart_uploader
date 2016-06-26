import hashlib

def getSHA1Digest(file):
    """
    Generate and return SHA-1 hash
    """
    
    sha1 = hashlib.sha1()

    # File is already opened. Read it
    sha1.update(file.read())

    # Reset file descriptor
    file.seek(0)

    return sha1.hexdigest()
