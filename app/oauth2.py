from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from .config import settings as st 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm 
# Expiration time

SECRET_KEY = st.secret_key
ALGORITHM = st.algorithm
ACCESS_TOKEN_EXPIRE_MINS = st.access_token_expire_mins

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return token 

def verify_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")    
        if not id:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail="could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_token(token, credential_exception)
    user =  db.query(models.User).filter(models.User.id == token.id).first()
    return user, token
    