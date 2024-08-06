import tkinter as tk
from tkinter import *


class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Add a frame to set the size of the window
        frame = Frame(self, bg="#DCDCDC", relief=SUNKEN)
        frame.pack(fill=BOTH, expand=True)

        Grid.rowconfigure(frame, 0)
        Grid.columnconfigure(frame, 0, weight=1)

        f1 = Frame(frame, relief=SUNKEN, bg="white")
        f1.grid(row=0, column=0, sticky="NSEW")

        Grid.rowconfigure(f1, 0)
        Grid.columnconfigure(f1, 0, weight=1)

        Grid.rowconfigure(f1, 1)
        Grid.rowconfigure(f1, 2)
        Grid.rowconfigure(f1, 3)
        Grid.rowconfigure(f1, 4)

        # slot= Label(f1, textvariable= controller.app_data["batch"],
        # font=('Helvetica 18 bold'),padx="10",pady="10",bg="#004C99",fg="white")
        # slot.grid(row=0, column=0, sticky="NSEW")

        top_bar = Frame(f1)
        top_bar.grid(row=0, column=0, sticky="NSEW")
        Grid.columnconfigure(top_bar, 0)
        Grid.columnconfigure(top_bar, 1, weight=1)
        Grid.columnconfigure(top_bar, 2)
        Grid.columnconfigure(top_bar, 3, weight=1)
        Grid.columnconfigure(top_bar, 4)
        Grid.columnconfigure(top_bar, 5, weight=1)

        slot = Label(top_bar, text="Slot Time: ",
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=0, sticky="NSEW")

        slot = Label(top_bar, textvariable=controller.app_data["batch"],
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=1, sticky="NSEW")

        slot = Label(top_bar, text="Roll Number: ",
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=2, sticky="NSEW")

        slot = Label(top_bar, textvariable=controller.app_data["username"],
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=3, sticky="NSEW")

        slot = Label(top_bar, text="Candidate Name: ",
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=4, sticky="NSEW")

        slot = Label(top_bar, textvariable=controller.app_data["name"],
                     font=('Helvetica 18 bold'), bg="#004C99", fg="white", padx="10", pady="10")
        slot.grid(row=0, column=5, sticky="NSEW")

        # Add a label widget
        label = Label(f1, text="Instructions for the Test",
                      font=('Helvetica 25 bold'), padx="10", bg="white")
        label.grid(row=1, column=0, sticky="NSEW")

        msg = tk.Message(f1, text="""
1. The total duration of this test is 30 minutes, and it carries a maximum of 10 marks. The test consists of three sections:
\ta. Section 1: Microsoft Word Skill Test - 3 marks
\tb. Section 2: Microsoft Excel Skill Test - 4 marks
\tc. Section 3: Microsoft PowerPoint Skill Test - 3 marks

2. You will be given 5 minutes to read the question paper. Click the "Start Solving" button to begin the test timer.

3. You can navigate through the questions using the "Previous Question" and "Next Question" buttons, as well as the Question Palette displayed on the left side of the screen.

4. After answering every question, remember to save the file by using "Ctrl+S" or the save button. 

5. The test must be submitted within 30 minutes by clicking the "Submit Test" button for final submission. 

6. If not done so, the test will be automatically be submitted once the time is up with all the questions saved by you.

7. Please ensure that you submit the test only when you have finished the paper. Once you submit the test, you will not be able to return to it.

8. Please ensure that you have saved answer of each question before final submission.""", font=('Helvetica 16 bold'), fg='black', bg="white", width="1360", padx="10", pady="10")
        msg.grid(row=2, column=0, sticky="NSEW")

        start_test_status_text = tk.Label(f1, textvariable=self.controller.start_test_state['start_test_status_text'],
                                          font=('Helvetica 25 bold'), padx="10",pady=1, bg="white")
        start_test_status_text.grid(row=3, column=0, sticky="NSEW")

        start_test_button = tk.Button(f1, text="Start Test", command=lambda: self.controller.start_test_method(
        ), padx=40, pady=1, bg="green", fg="white", relief=RAISED, font=('Helvetica 25 bold'), cursor="hand2")
        start_test_button.grid(
            row=4, column=0, sticky="NSEW", padx=200, pady=20)
        
    