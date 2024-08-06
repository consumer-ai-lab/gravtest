import tkinter as tk
from tkinter import *
from tkinter import ttk
import localfolder_utility
import fetch_image
from tkhtmlview import HTMLLabel


class TestScreen(tk.Frame):
    q1 = None
    q2 = None
    q3 = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Specify Grid
        Grid.rowconfigure(self, 0)
        Grid.columnconfigure(self, 0, weight=1)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.rowconfigure(self, 2)

        '''
        WCL DISPLAY AND TIMER
        '''
        # Create Buttons

        topic_frame = Frame(self, bg="white")
        topic_frame.grid(row=0, column=0, sticky="NSEW")

        Grid.rowconfigure(topic_frame, 0, weight=0)
        Grid.columnconfigure(topic_frame, 0, weight=2)
        Grid.columnconfigure(topic_frame, 1, weight=1)
        Grid.columnconfigure(topic_frame, 2, weight=1)

        wcl_label = Label(topic_frame, text="WCL Recruitment Test",
                          font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        wcl_label.grid(row=0, column=0, sticky="NSEW")

        wcl_label = Label(topic_frame, textvariable=self.controller.reading_timer_state['reading_time_left'], font=(
            'Helvetica', 20, 'bold'), bg="white", fg="black", relief=SUNKEN, padx=5, pady=3)
        wcl_label.grid(row=0, column=1, sticky="NSEW")
        self.controller.reading_timer_label_object = wcl_label

        wcl_label = Frame(topic_frame, bg="black", padx=5, pady=3)
        wcl_label.grid(row=0, column=2, sticky="NSEW")

        Grid.columnconfigure(wcl_label, 1, weight=1)
        roll = Label(wcl_label, text="Roll Number: ",
                     font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        roll.grid(row=0, column=0, sticky="NSEW")

        roll_no = Label(wcl_label, textvariable=self.controller.app_data['username'],
                        font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        roll_no.grid(row=0, column=1, sticky="NSEW")

        name = Label(wcl_label, text="Name: ",
                     font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        name.grid(row=1, column=0, sticky="NSEW")

        name = Label(wcl_label, textvariable=self.controller.app_data['name'],
                     font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        name.grid(row=1, column=1, sticky="NSEW")

        '''
        fetching class method
        '''

        '''
        Questions
        '''

        question_frame = Frame(self, bg="white")
        question_frame.grid(row=1, column=0, sticky="NSEW")

        customed_style = ttk.Style()
        customed_style.configure('Custom.TNotebook.Tab', padding=[
                                 12, 12], font=('Helvetica', 12, 'bold'))
        customed_style.map("Custom.TNotebook", background=[
                           ("selected", "#0000FF")])

        ques_display = Frame(question_frame, bg="white")
        ques_display.pack(expand=True, fill="both", pady=3)

        tabControl = ttk.Notebook(ques_display, style='Custom.TNotebook')

        tab1 = tk.Frame(tabControl, bg="white")
        tab2 = tk.Frame(tabControl, bg="white")
        tab3 = tk.Frame(tabControl, bg="white")

        tabControl.add(tab1, text='Section 1: Microsoft Word (3 marks)      ')
        tabControl.add(tab2, text='Section 2: Microsoft Excel (4 marks)     ')
        tabControl.add(tab3, text='Section 3: Microsoft Powerpoint (3 marks)')
        tabControl.pack(expand=True, fill="both")

        '''
        Microsoft Word Section
        '''

        sec1 = Frame(tab1)
        sec1.grid(column=0, row=0, sticky="NSEW")

        Grid.rowconfigure(sec1, 0)
        Grid.rowconfigure(sec1, 1, weight=1)
        Grid.columnconfigure(sec1, 0, weight=1)
        Grid.columnconfigure(tab1, 0, weight=1)
        Grid.rowconfigure(tab1, 0, weight=1)

        l1 = Label(
            sec1, text="Section 1: Microsoft Word Skill Test (3 marks)", fg="black", font=('Helvetica 15 bold'),)
        l1.grid(column=0, row=0, padx=20, pady=5, sticky="NSEW")

        TestScreen.q1 = HTMLLabel(
            sec1, html=''' ''', bg="black", relief=SUNKEN)
        # q1.place(x=5,y=5)

        TestScreen.q1.grid(column=0, row=1, sticky="NSEW")

        scroll = tk.Scrollbar(sec1, orient='horizontal',
                              command=TestScreen.q1.xview)
        TestScreen.q1.configure(xscrollcommand=scroll.set)

        scroll.grid(column=0, row=2, sticky="NSEW")
        '''
        EXCEL SECTION
        '''

        sec2 = Frame(tab2)
        sec2.grid(column=0, row=0, sticky="NSEW")

        Grid.rowconfigure(sec2, 0)
        Grid.rowconfigure(sec2, 1, weight=1)
        Grid.columnconfigure(sec2, 0, weight=1)
        Grid.columnconfigure(tab2, 0, weight=1)
        Grid.rowconfigure(tab2, 0, weight=1)

        l2 = Label(
            sec2, text="Section 2: Microsoft Excel Skill Test (4 marks)", fg="black", font=('Helvetica 15 bold'),)
        l2.grid(column=0, row=0, padx=20, pady=5, sticky="NSEW")

        TestScreen.q2 = HTMLLabel(
            sec2, html=''' ''', bg="black", relief=SUNKEN)
        TestScreen.q2.grid(column=0, row=1, sticky="NSEW")

        scroll1 = tk.Scrollbar(sec2, orient='horizontal',
                               command=TestScreen.q2.xview)
        TestScreen.q2.configure(xscrollcommand=scroll1.set)

        scroll1.grid(column=0, row=2, sticky="NSEW")

        '''
        Powerpoint SECTION
        '''

        sec3 = Frame(tab3)
        sec3.grid(column=0, row=0, sticky="NSEW")

        Grid.rowconfigure(sec3, 0)
        Grid.rowconfigure(sec3, 1, weight=1)
        Grid.columnconfigure(sec3, 0, weight=1)
        Grid.columnconfigure(tab3, 0, weight=1)
        Grid.rowconfigure(tab3, 0, weight=1)

        l3 = Label(
            sec3, text="Section 3: Microsoft Powerpoint Skill Test (3 marks)", fg="black", font=('Helvetica 15 bold'),)
        l3.grid(column=0, row=0, padx=20, pady=5, sticky="NSEW")

        TestScreen.q3 = HTMLLabel(sec3, html=''' ''',
                                  bg="black", relief=SUNKEN)
        TestScreen.q3.grid(column=0, row=1, sticky="NSEW")

        scroll2 = tk.Scrollbar(sec3, orient='horizontal',
                               command=TestScreen.q3.xview)
        TestScreen.q3.configure(xscrollcommand=scroll2.set)

        scroll2.grid(column=0, row=2, sticky="NSEW")

        '''
        Start Solving
        '''

        submit_test_button = Button(self, text="Start Solving", command=lambda: self.controller.start_solving_method(
        ), padx=40, pady=10, bg="green", fg="white", relief=RAISED, font=('Helvetica 18 bold'), cursor="hand2")
        submit_test_button.grid(row=2, column=0, sticky="NSEW")
