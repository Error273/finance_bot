import sqlite3
import datetime


class Database:
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()

    def add_operation(self, user_id, is_income, amount, reason):
        with self.connection:
            return self.connection.execute(
                'INSERT INTO operations (user_id, is_income, amount, reason, date) VALUES (?, ?, ?, ?, ?)',
                (user_id, is_income, amount, reason, datetime.datetime.now(),))
