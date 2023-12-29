from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schema
from sqlalchemy.orm import Session
from .database import engine, get_db
from typing import List
# from sqlalchemy import update
from pydantic import ValidationError
from passlib.context import CryptContext
from .routers import user, blog

app = FastAPI()

models.Base.metadata.create_all(engine)

# app.include_router(user.router)
app.include_router(blog.router)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/",  response_model=List[schema.ShowBlog], tags=["blog"])
# async def allblog(db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).all()
#     # return {"success": "true", "data": blog}
#     print()
#     return blog
#     # return {"success":True}


@app.get("/blog/{id}", response_model=schema.ShowBlog, tags=["blog"])
async def blog(id: int, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND

    # return {"success": True, "data": blog}
    return blog


@app.delete("/blog/{id}",   status_code=200, tags=["blog"])
async def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    blog.delete(synchronize_session=False)
    db.commit()
    return {"success": True}


@app.put("/blog/{id}",  status_code=200, tags=["blog"])
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


@app.post("/create", status_code=201, tags=["blog"])
async def create(req: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, description=req.description, owner_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": {"data is save successfully"}}


# user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/registration", status_code=201, tags=["user"])
async def registration(req: schema.User, db: Session = Depends(get_db)):
    password = get_password_hash(req.password)
    user = models.User(username=req.username, email=req.email, password=password)
    # user = models.User(req)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"data": {"user created successfully"}}


@app.get("/login",response_model=schema.ShowUser, status_code=200, tags=["user"])
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user do not exits")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"wrong password")

    return user