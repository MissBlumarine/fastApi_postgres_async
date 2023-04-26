from database import db
from fastapi import FastAPI


def init_app():
    db.init()

    app = FastAPI(
        title="Books App",
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from models.crud import api

    app.include_router(
        api,
        prefix="/api",
    )

    return app


app = init_app()

# from fastapi import FastAPI
#
# app = FastAPI(
#     title='Async FastApi'
# )

#
# @app.get('/')
# def hello():
#     return "Hello world"


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
