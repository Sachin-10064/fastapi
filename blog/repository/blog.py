from fastapi import status, HTTPException
from .. import models
from sqlalchemy.orm import Session



def get_all_blog(db:Session):
    blog = db.query(models.Blog).all()
    return blog


def create(req, db:Session):
    new_blog = models.Blog(title=req.title, description=req.description, owner_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": {"data is save successfully"}}


def singleblog(id: int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return blog


def delete(id: int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    blog.delete(synchronize_session=False)
    db.commit()
    return {"success": True}


def update(id, req, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.title = req.title
    blog.description = req.description
    db.commit()
    db.refresh(blog)
    return req
