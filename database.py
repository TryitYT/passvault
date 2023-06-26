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
    
def create_user(username, password):
    try:
        cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("INSERT INTO Users(username, password) VALUES (?,?)", (username, password))
            con.commit()
            return cur.lastrowid
        else:
            return "unique"
    except:
        return False

    
def select_logins_by_user(username):
    cur.execute("SELECT * FROM Logins JOIN Users ON User_ID = ID_User WHERE Users.username = ?", (username,))
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
    
def create_login(plattform, username, password, user_id):
    try:
        cur.execute("INSERT INTO Logins(plattform, username, password, User_ID) VALUES (?,?,?,?)", (plattform, username, password, user_id))
        con.commit()
        return cur.lastrowid
    except:
        return False
    
def delete_login(id):
    try:
        cur.execute("DELETE FROM Logins WHERE ID_Login = ?", (id,))
        con.commit()
        return True
    except:
        return False
    
def update_login(id, plattform, username, password):
    try:
        cur.execute("UPDATE Logins SET plattform = ?, username = ?, password = ? WHERE ID_Login = ?", (plattform, username, password, id))
        con.commit()
        return True
    except:
        return False