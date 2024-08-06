import os
import sys
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkhtmlview import HTMLLabel

CWD = os.getcwd()
if getattr(sys, 'frozen', False):
    CWD = sys._MEIPASS

wcl_logo_path = os.path.join(CWD, "data/assets/WCL3.png")

class LoginScreen(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        Grid.columnconfigure(self,0,weight=1)
        Grid.columnconfigure(self,1)
        Grid.rowconfigure(self,0,weight=1)

        f1=tk.Frame(self,background="#004C99")
        # f1.pack(side=LEFT,fill=BOTH,expand=True)
        f1.grid(row=0,column=0,sticky="NSEW")
        

        pic=tk.Frame(f1,width=200,height=200)
        pic.place(x=50,y=30)
        my_logo = HTMLLabel(pic, html=f"<img src='{str(wcl_logo_path)}'  width='150' height='198'/>", background="#004C99")
        my_logo.place(x=0,y=0)
        my_logo.pack()
        msg = tk.Message( f1, text = "Welcome to Western Coalfields Limited (WCL) Test",font = self.controller.FONT1,background="#004C99",fg='#ffffff')
        msg.pack(side=LEFT)

        f2=tk.Frame(self,bg="white",relief=RAISED,padx=50,pady=80,width=200)
        # f2.pack(side=RIGHT,fill="y")
        f2.grid(row=0,column=1,sticky="NSEW")


        
        heading_label = tk.Label(f2, text ="Login", font = self.controller.FONT1,bg='#ffffff')
        heading_label.grid(row = 0,columnspan = 2,padx = 40, pady = 30)

        username_label = tk.Label(f2, text ="Username:", font = self.controller.FONT2,bg='#ffffff')
        username_label.grid(row = 1, column = 0, padx = 2, pady = 2)
        
        username_entry = tk.Entry(f2, textvariable = self.controller.app_data['username'], font=self.controller.FONT2)
        username_entry.grid(row = 1, column = 1, padx = 2, pady = 2)

        user_password_label = tk.Label(f2, text ="User Password:", font = self.controller.FONT2,bg='#ffffff')
        user_password_label.grid(row = 2, column = 0, padx = 10, pady = 10)
        
        user_password_entry = tk.Entry(f2, textvariable = self.controller.app_data['user_password'], font=self.controller.FONT2, show='*')
        user_password_entry.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        test_password_label = tk.Label(f2, text ="Test Password:", font = self.controller.FONT2,bg='#ffffff')
        test_password_label.grid(row = 3, column = 0, padx = 10, pady = 10)
        
        test_password_entry = tk.Entry(f2, textvariable = self.controller.app_data['test_password'], font=self.controller.FONT2, show='*')
        test_password_entry.grid(row = 3, column = 1, padx = 10, pady = 20)        
        

        login_button = tk.Button(f2, text ="LOGIN",command = lambda : self.controller.login_method(),padx=40,pady=10,bg="green",fg="white",relief=RAISED,font="15",cursor="hand2")
        login_button.grid(row = 4, columnspan = 2, padx = 10, pady = 10)

        login_status_text_label = tk.Label(f2, textvariable=self.controller.login_state['login_status_text'], font = self.controller.FONT2,bg='#ffffff')
        login_status_text_label.grid(row = 5, columnspan = 2, padx = 10, pady = 10)

        
