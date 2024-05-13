import uuid
import bcrypt
from tortoise.models import Model
from tortoise import fields
from tortoise.signals import pre_save


class Role:
    ADMIN = "admin"
    TESTER = "tester"
    USER = "user"

    @classmethod
    def choices(cls):
        return [cls.ADMIN, cls.TESTER, cls.USER]


class User(Model):
    id = fields.CharField(pk=True, max_length=255)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    discord_id = fields.IntField(null=True)
    password = fields.CharField(max_length=255, null=True)
    role = fields.CharField(
        max_length=255, choices=Role.choices(), default=Role.USER
    )
    token = fields.CharField(max_length=500, null=True)


@pre_save(User)
async def generate_uuid(sender, instance, using_db, update_fields):
    if not instance.id:
        instance.id = str(uuid.uuid4())


@pre_save(User)
async def hash_password(sender, instance, using_db, update_fields):
    if not instance.password.startswith("$2b$"):
        instance.password = bcrypt.hashpw(
            instance.password.encode("utf8"), bcrypt.gensalt()
        ).decode("utf8")
