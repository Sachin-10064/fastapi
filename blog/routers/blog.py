from fastapi import APIRouter, Depends
from typing import List
from .. import schema, token
from ..database import get_db
from ..repository import blog
from sqlalchemy.orm import Session
from typing_extensions import Annotated
router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[schema.User, Depends(token.get_current_user)]

@router.get("/",  response_model=List[schema.ShowBlog])
async def allblog(current_user: user_dependency, db: db_dependency):
    return blog.get_all_blog(db)


@router.get("/{id}", response_model=schema.ShowBlog)
async def show(id: int, current_user: user_dependency, db: db_dependency):
    return blog.singleblog(id, db)


@router.delete("/{id}",   status_code=200)
async def delete(id: int, current_user: user_dependency, db: db_dependency):
    return blog.delete(id, db)


@router.put("/{id}",  status_code=200)
async def update(id: int, current_user: user_dependency, req: schema.Blog, db: db_dependency):
    return blog.update(id, req, db)


@router.post("/create/", status_code=201)
async def create(req: schema.Blog, current_user: user_dependency, db: db_dependency):
   return blog.create(req, db)

