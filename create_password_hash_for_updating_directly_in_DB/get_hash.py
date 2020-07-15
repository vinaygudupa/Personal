import hashlib
ha1 = hashlib.md5("{}:{}:{}".format(username, "phone-qa.voice.plivodev.com", "plivo").encode('utf-8')).hexdigest()
