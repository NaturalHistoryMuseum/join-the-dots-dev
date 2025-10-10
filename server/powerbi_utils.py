# from flask import jsonify, request
# from functools import wraps
# from flask_jwt_extended import JWTManager, verify_jwt_in_request
# import jwt, requests
# from server.config import Config

# # Fetch Microsoft’s public signing keys
# jwks = requests.get(Config.JWKS_URL).json()

# def microsoft_jwt_required(scope=None):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request(optional=False)
#             print('this is the request,')

#             print('this is the request,', request)
#             # Extract raw token
#             auth_header = request.headers.get("Authorization", None)
#             if not auth_header:
#                 return jsonify({"msg": "Missing Authorization Header"}), 401
#             token = auth_header.split(" ")[1]

#             try:
#                 decoded = jwt.decode(
#                     token,
#                     jwks,
#                     algorithms=["RS256"],
#                     audience=Config.CLIENT_ID,
#                     issuer=Config.ISSUER
#                 )
#                 # Optional: enforce scope
#                 if scope and scope not in decoded.get("scp", "").split():
#                     return jsonify({"msg": "Missing required scope"}), 403

#                 request.user = decoded
#             except Exception as e:
#                 return jsonify({"msg": str(e)}), 401

#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper


from functools import wraps

import jwt
import requests
from flask import jsonify, request

from server.config import Config

# Fetch Microsoft’s public signing keys once
jwks = requests.get(Config.JWKS_URL).json()


def get_signing_key(token):
    headers = jwt.get_unverified_header(token)
    kid = headers.get('kid')
    for key in jwks['keys']:
        if key['kid'] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    return None


def microsoft_jwt_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'msg': 'Missing Authorization Header'}), 401

            token = auth_header.split(' ')[1]
            try:
                key = get_signing_key(token)
                if not key:
                    return jsonify({'msg': 'Unable to find matching signing key'}), 401

                decoded = jwt.decode(
                    token,
                    key=key,
                    algorithms=['RS256'],
                    audience=Config.AUDIENCE,
                    issuer=Config.VALID_ISSUERS,
                )
                print('post decoded')

                print('this is the decoded token', decoded)

                # Check roles claim (for client credentials flow)
                if role:
                    roles = decoded.get('roles', [])
                    print('this is the roles claim,', roles)
                    if role not in roles:
                        return jsonify({'msg': 'Missing required role'}), 403

                request.user = decoded
            except Exception as e:
                return jsonify({'msg': str(e)}), 401

            return fn(*args, **kwargs)

        return decorator

    return wrapper
