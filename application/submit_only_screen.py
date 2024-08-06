import tkinter as tk
from tkinter import *
# from tkhtmlview import HTMLLabel


class SubmitOnlyScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        frame= Frame(self,bg="black",relief= 'sunken')
        frame.pack(fill= BOTH,expand=True)
        
        f1= Frame(frame, relief= 'sunken', bg= "white")
        f1.pack(fill= BOTH, expand= True, padx= 100, pady=30)

        Grid.rowconfigure(f1,0)
        Grid.rowconfigure(f1,1,weight=1)
        Grid.rowconfigure(f1,2)
        Grid.columnconfigure(f1,0,weight=1)

        label= Label(f1, text= "Western Coalfields Limited (WCL) Test",
        font=('Helvetica 25 bold'),background="#004C99",fg='#ffffff',padx="20",pady='20')
        label.grid(row=0, column=0, sticky="NSEW", padx=50, pady=20)

        # pic=Frame(f1,background="white",width=120,height=120)
        # pic.pack(pady="15")
        

        msg2 = tk.Message( f1, textvariable= self.controller.submit_only_screen_state['message']
        ,font=('Helvetica 20 bold'),fg='black',padx="20",pady="10",bg="white",width="900")
        msg2.grid(row=1, column=0, sticky="NSEW", padx=50, pady=20)
        # msg2.pack(side=LEFT,padx="35")

        msg3 = tk.Message( f1, textvariable= self.controller.submit_only_screen_state['status'] ,font=('Helvetica 20 bold'),fg='black',padx="20",pady="10",bg="white",width="900")
        # msg3.pack(side=LEFT,padx="35")
        msg3.grid(row=2, column=0, sticky="NSEW", padx=50, pady=20)
