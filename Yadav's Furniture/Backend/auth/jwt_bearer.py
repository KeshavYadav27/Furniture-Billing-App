# Thhe function of this file is t ocheck weather the request is Authorized or not
# (Verification of protected route)

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_handler import decodeJWT


# jwtbearer is a subclass of HTTPbearer class
class jwtBearer(HTTPBearer):
    def __init__(self,auto_Error:bool=True):
        super(jwtBearer,self).__init__(auto_error=auto_Error)

    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail = "Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail = "Invalid or Expired Token")    
    
    def verify_jwt(self,jwt_token:str):
        isTokenValid:bool = False
        payload = decodeJWT(jwt_token)
        if payload:
            isTokenValid = True
        return isTokenValid

