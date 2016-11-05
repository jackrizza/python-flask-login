"""
you will need to do a pip install of 
- redis
- hmac
"""
from db import DB
import redis, hashlib, hmac
"""
set up varibles that will become global to the class only
"""
#declare database class
db = DB()
r = redis.StrictRedis(host='localhost', port=6379, db=0)
sap = []

class Password (object) :
        """
        global varibles for the database
        """
        global sap
        global r
        """
        This is the other password function.
        it is only for this class because it requires different 
        parameters to work then the one in the db class
        """
        def password(self, password, salt, pepper) :
                #add the salt to the password
                password = hmac.new(salt, password, hashlib.sha512).hexdigest()
                #add the pepper to the password
                password = hmac.new(pepper, password, hashlib.sha512).hexdigest()
                return password
        
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
                        password = str(db.password(password))
                        #make the account
                        db.setAccount(email, password)
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
                for hashes in hashes :
                        sap.append(hashes)
        """
        these get methods are really needed only once but it is so someone 
        can fork this code and use a different database like mysql or mongodb
        it should be known that this getter is used to test if there is a User
        and to get the stored password from the database.
        """
        def getUser (self, email) :
                return r.get('user:' + email)
        
        """
        this is to verify that the Password that the user typed in
        is the same as the password in the database s
        """
        def verifyAccount (self, email, password) :
                #get database password
                accountPassword = self.getUser(email)
                #get the hashes for the user password
                self.getHash(email)
                #hash the password
                password = self.password(password, str(sap[0]), str(sap[1]))
                if str(password) == str(accountPassword) :
                        #they were the same passwords
                        return True
                else : 
                        #they were different passwords
                        return False