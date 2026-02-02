from jose import jwt , JWTError , ExpiredSignatureError
from passlib.context import CryptContext 
from app.core.config import JWT_ALGORITHM, SECRET
from datetime import datetime, timedelta 
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.database import get_db
from sqlalchemy import select
from app.models.user import User

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

############# passowrd hashing helper ##################

pwd_context=CryptContext(schemes=["argon2"])

def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify(password:str, hashed_password:str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data:dict, token_expiry: Optional[timedelta]=None) :
    data_copy=data.copy()
    if token_expiry:
        expiry=datetime.utcnow() + token_expiry
    else:
        expiry=datetime.utcnow() + timedelta(minutes=30)
    
    data_copy.update({"exp": expiry} )
    
    token=jwt.encode(data_copy,SECRET, algorithm=JWT_ALGORITHM)

    return token

def decode_token(token:str):

    try:
        obj=jwt.decode(token, SECRET, algorithms=[JWT_ALGORITHM])
        return obj
    except ExpiredSignatureError:
        # Token is expired
        return "expired"

    except JWTError:
        return None
    

async def get_current_user(token:str=Depends(oauth2_scheme), db: AsyncSession=Depends(get_db)):

    payload=decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload == "expired":
        raise HTTPException(status_code=401, detail="Token expired")

    email=payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="User Not found")
    if email:
        res=await db.execute(select(User).where(User.email == email))
        user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user 
    


