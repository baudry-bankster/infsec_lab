from app.tools import registration, full_auth

import tkinter as tk
from tkinter.messagebox import showinfo

class App(tk.Tk):

    # def app_registration(self):
    #     self.user
    def __init__(self):
        super().__init__()

        
        
    
        #configure the root window
        self.title = 'User'
        self.geometry('500x200')

        #labels
        self.lbl_username = tk.Label(self, text='Username')
        self.lbl_password = tk.Label(self, text='Password')


        #Entries
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self)


        #functions
        def app_registration():
            username = self.entry_username.get()
            password = self.entry_password.get()
            registration(username, password)


        def app_auth():
            username = self.entry_username.get()
            password = self.entry_password.get()
            full_auth(username, password)


        #Buttons
        self.btn_signup = tk.Button(self, text='SignUp', command= app_registration)
        self.btn_signin = tk.Button(self, text='SignIn', command=app_auth)


        #pack
        self.lbl_username.pack()
        self.entry_username.pack()
        self.lbl_password.pack()
        self.entry_password.pack()
        self.btn_signup.pack()
        self.btn_signin.pack()


            



if __name__  == '__main__':
    app = App()
    app.mainloop()

