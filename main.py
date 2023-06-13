import customtkinter

root = customtkinter.CTk()
loginFrame = customtkinter.CTkFrame(master=root)
registerFrame = customtkinter.CTkFrame(master=root)

def init():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root.geometry("700x500")
    root.title("PassVault")
    root.resizable(False, False)
    root.iconbitmap("logo.ico")
    set_login()



def switch_login_register(switch):
    if switch == True:
        loginFrame.pack_forget()
        set_register()
    else:
        registerFrame.pack_forget()
        set_login()

def set_login():
    loginFrame.pack(pady=90, padx=210, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=loginFrame, text="Login", font=("Roboto", 24))
    label.pack(pady=(55, 20), padx=10)

    username = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Username", width=200)
    username.pack(pady=(12,5), padx=10)

    password = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Password", show="*", width=200)
    password.pack(pady=(5,12), padx=10)

    login = customtkinter.CTkButton(master=loginFrame, text="Login", command="dsf", width=200)
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

init()

root.mainloop()