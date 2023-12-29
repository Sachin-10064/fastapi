from .database import Base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship



class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), index=True)
    description = Column(String(100))
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="blog")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200), unique=True, index=True)
    password = Column(String(500))

    blog = relationship("Blog", back_populates="owner")
