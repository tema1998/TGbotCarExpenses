import sqlite3
import datetime

class BotDB:

    def __init__(self, db_file):
        #Инициализация соединения
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        #Проверка есть ли user в бд
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        #Получить id user в базе по его user_id в телеге
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()


    def add_record(self, RepairOrFuel, user_id, value, date_text):
        date = datetime.date.today()
        if date_text == 'today':
            pass
        elif date_text == 'yesterday':
            date = date - datetime.timedelta(days=1)
        else:
            date = date_text

        if RepairOrFuel == 'fuel':
            self.cursor.execute("INSERT INTO `fuel` (`user_id`, `value`, `date`) VALUES (?, ?, ?)",
                                (self.get_user_id(user_id),
                                value,
                                date))
        elif RepairOrFuel == 'repair':
            self.cursor.execute("INSERT INTO `repair` (`user_id`, `value`, `date`) VALUES (?, ?, ?)",
                                (self.get_user_id(user_id),
                                value,
                                date))
        return self.conn.commit()


    def get_all_fuel_records(self, user_id, year=None, month=None):
        if year == None and month ==None: #If we get history for ALL TIME
            result = self.cursor.execute("SELECT * FROM `fuel` WHERE `user_id` = ? ORDER BY `date`",
                                         (self.get_user_id(user_id),))
            return result.fetchall()
        else:
            start = f'{year}-01-01 00:00:00'
            prev = f'+{str(int(month) - 1)} months'
            next = f'+{str(int(month))} months'
            result = self.cursor.execute(
                "SELECT * FROM `fuel` WHERE `user_id` = ? AND `date` BETWEEN datetime(?, ?) AND datetime(?, ?) ORDER BY `date`",
                (self.get_user_id(user_id), start, prev, start, next))
            return result.fetchall()


    def get_all_repair_records(self, user_id, year=None, month=None):
        if year == None and month == None:  # If we get history for ALL TIME
            result = self.cursor.execute("SELECT * FROM `repair` WHERE `user_id` = ? ORDER BY `date`",
                                         (self.get_user_id(user_id),))
            return result.fetchall()
        else:
            start = f'{year}-01-01 00:00:00'
            prev = f'+{str(int(month) - 1)} months'
            next = f'+{str(int(month))} months'
            result = self.cursor.execute(
                "SELECT * FROM `repair` WHERE `user_id` = ? AND `date` BETWEEN datetime(?, ?) AND datetime(?, ?) ORDER BY `date`",
                (self.get_user_id(user_id), start, prev, start, next))
            return result.fetchall()


    def delete_record(self, user_id, record_id):
        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ? AND `id` = ? ",
                                     (self.get_user_id(user_id), record_id))

        if result.fetchall():
            self.cursor.execute("DELETE FROM `records` WHERE `user_id` = ? AND `id` = ? ",
                                         (self.get_user_id(user_id), record_id))
            self.conn.commit()
            return f'An expense with <b>ID={record_id}</b> successfully deleted'
        return f'Cannot find an expense with <b>ID={record_id}</b>'