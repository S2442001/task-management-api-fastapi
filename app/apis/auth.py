from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.requests import RegisterIn, LoginIn
from app.models.user import User
from app.db.database import get_db
from sqlalchemy import select, func
from app.core.security  import hash_password, verify, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router=APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(register_data: RegisterIn, db:AsyncSession=Depends(get_db)):
    email=register_data.email
    password=register_data.password

    res=await db.execute(select(User).where(User.email==email))
    user=res.scalar_one_or_none()
    if user:
        return {"message": "User already Registered!"}
    
    # 1. Check how many users exist
    result_count = await db.execute(select(func.count(User.id)))
    user_count = result_count.scalar()

    # 2. Decide role
    if user_count == 0:
        role = "admin"
    else:
        role = "user"
    
    hashed_password=hash_password(password)
    
    new_user=User(email=email, hashed_password=hashed_password, role=role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message" : "User Registarion Successfull!"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession=Depends(get_db)):
    user_email=form_data.username
    user_password=form_data.password

    res=await db.execute(select(User).where(User.email==user_email))
    result=res.scalar_one_or_none()
    if not result:
        return {"message": "User not found & needs to Register"}
    
    # User verification Successfull
    if verify(user_password, result.hashed_password):
        data={"sub": user_email}
        token=create_access_token(data)
        return {"access_token": token, "token_type": "bearer"}
    
    return {"message": "Password Not Matching..."}



