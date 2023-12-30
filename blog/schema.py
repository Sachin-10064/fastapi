from pydantic import BaseModel
from typing import List, Union

class Blog(BaseModel):
    # id: int
    title: str
    description: str
    owner_id: int


class User(BaseModel):
    # id: int
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    username: str
    email: str
    class Config():
        from_attributes = True


class ShowBlog(BaseModel):
    title: str
    description: str
    # owner_id: int
    owner: ShowUser
    class Config():
        from_attributes = True

class TokenData(BaseModel):
    username: Union[str, None] = None