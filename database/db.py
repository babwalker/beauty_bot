import sqlite3

conn = sqlite3.connect('User.db')
cursor = conn.cursor()

def create_user(user_id):
    cursor.execute('''
        INSERT OR IGNORE INTO User (user_id)
        VALUES (?)
    ''', (user_id,))

    conn.commit()

def change_user_language(user_id, language):
    cursor.execute('''
        UPDATE User
        SET language = ?
        WHERE user_id = ?
    ''', (language, user_id))

    conn.commit()

def get_users(language):
    cursor.execute("SELECT user_id FROM User WHERE language = ?", (language,))
    return cursor.fetchall()

def get_user_language(user_id):
    cursor.execute("SELECT language FROM User WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        create_user(user_id=user_id)
        return "ru"

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'ru'
        )
    ''')

    conn.commit()

print(get_user_language(user_id=7598687905))
# print(get_users("en")[1][0])