from .config import TORTOISE_ORM
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
import strawberry
from .graphql.resolvers.user import (
    Query as UserQuery,
    Mutation as UserMutation,
)

load_dotenv("../config/.env")

app = FastAPI()


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

app.add_route("/graphql", GraphQL(schema=schema))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
