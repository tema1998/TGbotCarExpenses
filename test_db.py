import sqlite3

try:
    conn = sqlite3.connect("acc.db")
    cursor = conn.cursor()

    #Create user
    cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (1000,))

    #Read users
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

    #Confirm
    conn.commit()

except sqlite3.Error as error:
    print('Error', error)

finally:
    if(conn):
        conn.close()