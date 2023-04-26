from fastapi import FastAPI

from common.router import add_routes

app = FastAPI()

add_routes(app)
