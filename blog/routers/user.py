from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user
from typing_extensions import Annotated

router = APIRouter(
    prefix="/user",
    tags=["User"]
)
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/registration", status_code=201)
async def registration(req: schema.User, db: db_dependency):
    return user.user_create(req, db)


@router.post("/login",  response_model=schema.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return user.login(form_data.username, form_data.password, db)