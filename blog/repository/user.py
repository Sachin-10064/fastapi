from passlib.context import CryptContext
from fastapi import status, HTTPException
from .. import models, token
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def user_create(req, db:Session):
    password = get_password_hash(req.password)
    user = models.User(username=req.username, email=req.email, password=password)
    # user = models.User(req)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"data": {"user created successfully"}}


def login(username: str, password: str, db:Session):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user do not exits")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"wrong password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"token": access_token, "type": "bearer"}