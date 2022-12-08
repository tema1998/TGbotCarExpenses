import sqlite3

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


    def add_record(self, user_id, repair_value, fuel_value):
        self.cursor.execute("INSERT INTO `records` (`user_id`, `sp_value`, `fuel_value`) VALUES (?, ?, ?)",
                            (self.get_user_id(user_id),
                             repair_value,
                             fuel_value))
        return self.conn.commit()

    def get_records(self, user_id, year, month):
        start = f'{year}-01-01 00:00:00'
        prev = f'+{str(int(month)-1)} months'
        next = f'+{str(int(month))} months'
        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ? AND `date` BETWEEN datetime(?, ?) AND datetime(?, ?) ORDER BY `date`",
                                     (self.get_user_id(user_id), start, prev, start, next))
        return result.fetchall()

    def get_all_records(self, user_id):
        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ? ORDER BY `date`",
                                     (self.get_user_id(user_id),))
        return result.fetchall()

    def delete_record(self, user_id, record_id):
        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ? AND `id` = ? ",
                                     (self.get_user_id(user_id), record_id))

        if result.fetchall():
            self.cursor.execute("DELETE FROM `records` WHERE `user_id` = ? AND `id` = ? ",
                                         (self.get_user_id(user_id), record_id))
            self.conn.commit()
            return f'Запись с <b>id={record_id}</b> удалена'
        return f'Запись с <b>id={record_id}</b> не найдена'