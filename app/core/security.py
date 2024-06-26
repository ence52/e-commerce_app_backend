from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt


SECRET_KEY = "ERKAN"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta : Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now()+ expires_delta
    else:
        expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def check_password (plain_password:str,hashed_password:str)->bool:
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes,hashed_password_bytes)