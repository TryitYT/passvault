import customtkinter
import re
import database #Importiert die database Datei. Dient wie ein DAO (Data Access Object)

#Einzelne Frames für die verschiedenen Komponente der App, die Global zugegrifen müssen werden
root = customtkinter.CTk()
loginFrame = customtkinter.CTkFrame(master=root)
registerFrame = customtkinter.CTkFrame(master=root)
mainFrame = customtkinter.CTkFrame(master=root)
informationFrame = customtkinter.CTkFrame(master=mainFrame, width=550, height=500)

#Globale variablen
loggedInUsername = None #Sobald login, den aktuellen Benutzername
loggedInUserId = None #Sobald login, die akutelle ID vom User (Datenbank)
alreadyError = False  #Verhindert erneutes öffnen von Fehlerfenstern

#Funktion für zum starten des Programms. Wird über main aufgerufen
def init():
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")
    root.geometry("700x500") #Grösse Fenster
    root.title("PassVault")
    root.resizable(False, False)
    root.iconbitmap("logo.ico")
    set_login() #Erstellt zu begin des Programm das login Fenster
    root.mainloop()

#Erstellt ein Error Fenster mit der mitgegebenen Nachricht
def error_frame(error):
    global alreadyError
    if (not (alreadyError == True)):
        alreadyError = True
        errorFrame = customtkinter.CTkToplevel()
        errorFrame.title("Error")
        errorFrame.resizable(False, False)
        errorMessage = customtkinter.CTkLabel(master=errorFrame, text=error)
        errorMessage.pack(pady=10, padx=10)
        def close_error():
            errorFrame.destroy()
            global alreadyError
            alreadyError = False
        closeButton = customtkinter.CTkButton(master=errorFrame, text="Close", command= lambda : close_error())
        closeButton.pack(pady=10, padx=10)
        errorFrame.wm_transient(root) #Verhindert das das Error Fenster hinter dem Hauptfenster erstellt wird

#Überprüft ob das Passwort "sicher" ist.
def secure_password(password):
    x = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password)
    # (?=.*\d) -> Checkt ob mindestens eine Zahl vorhanden ist
    # (?=.*[a-z]) -> Checkt ob es mindestens ein kleiner Buchstaben hat
    # (?=.*[A-Z]) -> Checkt ob es mindestens ein grossen Buchstaben hat
    # (?=.*[a-zA-Z]) -> Checkt ob es überhaupt ein Zeichen hat
    # {8,} -> Mindestens 8 Zeichen
    return x

#Überprüft ob das Password mit dem eingegebenen Übereinstimmt. Checkt auch ob es diesen Überhaupt gibt.
def check_login(username, password):
    userInfo = database.select_user(username)
    if(not userInfo):
        error_frame("User doesn't exit.")
    elif (userInfo[2] == password):
        global loggedInUsername
        loggedInUsername = username
        global loggedInUserId
        loggedInUserId = userInfo[0]
        set_main() #Erstellt das eingeloggte GUI
    else:
        error_frame("Wrong password.")

#Erstellt ein User und erkennt alle möglichen Fehler
def create_user(username, password, repassword):
    if (not (username == "")):
        if (not (password == "" or repassword == "")):
            if (password == repassword):
                if (not (secure_password(password) == None)):
                    feedbackCreate = database.create_user(username, password)
                    print(feedbackCreate)
                    if (not feedbackCreate):
                        error_frame("error: couldn't create user")
                    elif (feedbackCreate == "unique"):
                        error_frame("User already exists.")
                    else:
                        registerFrame.pack_forget() 
                        set_login() #Leitet den User nach einem erfolgreichem regristrieren zur Login Seite
                else:
                    error_frame("The password needs atleast 8 letter. It must contain a small letter, a capital letter, and a number.")
            else:
                error_frame("The passwords don't match.")
        else:
            error_frame("Please enter a password.")
    else:
        error_frame("Please enter a username.")

       
#Erstellt ein neues Login für einen bestimmten User.            
def create_login(plattform, username, password, user_id):
    feedbackCreate = database.create_login(plattform, username, password, user_id)
    if (not feedbackCreate):
       error_frame("error: couldn't create login")
    else:
        set_main() #Erfrischt die gnaze Seite für das der neue Eintrag sichtbar ist
        set_login_frame(feedbackCreate) #Zeigt direkt den Eintrag an, wenn dieser erfolgreich erstellt wurde

#Löscht ein Login
def delete_login(id):
    feedbackDelete = database.delete_login(id)
    if (not feedbackDelete):
        error_frame("error: couldn't delete login")
    else:
        #Zerstört alle Komponenten auf dem Informations Frame
        for child in informationFrame.winfo_children():
            child.destroy()
        set_main() #Refreshed die ganze Seite für das der Eintrag nicht mehr sichtbar ist.

#Bearbeitet ein Login
def edit_login(id, plattform, username, password):
    feedbackEdit = database.update_login(id, plattform, username, password)
    if (not feedbackEdit):
        error_frame("error: couldn't update login")
    else: 
        set_main() #Refreshed die Seite falls es eine Änderung am Titel gäbe
        set_login_frame(id) #Zeigt den neuen bearbeiteten Eintrag direkt an
        
#Switched zwischen dem Regristrieren und dem Login Frame
def switch_login_register(switch):
    if switch == True:
        loginFrame.pack_forget()
        set_register()
    else:
        registerFrame.pack_forget()
        set_login()

#Zeigt das den Informations Frame an. Ähnlich wie wenn man den Frame nun sichtbar macht
def grid_information():
    informationFrame.pack_propagate(0)
    informationFrame.grid(pady=10, padx=(0,10),row=0, rowspan=3, column=1, columnspan=5, sticky='w')

#Erstellt das "Bearbeiten von einem Login" Frame.
def set_edit_login_frame(id):
    login = database.select_login(id)
    if (not login):
        error_frame("error: id doesn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattformEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Plattform Name")
        plattformEditInput.insert(0, login[1]) #Fügt in das Eingabefeld die jetzigen Daten ein
        plattformEditInput.pack(pady=10, padx=10)
        usernameEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Username")
        usernameEditInput.insert(0, login[2]) #Fügt in das Eingabefeld die jetzigen Daten ein
        usernameEditInput.pack(pady=10, padx=10)
        passwordEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Password")
        passwordEditInput.insert(0, login[3]) #Fügt in das Eingabefeld die jetzigen Daten ein
        passwordEditInput.pack(pady=10, padx=10)
        editButton = customtkinter.CTkButton(master=informationFrame, text="Edit", command= lambda : edit_login(id, plattformEditInput.get(), usernameEditInput.get(), passwordEditInput.get()))
        editButton.pack(pady=10, padx=10)
        grid_information() 
        
#Erstellt den Informations Frame für ein einzelnes Login
def set_login_frame(id):
    login = database.select_login(id)
    if (not login):
        error_frame("error: id doesn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattform = customtkinter.CTkLabel(master=informationFrame, text=login[1] + " Login", font=("Roboto", 36))
        plattform.pack(pady=(10, 30),padx=10)
        username = customtkinter.CTkLabel(master=informationFrame, text="Username: "+login[2])
        username.pack(pady=10,padx=10)
        password = customtkinter.CTkLabel(master=informationFrame, text="Password: "+login[3])
        password.pack(pady=10, padx=10)
        passwordSecureOrNot = None
        if (secure_password(login[3]) == None):
            passwordSecureOrNot = "Your password is not secure."
        else:
            passwordSecureOrNot = "Your password is secure."
        passwordSecure = customtkinter.CTkLabel(master=informationFrame, text=passwordSecureOrNot)
        passwordSecure.pack(pady=10, padx=10)
        passwordSecureInformation = customtkinter.CTkLabel(master=informationFrame, text="We check if the password has atleast 8 smybols, a lowercase letter, an uppercase letter, and a number.", font=("Roboto", 11))
        passwordSecureInformation.pack(pady=10,padx=10)
        editButton = customtkinter.CTkButton(master=informationFrame, text="Edit Login", command=lambda : set_edit_login_frame(id))
        editButton.pack(pady=10, padx=10)
        deleteButton = customtkinter.CTkButton(master=informationFrame, text="Delete Login", command=lambda : delete_login(id))
        deleteButton.pack(pady=10, padx=10)
        grid_information()

#Erstellt das Frame für zum erstellen von einem Login
def set_create_login_frame():
    informationFrame.grid_remove()
    for child in informationFrame.winfo_children():
        child.destroy()
    plattformNameInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Plattform Name")
    plattformNameInput.pack(pady=10, padx=10)
    usernameInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Username")
    usernameInput.pack(pady=10, padx=10)
    passwordInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Password")
    passwordInput.pack(pady=10, padx=10)
    createButton = customtkinter.CTkButton(master=informationFrame, text="Create", command= lambda : create_login(plattformNameInput.get(), usernameInput.get(), passwordInput.get(), loggedInUserId))
    createButton.pack(pady=10, padx=10)
    grid_information()

#Fügt je nach dem ob man schon Einträge erstellt hat ein anderes Anfangs Frame ein.
def set_start_frame(alreadyEntries):
    if(alreadyEntries):
        description = "Current Version 0.1\nMade with love by Alessio and Jeremias"    
    else:
        description = 'You currently have no logins. \nStart creating your own logins by pressing on the "Create Login" button.'
    informationFrame.grid_remove()
    startTitle = customtkinter.CTkLabel(master=informationFrame, text="Welcome to PassVault, " + loggedInUsername + ".", font=("Roboto", 36))
    startTitle.pack(pady=(10,30), padx=10)
    description = customtkinter.CTkLabel(master=informationFrame, text=description)
    description.pack(pady=10, padx=10)
    grid_information()

#Erstellt das einloggen Frame
def set_login():
    loginFrame.pack(pady=90, padx=210, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=loginFrame, text="Login", font=("Roboto", 24))
    label.pack(pady=(55, 20), padx=10)

    username = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Username", width=200)
    username.pack(pady=(12,5), padx=10)

    password = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Password", show="*", width=200)
    password.pack(pady=(5,12), padx=10)

    login = customtkinter.CTkButton(master=loginFrame, text="Login", command=(lambda : check_login(username.get(), password.get())), width=200)
    login.pack(pady=12,padx=10)

    link = customtkinter.CTkFont(family="Roboto", size=12, underline=True)
    register = customtkinter.CTkLabel(master=loginFrame, text="Don't have an account? Sign Up", font=link, cursor="hand2")
    register.pack(pady=12,padx=10)
    register.bind("<Button-1>", lambda e: switch_login_register(True)) #Bindet das Button-1 (Klick) Event an.

#Erstellt das registrieren Frame
def set_register():
    registerFrame.pack(pady=90, padx=210, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=registerFrame, text="Sign Up", font=("Roboto", 24))
    label.pack(pady=(25, 20), padx=10)

    username = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Username", width=200)
    username.pack(pady=(12,5), padx=10)

    password = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Password", show="*", width=200)
    password.pack(pady=(5,5), padx=10)

    verifyPassword = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Repeat Password", show="*", width=200)
    verifyPassword.pack(pady=(5,12), padx=10)

    login = customtkinter.CTkButton(master=registerFrame, text="Sign Up", command=lambda : create_user(username.get(), password.get(), verifyPassword.get()), width=200)
    login.pack(pady=12,padx=10)

    link = customtkinter.CTkFont(family="Roboto", size=12, underline=True)
    register = customtkinter.CTkLabel(master=registerFrame, text="Already have an account? Login", font=link, cursor="hand2")
    register.pack(pady=(4,12),padx=10)
    register.bind("<Button-1>", lambda e: switch_login_register(False)) #Bindet das Button-1 (Klick) Event an.

#Erstellt das Hauptframe nach einem erfolgreichem Login
def set_main():
    loginFrame.pack_forget()
    registerFrame.pack_forget()
    mainFrame.columnconfigure(0, weight=1) #Einstellung für ein Raster Layout
    mainFrame.columnconfigure(1, weight=1) #  " "
    mainFrame.rowconfigure(1, weight=1) #     " "
    mainFrame.pack(pady=5, padx = 5, fill="both", expand=True)

    listFrame = customtkinter.CTkScrollableFrame(master=mainFrame, width=100, height=400)
    listFrame.grid(pady=(10,0), padx=10, row=0, column=0, sticky='w')

    addLoginButton = customtkinter.CTkButton(master=mainFrame, width=120, height=50, text="Create login", command=lambda : set_create_login_frame())
    addLoginButton.grid(pady=(0,10), padx=10, row=2, column=0, sticky='w')

    grid_information()

    #Hohlt alle akutellen Logins und zeigt diese am Rand an
    userInfo = database.select_logins_by_user(loggedInUsername)
    if (not userInfo):
        set_start_frame(False)
    else:
        set_start_frame(True) 
        for i in range(len(userInfo)):
            frame = customtkinter.CTkFrame(master=listFrame)
            label = customtkinter.CTkLabel(master=frame, text=(userInfo[i])[1], font=("Roboto", 16), cursor="hand2")
            label.pack(pady=1,padx=1, fill="x")
            def make_lambda(x):
                return lambda e:set_login_frame(x)
            label.bind("<Button-1>", make_lambda(((userInfo[i])[0]))) #Bindet das Klick Event auf das Frame
            frame.pack(pady=2, padx=2, fill="x")
            

