from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from service.auth import get_current_user, get_password_hash, verify_password, create_access_token
from service.db import get_session
from schemas.users import CreateUser, ResponseToken, ResponseUser, UpdateUser, UserLogin
from models.users import Users

security = HTTPBearer()

async def get_current_user_db(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
) -> ResponseUser:
    username = get_current_user(credentials.credentials)
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Неверный токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    result = await db.execute(select(Users).filter(Users.id == username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Пользователь не найден"
        )
    
    return user

async def login_user(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_session)
) -> ResponseToken:
    email = credentials.email
    password = credentials.password
    
    result = await db.execute(
        select(Users).filter(Users.email == email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Неверный email или пароль"
        )
    
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    
    return ResponseToken(access_token=access_token, token_type="bearer")

async def create_user(
        user: CreateUser,
        db: AsyncSession = Depends(get_session)
        ) -> ResponseUser:
    
    result = await db.execute(select(Users).filter(Users.email == user.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = Users(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
        bio = user.bio,
        image_url = user.image_url,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(
    user_update: UpdateUser,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
) -> ResponseUser:
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "password" and value:
            setattr(current_user, field, get_password_hash(value))
        else:
            setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user
