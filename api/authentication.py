from passlib.context import CryptContext
from datetime import datetime, timedelta
# from django.conf import settings
from django.contrib.auth import authenticate
from jose import jwt
from requests import Session
from sems import SECRET_KEY, ALGORITHM
from .models import User

myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    """
    Authenticate the user using Django's built-in authentication system
    """
    user = authenticate(username=username, password=password)
    if user is None:
        return False
        # if not myctx.verify(password, user.password_hash):
        # if not pwd_context.verify(password, user.password_hash):

    return user
