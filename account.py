import uuid as uid
import random, hashlib, time
from string import ascii_letters, digits
from validate_email import validate_email

class Account:
    def __init__(self, dbObject, jwtObject):
        self.database = dbObject
        self.jwt = jwtObject

    def profileExist(self, username):
        profile = self.database.selectOne('users', 'username', username)
        if profile is None:
            return(False)
        else:
            return(True)

    def registerUser(self, username, email, password, firstName, lastName, dob, country, ipAddr):
        if self.profileExist(username):
            return({"error":{"Username already used."}})

        if ((username.isalnum()) and (firstName.isalpha()) and (lastName.isalpha()) and (validate_email(email))):
            salt,unixjoin = [''.join(random.sample(ascii_letters+digits, 8)), int(time.time())]
            passhash = hashlib.blake2b((password+salt).encode()).hexdigest()
            self.database.insertOne('users', '(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [str(uid.uuid4()), email, username, passhash, salt, None, firstName, lastName, dob, country, None, None, ipAddr, unixjoin])
            return({"success":{"username":username, "email":email}})

        else:
            return({"error":{"One or more fields were invalid."}})

    def login(self, username, password):
        if (not self.profileExist(username)) and username.isalnum():
            return({"error":"Incorrect credentials"})
        profile = self.database.selectOne('users', 'username', username)
        if (hashlib.blake2b((password+profile['salt']).encode()).hexdigest()) == profile['passhash']:
            return({"success":{"token":self.jwt.generateToken('PrivateKey.pem', profile['uuid'], 20160)}}) #14days
        else:
            return({"error":"Incorrect credentials"})


    def changePassword(self, token, pwFrom, pwTo):
        token = self.jwt.verifyToken('PrivateKey.pem', token)
        profile = self.database.selectOne('users', 'uuid', token['uuid'])
        #Not Done
