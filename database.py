import sqlite3

con = sqlite3.connect("passvault.db") #Erstellen einer Verbindung zur Datenbank. Besser gesagt dem File
cur = con.cursor() #Erstellt ein Cursor

#Funktion für zum erhalten eines User nach einem Namen
def select_user(username):
    cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows[0]

#Erstellt ein User, gibt den Wert "unique" zurück wenn der User schon existiert.    
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

#Funktion zum erhalten der Logins von einem User    
def select_logins_by_user(username):
    cur.execute("SELECT * FROM Logins JOIN Users ON User_ID = ID_User WHERE Users.username = ?", (username,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows

#CRUD von den Logins. Create, Read, Update, Delete

#Funktion zum erhalten eines Logins
def select_login(id):   
    cur.execute("SELECT * FROM Logins WHERE ID_Login = ?", (id,))
    rows = cur.fetchall()
    if len(rows)==0:
        return False
    else:
        return rows[0]

#Funktion zum erstellen eines Logins
def create_login(plattform, username, password, user_id):
    try:
        cur.execute("INSERT INTO Logins(plattform, username, password, User_ID) VALUES (?,?,?,?)", (plattform, username, password, user_id))
        con.commit()
        return cur.lastrowid
    except:
        return False

#Funktion um ein Login zu löschen
def delete_login(id):
    try:
        cur.execute("DELETE FROM Logins WHERE ID_Login = ?", (id,))
        con.commit()
        return True
    except:
        return False

#Funktion fpr zum bearbeiten eines Logins
def update_login(id, plattform, username, password):
    try:
        cur.execute("UPDATE Logins SET plattform = ?, username = ?, password = ? WHERE ID_Login = ?", (plattform, username, password, id))
        con.commit()
        return True
    except:
        return False