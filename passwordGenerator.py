import string, random, hashlib, os, binascii, hmac

class pg (object) :
        def password(self, password, salt, pepper) :
                #add the salt to the password
                print "clean password : " + password
                password = hmac.new(salt, password, hashlib.sha512).hexdigest()
                print "salted password : " + password
                #add the pepper to the password
                password = hmac.new(pepper, password, hashlib.sha512).hexdigest()
                print "peppered after some salt : " + password
                return password
        