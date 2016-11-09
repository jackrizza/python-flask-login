from twilio.rest import TwilioRestClient
from db import DB
import random

db = DB()
__account_sid = "AC8a668d1ccb430db18c162763c9d1d248"
__auth_token = "b43cbd21932d08f79408f6e03456a83c"
client = TwilioRestClient(__account_sid, __auth_token)

class tf (object) :
    
    global client        

    def pin () :
        pin = ""
        for i in 6 :
            pin = pin + str(random.randint(0,9))

        return int(pin)

    def sendMessage (self, number) :
        pin = pin()
        db.setPin(pin)
        self.tfMessage(number, pin)

    def tfMessage (self, number, pin) :
        message = client.messages.create(
        to="+" + number, 
        from_="+15555555555",
        body="Your code is : " + pin)