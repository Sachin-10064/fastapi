from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/registration", status_code=201, tags=["user"])
async def registration(req: schema.User, db: Session = Depends(get_db)):
    password = get_password_hash(req.password)
    user = models.User(username=req.username, email=req.email, password=password)
    # user = models.User(req)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"data": {"user created successfully"}}


@router.get("/login",response_model=schema.ShowUser, status_code=200, tags=["user"])
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user do not exits")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"wrong password")

    return user