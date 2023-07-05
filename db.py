import sqlite3
import datetime


class Database:
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()

    def add_operation(self, user_id, is_income, amount, reason):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO operations (user_id, is_income, amount, reason, date) VALUES (?, ?, ?, ?, ?)',
                (user_id, is_income, amount, reason, datetime.date.today(),))

    def get_data_week(self, user_id):
        return self.cursor.execute(
            "SELECT date, amount, reason, is_income FROM operations WHERE user_id=(?)"
            " AND date BETWEEN datetime('now', '-8 days') AND datetime('now', 'localtime')",
            (user_id,)).fetchall()

    def get_data_month(self, user_id):
        return self.cursor.execute(
            "SELECT date, amount, reason, is_income FROM operations WHERE user_id=(?)"
            " AND date BETWEEN datetime('now', '-32 days') AND datetime('now', 'localtime')",
            (user_id,)).fetchall()

    def get_data_all_time(self, user_id):
        return self.cursor.execute(
            "SELECT date, amount, reason, is_income FROM operations WHERE user_id=(?)", (user_id,)).fetchall()

    def get_categories(self, user_id, is_income):
        return self.cursor.execute(
            'SELECT reason FROM operations'
            ' WHERE user_id=(?) AND is_income=(?)'
            ' GROUP BY reason'
            ' ORDER BY COUNT(*) DESC,'
            ' reason DESC LIMIT 4', (user_id, is_income, )
        ).fetchall()


def init_db(dbfile):
    global db
    db = Database(dbfile)


def get_db():
    return db
