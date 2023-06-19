import sqlite3

con = sqlite3.connect("passvault.db")
cur = con.cursor()


def select_user(username):
    cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows[0]