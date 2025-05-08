import hmac
import hashlib

def sign_token(token, secret_key):
    return hmac.new(secret_key.encode(), token.encode(), hashlib.sha256).hexdigest()

#ping:abc123:hmac_signature
