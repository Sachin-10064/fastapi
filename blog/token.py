from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer,  OAuth2PasswordRequestForm,SecurityScopes
from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from . import schema
from .database import get_db
from sqlalchemy.orm import Session
from .repository import user
from pydantic import ValidationError


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/login",
    scopes={
        "admin": "Admin ",
        "staff": "Staff",
        "customer": "customer",
        "gust": "gust"
    },
)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def is_token_expired(expiration_time):
    current_time = datetime.utcnow().timestamp()
    return current_time > expiration_time
async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        print(f'Bearer scope="{security_scopes.scope_str}"')
    else:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_scopes = payload.get("scopes", [])
        token_scopes = payload.get("scopes")
        token_data = schema.TokenData(scopes=token_scopes, username=username)
        token_exp = payload.get('exp')
        if is_token_expired(token_exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expires",
                headers={"WWW-Authenticate": 'Bearer'},
            )


    except (JWTError, ValidationError):
        raise credentials_exception
    user1 = user.get_user(db, username=token_data.username)
    if user1 is None:
        raise credentials_exception

    if token_data.scopes not in security_scopes.scopes:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
        )
    # for scope in security_scopes.scopes:
    #     print(scope)
        # if scope not in token_data.scopes:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Not enough permissions",
        #         headers={"WWW-Authenticate": authenticate_value},
        #     )
    return user1
