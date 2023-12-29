from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/",  response_model=List[schema.ShowBlog], tags=["blog"])
async def allblog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@router.get("/blog/{id}", response_model=schema.ShowBlog, tags=["blog"])
async def blog(id: int, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blog


@router.delete("/blog/{id}",   status_code=200, tags=["blog"])
async def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    blog.delete(synchronize_session=False)
    db.commit()
    return {"success": True}


@router.put("/blog/{id}",  status_code=200, tags=["blog"])
async def update(id: int, req: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # blog.update(req, synchronize_session=False)
    blog.title = req.title
    blog.description = req.description
    db.commit()
    db.refresh(blog)
    return req


@router.post("/create", status_code=201, tags=["blog"])
async def create(req: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, description=req.description, owner_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": {"data is save successfully"}}

