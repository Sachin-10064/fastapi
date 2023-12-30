from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/registration", status_code=201)
async def registration(req: schema.User, db: Session = Depends(get_db)):
   return user.user_create(req, db)


@router.get("/login", status_code=200)
async def login(username: str, password: str, db: Session = Depends(get_db)):
   return  user.login(username, password, db)