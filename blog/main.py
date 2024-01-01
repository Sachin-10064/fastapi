import time
from fastapi import FastAPI,Request
from . import models, middleware
from .database import engine

from .routers import user, blog, mongodb

app = FastAPI()

models.Base.metadata.create_all(engine)

app.middleware('http')(middleware.add_process_time_header)

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(mongodb.router)

# all_routers = app.routes
# for route in all_routers:
#     print(route.path)
# print(app.router)


