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


def create_tables():
    with conn:
        conn.create_tables([City, Genre, User, Event, Notification])


def create_events():
    Event.create(
        name='Пой. Танцуй. Люби',
        city=1,
        genre=6,
        date='2022-01-11 19:00',
        place='Театр им. Пушкина',
        age=16,
        link='https://sibdrama.ru/events/poy-tancuy-lyubi',
        photo='https://sibdrama.ru/content/events/0c/0ce3fea9505c7b8ceb678bd2742883f1-devichnik-08-05-2021-009.jpg',
        price=700,
        description='Есть пьесы, написанные мужчинами, сыгранные мужчинами и рассказывающие о мужчинах. Эта пьеса — нечто прямо противоположное.'
    )
    Event.create(
        name='Земля Эльзы',
        city=1,
        genre=6,
        date='2022-01-13 19:00',
        place='Театр им. Пушкина',
        age=16,
        link='https://sibdrama.ru/events/zemlya-elzy',
        photo='https://sibdrama.ru/content/events/cc/cc55fd3ee354c76113b08d780ae129f2-574-1.jpg',
        price=300,
        description='Это спектакль о любви между двумя пожилыми людьми, поставленный по одноименной пьесе Ярославы Пулинович. История о том, что никогда не поздно начать жить настоящим, надеяться на лучшее будущее, даже если что-то идет не так, даже если все вокруг не понимают и осуждают тебя. Ведь найдется человек, который примет тебя таким, каков ты есть.'
    )
    Event.create(
        name='Горе от ума',
        city=1,
        genre=6,
        date='2022-01-14 19:00',
        place='Театр им. Пушкина',
        age=14,
        link='https://sibdrama.ru/events/gore-ot-uma',
        photo='https://sibdrama.ru/content/events/c8/c81ddc3fb6f3fb86735173a8d947fe46-foto-dlya-spiskov.jpg',
        price=300,
        description='Действие известной всем комедии А.С. Грибоедова перенесено в 70-80 годы XX века. На сцене – впечатляющие интерьеры московского метро, артисты в модных костюмах советского времени, звучат хиты 70-80-х годов.'
    )
