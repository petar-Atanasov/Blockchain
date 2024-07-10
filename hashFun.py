import hashlib, json

def hashMe(msg=""):
    # this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)
    # sort keys to guarantee repeatability
    
    #encode the string to bytes and calculeate it
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()        
    