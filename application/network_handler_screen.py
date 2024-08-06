import tkinter as tk
from tkinter import *
from tkinter import ttk
import localfolder_utility
from tkhtmlview import HTMLLabel


class NetworkHandlerScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller


        topic_frame = Frame(self, bg="#FFFF99",width=600, height=700,padx="30",pady="10")
        topic_frame.grid(row=0, column=0, sticky="NSEW",padx="300",pady="80")
       
        
        pic=Frame(topic_frame,width=200,height=200,background="#FFFF99")
        pic.pack(side=TOP)
        my_logo = HTMLLabel(pic, html="""
            <img src="data/assets/network_error.png" width="195" height="195" style="background-color:#FFFF99"/>
            """,bg="#FFFF99")
        my_logo.place(x=0,y=0)

        error_label = Label(topic_frame, text="Network Error \nPlease check your Internet Connection.",
                          font=self.controller.FONT1, fg="black",bg="#FFFF99", padx="5", pady="10")
        error_label.pack(side=TOP)


        label_one = Label(self, textvariable=controller.network_error_state['network_status'],
        font=80, fg="black", padx=5, pady=3)
        label_one.grid(row=1, column=0, sticky="NSEW",padx="220",pady="50")


        # Not Required as of now, but let it be present, will see if needed later
        label_two = Label(self, text="",
                          font=80, fg="black", padx=5, pady=3)
        label_two.grid(row=2, column=0, sticky="NSEW",padx="220",pady="50")
