from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class JWTService:
    def get_jwt_token(cls, user):
        refresh = RefreshToken.for_user(user)
        token = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

        return token
    
    def get_response_token_jwt(cls, token):
        response = Response(token)
        response.set_cookie(
            key="refreshToken", value=token["refresh_token"], httponly=True
        )
        response.set_cookie(
            key="accessToken", value=token["access_token"], httponly=True
        )

        return response
    
    def response_login_jwt(cls, user):
        token = cls.get_jwt_token(user)
        token_response = cls.get_response_token_jwt(token)
        return token_response
    
    def response_logout_jwt(cls):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("refreshToken")
        response.delete_cookie("accessToken")
        return response
    
    def revork_jwt_token(cls, token):
        try:
            refresh = RefreshToken(token)
            refresh.blacklist()
        except Exception as _:
            return
        
    def get_access_token_by_refresh_token(cls, refresh_token):
        rf_token = RefreshToken(refresh_token)
        access_token = str(rf_token.access_token)
        return access_token
    
    def response_refresh_token_jwt(cls, refresh_token):
        access_token = cls.get_access_token_by_refresh_token(refresh_token)
        response = Response(
            {"access_token": access_token}, status=status.HTTP_200_OK
        )
        response.set_cookie(key="accessToken", value=access_token, httponly=True)
        return response
