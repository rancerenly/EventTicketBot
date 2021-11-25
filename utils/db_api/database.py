from datetime import datetime

from peewee import *
from data import config

conn = SqliteDatabase(config.DB)


class BaseModel(Model):
    class Meta:
        database = conn


class City(BaseModel):
    id = AutoField(column_name='CityId', primary_key=True)
    name = TextField(column_name='Name', null=False)

    class Meta:
        table_name = 'City'


class Genre(BaseModel):
    id = AutoField(column_name='GenreId')
    name = TextField(column_name='Name', null=False)

    class Meta:
        table_name = 'Genre'


class User(BaseModel):
    id = IntegerField(column_name='UserTgId', unique=True)
    city = ForeignKeyField(City, related_name='fk_city_user', to_field=id, on_delete='cascade', on_update='cascade')
    genre = ForeignKeyField(Genre, related_name='fk_genre_user', to_field=id, on_delete='cascade', on_update='cascade')

    class Meta:
        table_name = 'User'


class Event(BaseModel):
    id = AutoField(column_name='Id', null=False)
    name = CharField(max_length=100)
    city = ForeignKeyField(City, related_name='fk_city_event', to_field=id, on_delete='cascade', on_update='cascade')
    genre = ForeignKeyField(Genre, related_name='fk_genre_event', to_field=id, on_delete='cascade', on_update='cascade')
    date = DateTimeField(column_name='Date', null=False)
    place = TextField(column_name='Place', null=False)
    age = IntegerField(column_name='Age', null=False)
    link = TextField(column_name='Link')
    photo = TextField(column_name='Photo')
    price = DecimalField(column_name='Price', null=False, rounding=2)
    description = TextField(column_name='Description')

    class Meta:
        table_name = 'Event'


class Notification(BaseModel):
    id = AutoField(null=False)
    user = ForeignKeyField(User, related_name='fk_user_notify', to_field=id,
                           on_delete='cascade', on_update='cascade')
    event = ForeignKeyField(Event, related_name='fk_event_notify', to_field=id,
                            on_delete='cascade', on_update='cascade')
    date = DateTimeField(null=False)

    class Meta:
        table_name = 'Notification'


