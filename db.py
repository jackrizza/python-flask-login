"""
you will need to do a pip install of 
- redis
- hmac
"""
from passwordGenerator import pg
import redis, string, random, hashlib, os, binascii, hmac
"""
set up varibles that will become global to the class only
"""
pg = pg()
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
                #salt
                sap.append(binascii.b2a_hex(os.urandom(15)))
                #pepper
                sap.append(binascii.b2a_hex(os.urandom(15)))
                        
                
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
        def setAccount (self, email, password, salt, pepper) :
                r.set('user:' + email, password)
                self.setHash(email, salt, pepper)
        """
        set pin for two factor
        """
        def setPin (self, email, pin) :
                r.set('phone:' + email, pin)
        """
        get pin for two factor
        """
        def getPin (self, email) :
                return r.get('phone:' + email)

        """
        initilize a new user
        when signing in it will check if there is a user.
        later getUser should be created to make it easier to change 
        the database that you can you for this project
        """
        def setUser (self, email, password) :
                #check for email in the database
                userCreated = self.getUser(email)
                #if the email is not in the database
                #the users email is the unique key 
                #so this is a very important check
                if userCreated is None :
                        #create the hashed password
                        self.id_generator()
                        password = pg.password(password, sap[0], sap[1])
                        #make the account
                        db.setAccount(email, password, sap[0], sap[1])
                        return True
                #if there is a user already it returns false
                else :
                        return False
        """
        get the salt and pepper for the user from the databsae
        this requires a smembers callback and not a get for redis
        becasue I used sadd in the db class to create a single
        database entry with the salt and pepper
        read more about sadd http://redis.io/commands/sadd
        read more about smembers http://redis.io/commands/smembers
        """             
        def getHash (self, email) :
                #get salt and pepper as a array
                hashes = r.smembers('hash:' + email)
                #loop through the array to add it to salt
                #and pepper array
                if hashes :
                        internalSap = []
                        for hashes in hashes :
                                internalSap.append(hashes)

                        return hashes
                else : 
                        return False
        """
        these get methods are really needed only once but it is so someone 
        can fork this code and use a different database like mysql or mongodb
        it should be known that this getter is used to test if there is a User
        and to get the stored password from the database.
        """
        def getUser (self, email) :
                return r.get('user:' + email)
        