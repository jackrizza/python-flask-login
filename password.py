"""
you will need to do a pip install of 
- redis
- hmac
"""
from db import DB
from passwordGenerator import pg
import redis, string, random, hashlib, os, binascii, hmac
"""
set up varibles that will become global to the class only
"""
#declare database class
db = DB()
pg = pg()

r = redis.StrictRedis(host='localhost', port=6379, db=0)
sap = []

class Password (object) :
        """
        global varibles for the database
        """
        global sap
        global r

        """
        salt and pepper generator
        """
        def id_generator(self):
                #make a random string for the salt and pepper
                #salt
                sap.append(binascii.b2a_hex(os.urandom(15)))
                #pepper
                sap.append(binascii.b2a_hex(os.urandom(15)))
        """
        this is to verify that the Password that the user typed in
        is the same as the password in the database s
        """
        def verifyAccount (self, email, password) :
                #get database password
                accountPassword = db.getUser(email)
                #get the hashes for the user password
                hashed = db.getHash(email)
                print hashed
                #hash the password
                if hashed :
                        password = pg.password(password, hashed[0], hashed[1])
                        if password == accountPassword :
                                #they were the same passwords
                                return True
                        else : 
                                #they were different passwords
                                print "Password on file : " + accountPassword
                                print "User typed password : " + password
                                return False
                else :
                        print "sap error"
                        return False