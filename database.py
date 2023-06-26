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
    
def select_logins_by_user(username):
    cur.execute("SELECT * FROM Logins JOIN Users ON User_ID = ID_User WHERE username = ?", (username,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows

def select_login(id):
    cur.execute("SELECT * FROM Logins WHERE ID_Login = ?", (id,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows[0]