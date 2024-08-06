import tkinter as tk
from tkinter import *
from tkinter import ttk
import localfolder_utility
from tkinter import messagebox
import fetch_image
from tkhtmlview import HTMLLabel
import time
import threading
import timer_utility

TOTAL_WRITING_TIME = 10 * 60  # seconds


class SpeedTestScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.timer = tk.StringVar()

        self.running_test = False
        self.counter = 0

        self.mins = "10"
        self.secs = "00"
        self.final_wpm = 0

        self.question = controller.QUESTION

        self.timer.set(f"{self.mins}:{self.secs}")

        def time_remaining_popup(controller):
            messagebox = tk.messagebox.askokcancel(
                "ALERT!!!!!!", "2 mins are remaining!", icon="warning"
            )

        # Specify Grid

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        # Grid.columnconfigure(self, 1, weight=3)

        # main_full_frame = Frame(self, bg="white")
        # main_full_frame.grid(row=0, column=0, sticky="NSEW")

        Grid.columnconfigure(self, 0, weight=1)

        Grid.rowconfigure(self, 0, weight=0)
        Grid.rowconfigure(self, 1, weight=4)
        Grid.rowconfigure(self, 2, weight=1)

        """
        WCL DISPLAY AND TIMER
        """
        # Create Buttons

        topic_frame = Frame(self, bg="white")
        topic_frame.grid(row=0, column=0, sticky="NSEW")

        Grid.rowconfigure(topic_frame, 0, weight=0)
        Grid.columnconfigure(topic_frame, 0, weight=1)
        Grid.columnconfigure(topic_frame, 1, weight=2)
        Grid.columnconfigure(topic_frame, 2, weight=2)

        wcl_label = Label(
            topic_frame,
            text="WCL Recruitment Test",
            font=("Helvetica 12 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        wcl_label.grid(row=0, column=0, sticky="NSEW")

        wcl_label = Label(
            topic_frame,
            textvariable=self.controller.timer_state["time_left"],
            font=("Helvetica", 20, "bold"),
            bg="black",
            fg="black",
        )
        wcl_label.grid(row=0, column=1, sticky="NSEW")
        self.controller.solving_timer_label_object = wcl_label

        wcl_label = Frame(topic_frame, bg="black", padx=5, pady=3)
        wcl_label.grid(row=0, column=2, sticky="NSEW")

        Grid.columnconfigure(wcl_label, 1, weight=1)
        roll = Label(
            wcl_label,
            text="Roll Number: ",
            font=("Helvetica 12 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        roll.grid(row=0, column=0, sticky="NSEW")

        roll_no = Label(
            wcl_label,
            textvariable=self.controller.app_data["username"],
            font=("Helvetica 12 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        roll_no.grid(row=0, column=1, sticky="NSEW")

        name = Label(
            wcl_label,
            text="Name: ",
            font=("Helvetica 12 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        name.grid(row=1, column=0, sticky="NSEW")

        name = Label(
            wcl_label,
            textvariable=self.controller.app_data["name"],
            font=("Helvetica 12 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        name.grid(row=1, column=1, sticky="NSEW")

        """
        QUESTION DISPLAY
        """

        question_frame = Frame(self, bg="white")
        question_frame.grid(row=1, column=0, sticky="NSEW")

        Grid.rowconfigure(question_frame, 0, weight=1)
        Grid.columnconfigure(question_frame, 0, weight=1)
        Grid.columnconfigure(question_frame, 1, weight=1)

        question_panel = Frame(question_frame, bg="white")
        question_panel.grid(row=0, column=0, sticky="NSEW")

        text_box_panel = Frame(question_frame, bg="black")
        text_box_panel.grid(row=0, column=1, sticky="NSEW")

        Grid.columnconfigure(question_panel, 0, weight=1)
        Grid.columnconfigure(text_box_panel, 0, weight=1)

        question_label = Label(
            question_panel,
            text="Question:",
            font=("Helvetica 15 bold"),
            bg="#004C99",
            fg="white",
            padx=5,
            pady=3,
        )
        question_label.grid(row=0, column=0, sticky="NSEW")

        question_text = HTMLLabel(
            question_panel,
            html=f"""<h3>Write this paragraph in the text box.</h3>
                                  <p>
                                  {self.question}
                                  </p>
                                  """,
            font=("Helvetica 12"),
            bg="white",
            fg="black",
            padx=5,
            pady=3,
        )
        question_text.grid(row=1, column=0, sticky="NSEW")

        Grid.rowconfigure(question_panel, 0, weight=1)
        Grid.rowconfigure(question_panel, 1, weight=10)

        text_box_label = Label(
            text_box_panel,
            text="Type here:",
            font=("Helvetica 15 bold"),
            bg="#004C99",
            fg="white",
            padx=5,
            pady=3,
        )
        text_box_label.grid(row=0, column=0, sticky="NSEW")

        self.text_box = Text(
            text_box_panel,
            font=("Helvetica 12"),
            bg="white",
            fg="black",
            padx=5,
            pady=3,
        )
        self.text_box.grid(row=1, column=0, sticky="NSEW")
        self.text_box.bind("<KeyPress>", self.check_text)

        Grid.rowconfigure(text_box_panel, 0, weight=1)
        Grid.rowconfigure(text_box_panel, 1, weight=10)
        # self.text_box.config(state="disabled")

        """
        Submission
        """

        submission_frame = Frame(self, bg="white")
        submission_frame.grid(row=2, column=0, sticky="NSEW")

        # create two rows, one row will have question name in center and second row will have a submit button, a solve button and timer

        Grid.rowconfigure(submission_frame, index=0, weight=0)
        Grid.columnconfigure(submission_frame, 0, weight=1)
        Grid.columnconfigure(submission_frame, 1, weight=1)

        s_label = tk.Label(
            submission_frame,
            text="Typing Speed Test",
            font=("Helvetica 15 bold"),
            bg="black",
            fg="white",
            padx=5,
            pady=3,
        )
        s_label.grid(row=0, columnspan=4, sticky="NSEW", ipady=3, pady=5)

        timer_label = tk.Label(
            submission_frame,
            textvariable=self.timer,
            padx=20,
            pady=10,
            bg="black",
            fg="white",
            relief=RAISED,
            font=("Helvetica 15 bold"),
        )
        timer_label.grid(column=0, columnspan=1, row=1, padx=3, pady=3)

        self.submit_button = tk.Button(
            submission_frame,
            text="Submit",
            command=lambda: self.ExitApplication(),
            padx=20,
            pady=10,
            bg="black",
            fg="white",
            relief=RAISED,
            font=("Helvetica 15 bold"),
            cursor="hand2",
        )
        self.submit_button.grid(column=1, columnspan=1, row=1, padx=3, pady=3)

    def santize_text(self, text: str):
        return " ".join([x.strip() for x in text.strip().split("\n")])

    def check_text(self, event):
        if self.running_test:
            self.controller.input_text = self.text_box.get(1.0, "end-1c") + event.char
            self.controller.question = self.santize_text(self.question)
            if self.text_box.get(1.0, "end-1c") + event.char == self.santize_text(
                self.question
            ):
                self.controller.wpm = self.final_wpm
                return
            self.text_box.config(foreground="black")
        else:
            if event.char.isalpha():
                self.start_test()

    def calculate_wpm(self):
        wpms = []
        for word in self.text_box.get(1.0, "end-1c").split(" "):
            if word in self.santize_text(self.question) and word != "":
                wpms.append(word)
        self.controller.wpm_normal = len(" ".join(wpms)) / self.counter * 60 / 5
        return (len(" ".join(wpms)) / self.counter * 60 / 5) * (len(wpms) / 300)

    def countdown(self):
        # print(self.mins, self.secs)
        if int(self.mins) > 0 or int(self.secs) > 0:
            if int(self.secs) > 0:
                self.secs = "{:02d}".format(int(self.secs) - 1)
            elif int(self.mins) > 0 and int(self.secs) == 0:
                self.mins = str(int(self.mins) - 1)
                self.secs = str(59)
        else:
            self.controller.prev_state = self.controller.current_state
            self.controller.current_state = "submit_only_screen"
            self.controller.submit_only_screen_state["message"].set(
                "Test Time Is Over.......Submitting the test, Please Wait"
            )
            self.controller.show_frame(
                timer_utility.submit_only_screen.SubmitOnlyScreen
            )
            timer_utility.submit_only_screen_incrementer(self.controller)
            self.controller.timer_state["local_elapsed_time_incrementer_active"] = False
            return

        self.timer.set(f"{self.mins}:{self.secs}")
        self.controller.after(1000, self.countdown)

    def time_thread(self):
        while self.running_test:
            if self.counter + 120 == TOTAL_WRITING_TIME:
                self.time_remaining_popup(self)
            time.sleep(1)
            self.counter += 1
            wpm = self.calculate_wpm()
            self.final_wpm = wpm
            self.controller.wpm = wpm
            self.controller.time = self.counter

    def start_test(self):
        if not self.running_test:
            self.running_test = True
            t = threading.Thread(target=self.time_thread)
            t.start()
            self.countdown()
            # self.text_box.config(state="normal")

    def ExitApplication(self):
        MsgBox = tk.messagebox.askquestion(
            "Confirmation on Submission of Test",
            "Are you sure you want to submit the test?\nOnce submitted you cannot resume your test.",
            icon="question",
        )
        if MsgBox == "yes":
            self.running_test = False
            self.controller.submit_test_method()
        else:
            pass
