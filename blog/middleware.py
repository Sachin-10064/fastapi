import time

from fastapi import FastAPI, Request

app = FastAPI()

"""
this is a list that we can get at time of requesting 
type
asgi
http_version
server
client
scheme
root_path
headers
state
method
path
raw_path
query_string
app
fastapi_astack
router
endpoint
path_params
route
"""
# @app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # for req in request:
    #     print(req.root_path)
    # print(request.headers)
    return response