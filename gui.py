import customtkinter
import database

root = customtkinter.CTk()
loginFrame = customtkinter.CTkFrame(master=root)
registerFrame = customtkinter.CTkFrame(master=root)
mainFrame = customtkinter.CTkFrame(master=root)
informationFrame = customtkinter.CTkFrame(master=mainFrame, width=550, height=500)

loggedInUsername = customtkinter.CTkFrame(master=mainFrame, width=550, height=500)

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
        set_main()
    else:
        print("Password wrong")
            

def switch_login_register(switch):
    if switch == True:
        loginFrame.pack_forget()
        set_register()
    else:
        registerFrame.pack_forget()
        set_login()

def grid_information():
    informationFrame.pack_propagate(0)
    informationFrame.grid(pady=10, padx= (0,10),row=0, rowspan=3, column=1, columnspan=5, sticky='w')

def set_login_frame(id):
    login = database.select_login(id)
    if (not login):
        print("error: id doesnn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattform = customtkinter.CTkLabel(master=informationFrame, text=login[1])
        plattform.pack(pady=10,padx=10)
        password = customtkinter.CTkLabel(master=informationFrame, text=login[2])
        password.pack(pady=10, padx=10)
        grid_information()
        
        
        print(login)

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

    login = customtkinter.CTkButton(master=registerFrame, text="Sign Up", command="dsf", width=200)
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

    addLoginButton = customtkinter.CTkButton(master=mainFrame, width=120, height=50, text="Create login")
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
            

