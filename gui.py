import customtkinter
import re
import database

root = customtkinter.CTk()
loginFrame = customtkinter.CTkFrame(master=root)
registerFrame = customtkinter.CTkFrame(master=root)
mainFrame = customtkinter.CTkFrame(master=root)
informationFrame = customtkinter.CTkFrame(master=mainFrame, width=550, height=500)

loggedInUsername = ""
loggedInUserId = None

def init():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root.geometry("700x500")
    root.title("PassVault")
    root.resizable(False, False)
    root.iconbitmap("logo.ico")
    set_login()
    root.mainloop()

def check_login(username, password):
    userInfo = database.select_user(username)
    if(not userInfo):
        print("Not found")
    elif (userInfo[2] == password):
        global loggedInUsername
        loggedInUsername = username
        global loggedInUserId
        loggedInUserId = userInfo[0]
        set_main()
    else:
        print("Password wrong")

def create_user(username, password, repassword):
    if (not (username == "")):
        if (not (password == "" or repassword == "")):
            if (password == repassword):
                x = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password)
                if (not (x == None)):
                    feedbackCreate = database.create_user(username, password)
                    print(feedbackCreate)
                    if (not feedbackCreate):
                        print("error: couldn't create user")
                    elif (feedbackCreate == "unique"):
                        print("User already exists")
                    else:
                        registerFrame.pack_forget()
                        set_login()
                else:
                    print("The password needs atleast 8 letter. It must contain a small letter, a capital letter, and a number.")
            else:
                print("The passwords don't match")
        else:
            print("Please enter a password")
    else:
        print("Please enter a username")

       
            
def create_login(plattform, username, password, user_id):
    feedbackCreate = database.create_login(plattform, username, password, user_id)
    if (not feedbackCreate):
       print("error: couldn't create login")
    else:
        set_main()
        set_login_frame(feedbackCreate)

def delete_login(id):
    feedbackDelete = database.delete_login(id)
    if (not feedbackDelete):
        print("error: couldn't delete login")
    else:
        for child in informationFrame.winfo_children():
            child.destroy()
        set_main()
def edit_login(id, plattform, username, password):
    feedbackEdit = database.update_login(id, plattform, username, password)
    if (not feedbackEdit):
        print("error: couldn't update login")
    else: 
        set_main()
        set_login_frame(id)
        

def switch_login_register(switch):
    if switch == True:
        loginFrame.pack_forget()
        set_register()
    else:
        registerFrame.pack_forget()
        set_login()

def grid_information():
    informationFrame.pack_propagate(0)
    informationFrame.grid(pady=10, padx=(0,10),row=0, rowspan=3, column=1, columnspan=5, sticky='w')

def set_edit_login_frame(id):
    login = database.select_login(id)
    if (not login):
        print("error: id doesnn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattformEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Plattform Name")
        plattformEditInput.insert(0, login[1])
        plattformEditInput.pack(pady=10, padx=10)
        usernameEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Username")
        usernameEditInput.insert(0, login[2])
        usernameEditInput.pack(pady=10, padx=10)
        passwordEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Password")
        passwordEditInput.insert(0, login[3])
        passwordEditInput.pack(pady=10, padx=10)
        editButton = customtkinter.CTkButton(master=informationFrame, text="Edit", command= lambda : edit_login(id, plattformEditInput.get(), usernameEditInput.get(), passwordEditInput.get()))
        editButton.pack(pady=10, padx=10)
        grid_information() 
        

def set_login_frame(id):
    login = database.select_login(id)
    if (not login):
        print("error: id doesn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattform = customtkinter.CTkLabel(master=informationFrame, text=login[1])
        plattform.pack(pady=10,padx=10)
        username = customtkinter.CTkLabel(master=informationFrame, text=login[2])
        username.pack(pady=10,padx=10)
        password = customtkinter.CTkLabel(master=informationFrame, text=login[3])
        password.pack(pady=10, padx=10)
        editButton = customtkinter.CTkButton(master=informationFrame, text="Edit Login", command=lambda : set_edit_login_frame(id))
        editButton.pack(pady=10, padx=10)
        deleteButton = customtkinter.CTkButton(master=informationFrame, text="Delete Login", command=lambda : delete_login(id))
        deleteButton.pack(pady=10, padx=10)
        grid_information()

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
    register.bind("<Button-1>", lambda e: switch_login_register(True))

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
    register.bind("<Button-1>", lambda e: switch_login_register(False)) 

def set_main():
    loginFrame.pack_forget()
    registerFrame.pack_forget()
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.columnconfigure(1, weight=1)
    mainFrame.rowconfigure(1, weight=1)
    mainFrame.pack(pady=5, padx = 5, fill="both", expand=True)

    listFrame = customtkinter.CTkScrollableFrame(master=mainFrame, width=100, height=400)
    listFrame.grid(pady=(10,0), padx=10, row=0, column=0, sticky='w')

    addLoginButton = customtkinter.CTkButton(master=mainFrame, width=120, height=50, text="Create login", command=lambda : set_create_login_frame())
    addLoginButton.grid(pady=(0,10), padx=10, row=2, column=0, sticky='w')

    grid_information()

    userInfo = database.select_logins_by_user(loggedInUsername)
    if (not userInfo):
        print("No entries")
    else: 
        for i in range(len(userInfo)):
            frame = customtkinter.CTkFrame(master=listFrame)
            label = customtkinter.CTkLabel(master=frame, text=(userInfo[i])[1], font=("Roboto", 16), cursor="hand2")
            label.pack(pady=1,padx=1, fill="x")
            def make_lambda(x):
                return lambda e:set_login_frame(x)
            label.bind("<Button-1>", make_lambda(((userInfo[i])[0])))
            frame.pack(pady=2, padx=2, fill="x")
            

