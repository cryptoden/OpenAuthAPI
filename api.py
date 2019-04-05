from db import db
import hug
import tokenJWT
import account

database = db('user.db')
jwt = tokenJWT.tokenJWT(database)
acct = account.Account(database, jwt)

#Create Token Verification Function
def verifyToken(token):
    return(jwt.verifyToken('PrivateKey.pem', token))

token_key_authentication = hug.authentication.token(verifyToken)

#API Main Authentication Endpoints
@hug.post('/register')
def register_user(username, email, password, firstName, lastName, dob, country, ipAddr):
    return(acct.registerUser(username, email, password, firstName, lastName, dob, country, ipAddr))

@hug.post('/login')
def login(username, password):
    return(acct.login(username, password))

#API Main Service Endpoints
@hug.get('/testauth', requires=token_key_authentication)
def basic_auth_api_call(user: hug.directives.user):
    return ('Test Good'+user[1]['uuid'])
