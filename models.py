import datetime

from peewee import *


db = SqliteDatabase('bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = BigIntegerField(null=False)
    subscribed = BooleanField(null=False, default=False)
    stat = CharField(null=False)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "users"
        order_by = ('created_at',)


class Chat(BaseModel):
    id = BigIntegerField(null=False)

    user_id = ForeignKeyField(User, related_name='fk_user_prod', to_field='id', on_delete='cascade',
                              on_update='cascade')

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "chats"
        order_by = ('created_at',)


class Photo(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField(null=False)
    time = TimeField()
    date1 = DateField()
    date2 = DateField()
    moons = IntegerField()
    weeks = IntegerField()
    days = IntegerField()
    mes_id = BigIntegerField()
    text = TextField()
    chat_id = ForeignKeyField(Chat, related_name='fk_chat_prod', to_field='id', on_delete='cascade',
                              on_update='cascade')

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "photos"
        order_by = ('created_at',)


def create_tables():
    db.create_tables([User, Chat, Photo])