from datetime import datetime, timedelta

from utils.db_api import database


def events_name():
    events = []
    for event in database.Event.select():
        events.append((event.id, event.name))
    return events


def genre_name(genre_id):
    genre = database.Genre.get(database.Genre.id==genre_id)
    return genre.name


def search_event_by_id(event_id):
    event = database.Event.get(database.Event.id == event_id)
    return event


def search_events_by_genre(genre_id):
    events = []
    for event in database.Event.select().join(database.Genre).where(database.Genre.id == genre_id):
        events.append((event.id, event.name))
    return events


def create_user(user_id):
    try:
        database.User.create(id=user_id,
                             city=1, genre=1)
    except Exception as err:
        print('User уже существует')


def notify_day(event_date, time):
    return datetime.strptime(event_date, '%Y-%m-%d %H:%M') - timedelta(int(time)) + timedelta(
        microseconds=datetime.now().microsecond)


def get_genres():
    genres = []
    for genre in database.Genre.select():
        genres.append((genre.id, genre.name))
    return genres
