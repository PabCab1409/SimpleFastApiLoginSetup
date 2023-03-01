from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from models.user import User, UserInDB
from models.token import Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db import crud
from jose import JWTError, jwt
from datetime import datetime, timedelta


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = "b95a088c4dc76e84864dbaa94aa4e8d9bf6c25fd756ae194cc2d1d0a02977b10"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def createHashedPassword(password):
    return pwd_context.hash(password)

def getUser(username):
    user_dict  = crud.get_user(username)
    if user_dict:
        return User(**user_dict)
    
def verifyPassword(plainPassword, hashedPassword):
    return pwd_context.verify(plainPassword, hashedPassword)    

def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        tokenData = TokenData(username=username)
        print(tokenData)
    except JWTError:
        raise credentials_exception
    
    user = getUser(tokenData.username)
    if user is None:
        raise credentials_exception
    print(user)
    return user

def authenticateUser(username, plainPassword):
    user = getUser(username)
    if not user:
        return False
    if not verifyPassword(plainPassword, user.password):
        return False
    return user

def createAccessToken(data: dict):
    return jwt.encode(data.copy(), SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token")
async def getToken(form_data: OAuth2PasswordRequestForm = Depends()):
    plainPassword = form_data.password
    user = authenticateUser(form_data.username, plainPassword)
    notAuthenticatedException = HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    if not user:
        raise notAuthenticatedException
    
    accessToken = createAccessToken( data={"sub": user.username})
    return {"access_token": accessToken, "token_type": "bearer"}

@router.get("/login")
async def login(currentUser: User = Depends(getCurrentUser)):
   contacts = crud.get_contacts(currentUser.id)
   return contacts