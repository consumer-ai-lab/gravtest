import tkinter as tk
from tkinter import *


class StartScreenTypingTest(tk.Frame):
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
1. The total duration of this test is 10 minutes.

2. Click the "Start Test" button to begin the test timer.

3. Type the given paragraph inside the text box as fast as possible.

4. The test will be automatically submitted once the time is up.

5. The test can also be submitted within 10 minutes by clicking the "Submit".""", font=('Helvetica 16 bold'), fg='black', bg="white", width="1360", padx="10", pady="10")
        msg.grid(row=2, column=0, sticky="NSEW")

        start_test_status_text = tk.Label(f1, textvariable=self.controller.start_test_state['start_test_status_text'],
                                          font=('Helvetica 25 bold'), padx="10", pady=1, bg="white")
        start_test_status_text.grid(row=3, column=0, sticky="NSEW")

        start_test_button = tk.Button(f1, text="Start Test", command=lambda: self.controller.start_test_method(
        ), padx=40, pady=1, bg="green", fg="white", relief=RAISED, font=('Helvetica 25 bold'), cursor="hand2")
        start_test_button.grid(
            row=4, column=0, sticky="NSEW", padx=200, pady=20)
