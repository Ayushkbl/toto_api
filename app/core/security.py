import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import timedelta, timezone, datetime

from app.schemas.token import Token
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPPIRES_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    print("Inside the creation of access token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPPIRES_MINUTES)
    
    to_encode.update({"exp" : expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def decode_access_token(access_token: Token):
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

