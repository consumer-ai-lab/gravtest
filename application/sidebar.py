import tkinter as tk
from tkinter import *
from tkinter import ttk
import localfolder_utility
from tkinter import messagebox
import fetch_image
from tkhtmlview import HTMLLabel


class ScreenWithSidebar(tk.Frame):
    q1 = None
    q2 = None
    q3 = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Frame.__init__(self, parent)

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)


        # create sidebar at left side
        self.sidebar = tk.Frame(self, bg='white', width=200, height=500, relief='sunken', borderwidth=2)

        self.sidebar.grid(row=0, column=0, sticky='ns')

        # create a main frame
        self.main = tk.Frame(self, bg='white', width=500, height=500, relief='sunken', borderwidth=2)

        self.main.grid(row=0, column=1, sticky='nsew')

        # create a label for the sidebar

        self.sidebar_label = tk.Label(self.sidebar, text="Sidebar", bg='white', font=('Helvetica', 18, 'bold'))

        self.sidebar_label.pack(side='top', fill='x')

        # create a button for the sidebar
        
        
