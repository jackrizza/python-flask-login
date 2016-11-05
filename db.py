"""
you will need to do a pip install of 
- redis
- hmac
"""
import redis, string, random, hashlib, os, binascii, hmac
"""
set up varibles that will become global to the class only
"""
r = redis.StrictRedis(host='localhost', port=6379, db=0)
sap = []

class DB (object):
        """
        global varibles.
        I don't know if there is a better way of doing this but
        it worked
        """
        global r
        global sap

        """
        salt and pepper generator
        """
        def id_generator(self):
                #make a random string for the salt and pepper
                return binascii.b2a_hex(os.urandom(15))
        
        """
        password hasher for db there is on in password as well becasue
        they work the same but require different parameters
        """
        def password(self, password) :
                #add the salt the salt and pepper (sap) array
                sap.append(self.id_generator())
                #add the pepper the salt and pepper (sap) array
                sap.append(self.id_generator())
                #salt the password
                password = hmac.new(sap[0], password, hashlib.sha512).hexdigest()
                #pepper the password
                password = hmac.new(sap[1], password, hashlib.sha512).hexdigest()

                return password
                
        """
        send hashes to the database.
        all of these functions are created to make it easy to 
        swap out redis for something else i.e. mongodb, mysql, postgres
        """
        def setHash (self, email, salt, pepper) :
                """
                add the salt and pepper to the redis database
                sadd => to a array type for redis, requires smembers
                to get the strings.
                read more about sadd http://redis.io/commands/sadd
                read more about smembers http://redis.io/commands/smembers
                """
                #add salt to redis array
                r.sadd('hash:' + email, salt)
                #add pepper to redis array
                r.sadd('hash:' + email, pepper)
        
        """
        create the final account in the database
        """
        def setAccount (self, email, password) :
                r.set('user:' + email, self.password(password))
                self.setHash(email, sap[0], sap[1])