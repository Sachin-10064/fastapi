from fastapi import APIRouter, Depends, Security
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing_extensions import Annotated
from .. import token, schema

# MongoDB Connection
DATABASE_URL_MONGO = "mongodb://localhost:27017"
client = AsyncIOMotorClient(DATABASE_URL_MONGO)
db_mongo = client["fastapi"]


async def get_db_mongo():
    return db_mongo

mongo_dependencies = Annotated[AsyncIOMotorDatabase, Depends(get_db_mongo)]

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    # dependencies=[Depends(token.get_current_user)]
)

user_dependency = Annotated[schema.User, Security(token.get_current_user, scopes=["admin", "staff"])]

class Blog(BaseModel):
    title: str
    content: str


@router.get("/blogs/")
async def get_all_blogs(current_user: user_dependency, db: mongo_dependencies):
    cursor = db.blog.find({}, {'_id': 0})
    blogs = await cursor.to_list(length=None)  # Convert the cursor to a list
    # Convert ObjectId to string in each document
    # for blog in blogs:
    #     blog['_id'] = str(blog['_id'])
    return blogs


@router.post("/mongo-item/")
async def create_mongo_item(req: Blog, db: mongo_dependencies):
    new_blog = {"title": req.title, "content": req.content}
    result = db.blog.insert_one(new_blog)
    inserted_id = result.inserted_id
    print(inserted_id)
    return {"inserted_id": str(inserted_id)}