from fastapi import APIRouter, Depends
from typing import List
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/",  response_model=List[schema.ShowBlog], tags=["blog"])
async def allblog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    # return {"success": "true", "data": blog}
    print()
    return blog
    # return {"success":True}