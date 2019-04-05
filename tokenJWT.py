import datetime
import calendar
import python_jwt as jwt
import jwcrypto.jwk as jwk

class tokenJWT:
    def __init__(self, dbObject):
        self.database = dbObject

    def generatePrivateKey(self, exportName, keysize=2048):
        key = jwk.JWK.generate(kty='RSA', size=keysize)
        open(exportName, 'w').write(key.export_to_pem(private_key=True, password=None).decode())
        return('Private Key Written')

    def generateToken(self, privateKey, uuid, timeMinutes):
        expirationTime = datetime.timedelta(minutes=timeMinutes)
        key = jwk.JWK.from_pem(open(privateKey, 'r').read().encode())
        payload = {'uuid':uuid}
        token = jwt.generate_jwt(payload, key, 'RS256', expirationTime)
        expirationTime = calendar.timegm((datetime.datetime.utcnow()+expirationTime).utctimetuple())
        self.database.insertOne('tokens', '(?,?,?,?,?)', [uuid, token, False, str(expirationTime), False])
        return(token)

    def verifyToken(self, privateKey, token):
        key = jwk.JWK.from_pem(open(privateKey, 'r').read().encode())
        try:
            dbInfo = self.database.selectOne('tokens', 'token', token)
            if dbInfo['revoked'] == False:
                tokenData = jwt.verify_jwt(token, key, ['RS256'])
                return(tokenData)
            else:
                return(False)
        except:
            return(False)
