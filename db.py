import sqlite3

db = sqlite3.connect('bans.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS bans (
    chat_id INTEGER
)""")

db.commit()

c = db.cursor()


def is_ban(chat_id: int):
    sql.execute(f"SELECT chat_id FROM bans WHERE chat_id = '{chat_id}'")
    return not sql.fetchone() is None

def ban_user(chat_id: int):
    if not is_ban(chat_id):
        a = "INSERT INTO bans (chat_id) VALUES (?);"
        data_tuple = (chat_id,)
        sql.execute(a, data_tuple)
        db.commit()
        return 'success'
    else:
        return 'already ban'
    

def unban_user(chat_id: int):
    if not is_ban(chat_id):
        return 'not banned'
    else:
        a = "DELETE FROM bans WHERE chat_id=?;"
        data_tuple = (chat_id,)
        sql.execute(a, data_tuple)
        db.commit()
        return 'success'