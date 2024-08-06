import tkinter as tk
from tkinter import *
from tkinter import ttk
import localfolder_utility
from tkinter import messagebox
import fetch_image
from tkhtmlview import HTMLLabel


class SolvingScreen(tk.Frame):
    q1 = None
    q2 = None
    q3 = None

    
    currentTab = 0
        


    def ExitApplication(self):
        MsgBox = tk.messagebox.askquestion('Confirmation on Submission of Test',
                                           'Are you sure you want to submit the test?\nOnce submitted you cannot resume your test.',
                                           icon='question')
        if MsgBox == 'yes':
            self.controller.submit_test_method()
        else:
            pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Specify Grid

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        # Grid.columnconfigure(self, 1, weight=3)

        main_full_frame = Frame(self, bg="white")
        main_full_frame.grid(row=0, column=0, sticky="NSEW")

        Grid.columnconfigure(main_full_frame, 0, weight=1)

        Grid.rowconfigure(main_full_frame, 0, weight=0)
        Grid.rowconfigure(main_full_frame, 1, weight=3)
        Grid.rowconfigure(main_full_frame, 2, weight=1)

        '''
        WCL DISPLAY AND TIMER
        '''
        # Create Buttons

        topic_frame = Frame(main_full_frame, bg="white")
        topic_frame.grid(row=0, column=0, sticky="NSEW")

        Grid.rowconfigure(topic_frame, 0, weight=0)
        Grid.columnconfigure(topic_frame, 0, weight=1)
        Grid.columnconfigure(topic_frame, 1, weight=2)
        Grid.columnconfigure(topic_frame, 2, weight=2)

        wcl_label = Label(topic_frame, text="WCL Recruitment Test",
                          font=('Helvetica 12 bold'), bg="black", fg="white", padx=5, pady=3)
        wcl_label.grid(row=0, column=0, sticky="NSEW")

        wcl_label = Label(topic_frame, textvariable=self.controller.timer_state['time_left'], font=(
            'Helvetica', 20, 'bold'), bg="white", fg="black", relief=SUNKEN, padx=5, pady=3)
        wcl_label.grid(row=0, column=1, sticky="NSEW")
        self.controller.solving_timer_label_object = wcl_label

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
        Questions
        '''

        question_frame = Frame(main_full_frame, bg="white", relief=GROOVE)
        question_frame.grid(row=1, column=0, sticky="NSEW")

        Grid.columnconfigure(question_frame, 0, weight=1)
        # Grid.columnconfigure(question_frame, 1, weight=1)

        custom_style = ttk.Style()
        # custom_style.configure(
        #     'Custom.TNotebook.Tab',
        #     padding=[
        #         12,
        #         12
        #     ],
        #     font=('Helvetica', 12, 'bold'),
        #     tabposition='wn',
        # )

        custom_style = ttk.Style()
        custom_style.configure(
                'Custom.TNotebook',
    tabposition='wn',
    borderwidth=0,
    )
        custom_style.configure(
    'Custom.TNotebook.Tab',
    padding=[30, 10],
    font=('Helvetica', 12, 'bold'),
    background='white',
    foreground='black',
    borderwidth=0,
    )

        custom_style.map(
            "Custom.TNotebook",
            background=[
                (
                    "selected",
                    "#0000FF"
                )
            ]
        )

        def on_tab_selected(event):
            selected_tab = event.widget.select()
            selected_tab_index = event.widget.index(selected_tab)
            tab_text = event.widget.tab(selected_tab, "text")
            print(tab_text, selected_tab_index)

            # update text of current question
            current_question_label.config(text=questionsList[selected_tab_index][0])

            # update solve button command
            tk.Button(submission_frame, text="Solve", command=questionsList[selected_tab_index][1],
                    padx=20, pady=10, bg="blue", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
                    cursor="hand2").grid(
                column=2,
                row=2,
                padx=3,
                pady=3)

        ques_display = Frame(question_frame, bg="white")
        ques_display.pack(expand=True, fill="both")

        tabControl = ttk.Notebook(ques_display, style='Custom.TNotebook')

        tab1 = tk.Frame(tabControl, bg="white")
        tab2 = tk.Frame(tabControl, bg="white")
        tab3 = tk.Frame(tabControl, bg="white")

        tabControl.bind("<<NotebookTabChanged>>", on_tab_selected)

        tabControl.add(tab1, text='Section 1: Microsoft Word (3 marks)     ', compound=LEFT)
        tabControl.add(tab2, text='Section 2: Microsoft Excel (4 marks)     ', compound=LEFT)

        tabControl.add(tab3, text='Section 3: Microsoft Powerpoint (3 marks)', compound=LEFT)
        tabControl.pack(expand=True, fill="both")

        questionsList = [
        ["Section 1: Microsoft Word Skill Test (3 marks)", lambda: localfolder_utility.openDocFile(self.controller)],
        ["Section 2: Microsoft Excel Skill Test (4 marks)", lambda: localfolder_utility.openExcelFile(self.controller)],
        ["Section 3: Microsoft Powerpoint Skill Test (3 marks)", lambda: localfolder_utility.openPptFile(self.controller)]
        ]

        tabs = [tab1, tab2, tab3]

        def nextQuestion():
            self.currentTab = (self.currentTab + 1) % 3
            tabControl.select(tabs[self.currentTab])

            # update text of current question
            current_question_label.config(text=questionsList[self.currentTab][0])

            # update solve button command
            tk.Button(submission_frame, text="Solve", command=questionsList[self.currentTab][1],
                    padx=20, pady=10, bg="blue", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
                    cursor="hand2").grid(
                column=2,
                row=2,
                padx=3,
                pady=3)
            

        def previousQuestion():
            self.currentTab = (self.currentTab - 1) % 3
            tabControl.select(tabs[self.currentTab])

            # update text of current question
            current_question_label.config(text=questionsList[self.currentTab][0])

            # update solve button command
            tk.Button(submission_frame, text="Solve", command=questionsList[self.currentTab][1],
                    padx=20, pady=10, bg="blue", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
                    cursor="hand2").grid(
                column=2,
                row=2,
                padx=3,
                pady=3)


        '''
        Microsoft Word Section
        '''

        sec1 = Frame(tab1)
        sec1.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)

        Grid.rowconfigure(sec1, 0)
        Grid.rowconfigure(sec1, 1, weight=1)
        Grid.columnconfigure(sec1, 0, weight=1)
        Grid.columnconfigure(tab1, 0, weight=1)
        Grid.rowconfigure(tab1, 0, weight=1)

        l1 = Label(
            sec1, text="Section 1: Microsoft Word Skill Test (3 marks)", fg="black", font=('Helvetica 15 bold'),
            bg="white")
        l1.grid(column=0, row=0, sticky="NSEW")

        SolvingScreen.q1 = HTMLLabel(
            sec1, html=''' ''', bg="black", relief=SUNKEN)
        # q1.place(x=5,y=5)

        SolvingScreen.q1.grid(column=0, row=1, sticky="NSEW")

        scroll = tk.Scrollbar(sec1, orient='horizontal',
                              command=SolvingScreen.q1.xview)
        SolvingScreen.q1.configure(xscrollcommand=scroll.set)

        scroll.grid(column=0, row=2, sticky="NSEW")

        '''
        EXCEL SECTION
        '''

        sec2 = Frame(tab2)
        sec2.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)
        Grid.rowconfigure(sec2, 0)
        Grid.rowconfigure(sec2, 1, weight=1)
        Grid.columnconfigure(sec2, 0, weight=1)
        Grid.columnconfigure(tab2, 0, weight=1)
        Grid.rowconfigure(tab2, 0, weight=1)

        l2 = Label(
            sec2, text="Section 2: Microsoft Excel Skill Test (4 marks)", fg="black", font=('Helvetica 15 bold'),
            bg="white")
        l2.grid(column=0, row=0, sticky="NSEW")

        SolvingScreen.q2 = HTMLLabel(
            sec2, html=''' ''', bg="black", relief=SUNKEN)
        SolvingScreen.q2.grid(column=0, row=1, sticky="NSEW")
        scroll1 = tk.Scrollbar(sec2, orient='horizontal',
                               command=SolvingScreen.q2.xview)
        SolvingScreen.q2.configure(xscrollcommand=scroll1.set)

        scroll1.grid(column=0, row=2, sticky="NSEW")

        '''
        Powerpoint SECTION
        '''

        sec3 = Frame(tab3)
        sec3.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)

        Grid.rowconfigure(sec3, 0)
        Grid.rowconfigure(sec3, 1, weight=1)
        Grid.columnconfigure(sec3, 0, weight=1)
        Grid.columnconfigure(tab3, 0, weight=1)
        Grid.rowconfigure(tab3, 0, weight=1)

        l3 = Label(
            sec3, text="Section 3: Microsoft Powerpoint Skill Test (3 marks)", fg="black", font=('Helvetica 15 bold'),
            bg="white")
        l3.grid(column=0, row=0, sticky="NSEW")

        SolvingScreen.q3 = HTMLLabel(sec3, html=''' ''',
                                     bg="black", relief=SUNKEN)
        SolvingScreen.q3.grid(column=0, row=1, sticky="NSEW")

        scroll2 = tk.Scrollbar(sec3, orient='horizontal',
                               command=SolvingScreen.q3.xview)
        SolvingScreen.q3.configure(xscrollcommand=scroll2.set)

        scroll2.grid(column=0, row=2, sticky="NSEW")

        '''
        Submission
        '''

        submission_frame = Frame(main_full_frame, bg="white")
        submission_frame.grid(row=2, column=0, sticky="NSEW")

        Grid.rowconfigure(submission_frame, 0, weight=0)
        Grid.columnconfigure(submission_frame, 0, weight=1)
        Grid.columnconfigure(submission_frame, 1, weight=1)
        Grid.columnconfigure(submission_frame, 2, weight=1)
        Grid.columnconfigure(submission_frame, 3, weight=1)

        s_label = tk.Label(submission_frame, text="Submission",
                           font=('Helvetica 15 bold'), bg="black", fg="white", padx=5, pady=3)
        s_label.grid(row=0, columnspan=4, sticky="NSEW", ipady=3, pady=5)

        
        submit_test_button = tk.Button(submission_frame, text="Final Submit", command=self.ExitApplication,
                                       cursor="hand2", padx=20, pady=10, bg="green", fg="white", relief=RAISED,
                                       font=('Helvetica 15 bold'))
        submit_test_button.grid(column=0,
                                columnspan=1,
                                row=2,
                                padx=10,
                                pady=10
                                )


        go_to_previous_question_button = tk.Button(
            submission_frame, 
            text="Previous Question",
            cursor="hand2", padx=20, pady=10, bg="black", fg="white",
            relief=RAISED,
            font=('Helvetica 15 bold'),
            command=previousQuestion
            )

        go_to_previous_question_button.grid(column=1,
                                            row=2,
                                            padx=10,
                                            pady=10
                                            )
        
        

        current_question_label = tk.Label(
            submission_frame, text=questionsList[self.currentTab][0], font=('Helvetica 15 bold'), bg="white")
        current_question_label.grid(column=2,
                                    row=1,
                                    padx=10,
                                    pady=10
                                    )
        tk.Button(submission_frame, text="Solve", command=questionsList[self.currentTab][1],
                    padx=20, pady=10, bg="blue", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
                    cursor="hand2").grid(
                column=2,
                row=2,
                padx=3,
                pady=3)


        go_to_next_question_button = tk.Button(
            submission_frame,
            text="Next Question",
            cursor="hand2", padx=20, pady=10, bg="black", fg="white",
            relief=RAISED,
            font=('Helvetica 15 bold'),
            command=nextQuestion
            )
        
        go_to_next_question_button.grid(column=3,
                                        row=2,
                                        padx=10,
                                        pady=10
                                        )



        # tk.Label(submission_frame, text="Section 1: Microsoft Word", bg="white", font=('Helvetica 15 bold')).grid(
        #     column=0,
        #     row=1,
        #     padx=3,
        #     pady=3)
        # tk.Button(submission_frame, text="Solve", command=lambda: localfolder_utility.openDocFile(self.controller),
        #           padx=20, pady=10, bg="black", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
        #           cursor="hand2").grid(
        #     column=1,
        #     row=1,
        #     padx=3,
        #     pady=3)
        # tk.Label(submission_frame, text="Section 2: Microsoft Excel", bg="white", font=('Helvetica 15 bold')).grid(
        #     column=2,
        #     row=1,
        #     padx=3,
        #     pady=3)
        # tk.Button(submission_frame, text="Solve", command=lambda: localfolder_utility.openExcelFile(self.controller),
        #           padx=20, pady=10, bg="black", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
        #           cursor="hand2").grid(
        #     column=3,
        #     row=1,
        #     padx=3,
        #     pady=3)
        # tk.Label(submission_frame, text="Section 3: Microsoft Powerpoint", bg="white", font=('Helvetica 15 bold')).grid(
        #     column=0,
        #     row=2,
        #     padx=3,
        #     pady=3
        # )
        # tk.Button(submission_frame, text="Solve", command=lambda: localfolder_utility.openPptFile(self.controller),
        #           padx=20, pady=10, bg="black", fg="white", relief=RAISED, font=('Helvetica 15 bold'),
        #           cursor="hand2").grid(column=1,
        #                                row=2,
        #                                padx=3,
        #                                pady=3
        #                                )
        # submit_test_button = tk.Button(submission_frame, text="Submit Test", command=self.ExitApplication,
        #                                cursor="hand2", padx=20, pady=10, bg="green", fg="white", relief=RAISED,
        #                                font=('Helvetica 15 bold'))
        # submit_test_button.grid(column=2,
        #                         columnspan=2,
        #                         row=2,
        #                         padx=10,
        #                         pady=10
        #                         )

        # main_right_frame = Frame(self, bg="white")
        # main_right_frame.grid(row=0, column=1, sticky="NSEW")
        #
        # # sub_frame = Frame(main_right_frame, bg="white")
        # # sub_frame.grid(row=0, column=1, sticky="NSEW")
        #
        # Grid.rowconfigure(main_right_frame, 0, weight=1)
        # Grid.columnconfigure(main_right_frame, 0, weight=1)
        # tk.Label(main_right_frame,
        #          text="Please click on Solve Button to open Microsoft Word, Powerpoint and Excel.\n Your screen will be displayed here.",
        #          font=('Helvetica 10 bold'), bg="white").grid(
        #     column=0,
        #     row=0,
        #     sticky="NSEW", ipadx="200", ipady="300")

# lambda : self.controller.submit_test_method()
