import sqlite3

try:
    conn = sqlite3.connect("error_feedback_favorites_recipe.db")
    cursor = conn.cursor()

    # cursor.execute("INSERT INTO 'records' ('users_id', 'operation', 'value') VALUES (562125844, review, badletter)")
    # cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (101,))
    # cursor.execute("INSERT OR IGNORE INTO 'records' ('users_id','operation','value','date') VALUES (907,'review','udaudzau',2023-08-23)")

    # users = cursor.execute("SELECT * FROM 'users'")
    # users = cursor.execute("SELECT id FROM users WHERE user_id = 101")
    # users = cursor.execute("SELECT * FROM records WHERE users_id = (SELECT id FROM users WHERE id = (SELECT user_id FROM users WHERE user_id = 562125844))ORDER BY date")
    # print(users.fetchall())
    # info_from_records_where_id_from_user = cursor.execute(
    #     # "SELECT * FROM records WHERE users_id = (SELECT id FROM users WHERE id = (SELECT user_id FROM users WHERE "
    #     # "user_id = 562125844))ORDER BY date")
    #     "SELECT * FROM records WHERE users_id = (SELECT id FROM users WHERE user_id = 562125844) ORDER BY date")
    #
    # print(info_from_records_where_id_from_user.fetchall())
    # delete_from_records_where_id_from_user = cursor.execute(
        # "SELECT * FROM records WHERE users_id = (SELECT id FROM users WHERE id = (SELECT user_id FROM users WHERE "
        # "user_id = 562125844))ORDER BY date")
        # "DELETE FROM records WHERE users_id = (SELECT id from users WHERE user_id = 562125844)")

    # print(delete_from_records_where_id_from_user.fetchall())
    # conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()