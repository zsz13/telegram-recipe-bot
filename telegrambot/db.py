import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        rf = result.fetchone()[0]
        print(rf)
        # print(user_id)
        return rf

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        user_id = self.get_user_id(user_id)
        self.cursor.execute("SELECT COUNT(*) FROM records WHERE users_id = ? AND operation = ? AND value = ?",
                            (user_id, operation, value))
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.cursor.execute("INSERT INTO records (users_id, operation, value) VALUES (?, ?, ?)",
                                (user_id, operation, value))
            self.conn.commit()
        else:
            print("Record with this value already exists.")

    def delete_record_by_id(self, id):
        self.cursor.execute("SELECT COUNT(*) FROM records WHERE id = ?", (id,))
        count = self.cursor.fetchone()[0]
        if count > 0:
                    self.cursor.execute("DELETE FROM records WHERE id = ?", (id,))
                    self.conn.commit()
                    print(f"Record with id {id} has been successfully deleted.")
                    return True
        else:
            print(f"The record with ID {id} was not found.")
            return False

    def delete_all_records(self, user_id):
        result_delete_all_records = self.cursor.execute("DELETE FROM records WHERE users_id = (SELECT id from users WHERE user_id = ?)", (user_id,))
        self.conn.commit()
        # print(user_id)
        return result_delete_all_records.fetchall()

    def get_records(self, user_id):
        result = self.cursor.execute(
            "SELECT * FROM records WHERE users_id = (SELECT id from users WHERE user_id = ?) ORDER BY date",
            (user_id,))

        return result.fetchall()

    def close(self):
        self.conn.close()

