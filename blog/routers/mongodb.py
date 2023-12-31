from fastapi import APIRouter, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# MongoDB Connection
DATABASE_URL_MONGO = "mongodb://localhost:27017"
client = AsyncIOMotorClient(DATABASE_URL_MONGO)
db_mongo = client["fastapi"]

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"]
)

async def get_db_mongo():
    return db_mongo


class Blog(BaseModel):
    title: str
    content: str


@router.get("/blogs/")
async def get_all_blogs(db: AsyncIOMotorDatabase = Depends(get_db_mongo)):
    cursor = db.blog.find({})
    blogs = await cursor.to_list(length=None)  # Convert the cursor to a list
    # Convert ObjectId to string in each document
    for blog in blogs:
        blog['_id'] = str(blog['_id'])

    return blogs


@router.post("/mongo-item/")
async def create_mongo_item(req: Blog, db: AsyncIOMotorDatabase = Depends(get_db_mongo)):
    new_blog = {"title": req.title, "content": req.content}
    result = db.blog.insert_one(new_blog)
    inserted_id = result.inserted_id
    print(inserted_id)
    return {"inserted_id": str(inserted_id)}