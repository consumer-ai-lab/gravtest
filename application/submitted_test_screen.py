import tkinter as tk
from tkinter import *
from tkhtmlview import HTMLLabel
import os
import sys

CWD = os.getcwd()
if getattr(sys, 'frozen', False):
    CWD = sys._MEIPASS

submitted_logo_path = os.path.join(CWD, "data/assets/submittedIcon.png")

class SubmittedTestScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
       
        # Add a frame to set the size of the window
        frame= Frame(self,bg="black",relief= 'sunken')
        frame.pack(fill= BOTH,expand=True)
        
        f1= Frame(frame, relief= 'sunken', bg= "white")
        f1.pack(fill= BOTH, expand= True, padx= 100, pady=30)

            
        # Add a label widget
        label= Label(f1, text= "Western Coalfields Limited (WCL) Test",
        font=('Helvetica 25 bold'),background="#004C99",fg='#ffffff',padx="20",pady='20')
        label.pack(pady= 2,fill='x')

        pic=Frame(f1,background="white",width=120,height=120)
        pic.pack(pady="15")
    
        success_logo = HTMLLabel(pic, html=f"""
            <img src='{str(submitted_logo_path)}' width="120" height="120" style="background-color:white" >
            """)
        success_logo.place(x=0,y=0)

        label1= Label(f1, text= "Thanks!",
        font=('Helvetica 35 bold'),background="white",fg='green',padx="20",pady='20')
        label1.pack(pady="15")

   
        msg2 = tk.Message( f1, text = "Your Test has been successfully Submitted.\n\n"+
        "Thank you for taking the test.\nYour Results would be communicated to you further.\n\n"+
        "Please click on Close Test Button."
        ,font=('Helvetica 20 bold'),fg='black',padx="20",pady="10",bg="white",width="900")
        msg2.pack(side=LEFT,padx="35")

        end_test_button = tk.Button(f1, text ="Close Test",command = lambda : self.controller.end_test_method(),padx=40,pady=10,bg="black",fg="white",relief=RAISED, font=('Helvetica 18 bold'), cursor="hand2")
        end_test_button.pack(side=BOTTOM,padx=35,pady = 20)
