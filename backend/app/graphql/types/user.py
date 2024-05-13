import strawberry
from typing import Optional
from enum import Enum


@strawberry.enum
class Role(Enum):
    ADMIN = "admin"
    TESTER = "tester"
    USER = "user"


@strawberry.type
class User:
    id: str
    username: str
    email: str
    discord_id: Optional[int]
    password: str
    role: Role
    token: Optional[str]


@strawberry.type
class PublicUser:
    username: str


@strawberry.type
class AuthenticatedUser:
    username: str
    email: str
    discord_id: Optional[int]
    token: str


@strawberry.type
class PublicUserList:
    users: list[PublicUser]


@strawberry.type
class AdminUserList:
    users: list[User]
