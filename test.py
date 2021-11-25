import unittest
from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from loader import bot, dp

from utils.db_api import database


class TestAdd(IsolatedAsyncioTestCase):
    def test_add(self):
        # добавляем в БД пользователя с Id-1, City-1, Genre-1
        # если ранее было реализовано добавление юзера с Id=1
        # тест будет провален, id юзера должен быть UNIQUE
        database.User.create(id=1, city=1, genre=1)

        # проверяем, есть ли такой юзер в БД
        user = database.User.select().where(
            database.User.id == 1
        ).tuples()
        self.assertEqual(user, ('1', '1'))


class TestUpdate(IsolatedAsyncioTestCase):
    def test_update(self):
        # обновляем Id пользователя в БД
        database.User.update(id=2, city=2, genre=2).where(database.User.id == 1).execute()
        # проверяем, есть ли пользователем с Id=2
        user = database.User.select().where(
            database.User.id == 2
        ).tuples()
        self.assertEqual(user, ('2', '2',))


class TestAddNotification(IsolatedAsyncioTestCase):
    def test_add_notification(self):
        database.Notification.create(user=2, event=2, date=datetime.now())
        user = database.Notification.select().where(
            database.Notification.user == 2
        ).tuples()
        self.assertEqual(user, ('2', '2'))


class TestDeleteNotification(IsolatedAsyncioTestCase):
    def test_delete_notification(self):
        database.Notification.delete().where(
            database.Notification.user == 2
        ).execute()
        notification = database.Notification.select().where(
            database.Notification.id == 2
        ).tuples()
        self.assertEqual(notification, None)


class TestDeleteNotificationByUser(IsolatedAsyncioTestCase):
    def test_delete_notification_by_user(self):
        database.User.create(id=3, city=3, genre=3)
        database.Notification.create(user=3, event=2, date=datetime.now())
        database.User.delete().where(
            database.User.id == 3
        ).execute()
        notification = database.Notification.select().where(
            database.Notification.user == 3
        ).tuples()
        self.assertEqual(notification, None)


class TestDelete(IsolatedAsyncioTestCase):
    def test_delete(self):
        # удаляем пользователя из БД с Id=2
        database.User.delete().where(
            database.User.id == 2
        ).execute()
        # проверяем, есть ли пользователем с Id=2
        user = database.User.select().where(
            database.User.id == 2
        ).tuples()
        self.assertEqual(user, None)


class TestNameBot(IsolatedAsyncioTestCase):
    async def test_bot_name(self):
        bot_name = await bot.get_me()
        await bot.close()
        self.assertEqual(bot_name["username"], 'EventTicketBot')


if __name__ == '__main__':
    unittest.main()