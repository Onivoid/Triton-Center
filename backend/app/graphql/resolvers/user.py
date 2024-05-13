import strawberry
import bcrypt
import os
from typing import Union
from fastapi.requests import HTTPConnection
from app.models.user import User as UserModel
from app.graphql.types.user import (
    User,
    PublicUser,
    PublicUserList,
    AdminUserList,
    AuthenticatedUser,
)
from app.graphql.types.error import Error
from tortoise.exceptions import DoesNotExist
from dotenv import load_dotenv
from jwt import (
    encode as jwt_encode,
)
from datetime import datetime, timedelta
from app.utils.jwt_utils import verify_token

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


@strawberry.type
class Mutation:
    @strawberry.field
    async def register(
        self, info, username: str, email: str, password: str
    ) -> Union[PublicUser, Error]:
        try:
            user = await UserModel.create(
                username=username,
                email=email,
                password=password,
            )
            return PublicUser(
                username=user.username,
            )
        except Exception as e:
            return Error(message=str(e))

    @strawberry.field
    async def login(
        self, info, username: str, password: str
    ) -> Union[AuthenticatedUser, Error]:
        try:
            user = await UserModel.get(username=username)
            if bcrypt.checkpw(
                password.encode("utf8"), user.password.encode("utf8")
            ):
                payload = {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "discord_id": user.discord_id,
                    "exp": datetime.now() + timedelta(hours=12),
                }
                token = jwt_encode(
                    payload=payload, key=SECRET_KEY, algorithm=ALGORITHM
                )
                user.token = token
                await user.save()
                return AuthenticatedUser(
                    username=user.username,
                    discord_id=user.discord_id,
                    email=user.email,
                    token=token,
                )
            else:
                return Error(message="Invalid password")
        except DoesNotExist:
            return Error(message="User not found")


@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self, info: strawberry.private
    ) -> Union[PublicUserList, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)

        if isinstance(payload, str):
            return Error(message=payload)

        users = await UserModel.all()
        return PublicUserList(
            users=[PublicUser(username=user.username) for user in users]
        )

    @strawberry.field
    async def admin_users(
        self, info: strawberry.private
    ) -> Union[AdminUserList, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)
        user_id = payload.get["user_id"]
        adminUser = await UserModel.get(id=user_id)

        if not adminUser.role == "admin":
            return Error(message="Unauthorized")

        users = await UserModel.all()
        return AdminUserList(
            users=[
                User(
                    id=str(user.id),
                    username=user.username,
                    email=user.email,
                    discord_id=user.discord_id,
                    role=user.role,
                )
                for user in users
            ]
        )
