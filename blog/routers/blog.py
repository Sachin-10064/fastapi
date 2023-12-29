from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schema, models
from ..database import get_db
from ..repository import blog
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)


@router.get("/",  response_model=List[schema.ShowBlog])
async def allblog(db: Session = Depends(get_db)):
    return blog.get_all_blog(db)


@router.get("/{id}", response_model=schema.ShowBlog)
async def show(id: int, db: Session = Depends(get_db)):
    return blog.singleblog(id, db)


@router.delete("/{id}",   status_code=200)
async def delete(id: int, db: Session = Depends(get_db)):
    return blog.delete(id, db)


@router.put("/{id}",  status_code=200)
async def update(id: int, req: schema.Blog, db: Session = Depends(get_db)):
    return blog.update(id, req, db)


@router.post("/create/", status_code=201)
async def create(req: schema.Blog, db: Session = Depends(get_db)):
   return blog.create(req, db)

