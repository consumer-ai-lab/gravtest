import tkinter as tk
from tkinter import ttk
import login_screen
import start_screen
import test_screen
import speed_test_screen
import start_screen_typing_test
import submitted_test_screen
import solving_screen
import database_utility
import localfolder_utility
import time
import timer_utility
import keyboard
import network_handler_screen
import submit_only_screen
import window_handler
import threading
from dotenv import dotenv_values
import window_handler
import threading
import pymongo
import os
import sys
from config_module import config, db_client

mydb = db_client["myFirstDatabase"]


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        import ssl

        self.FONT1 = ("Verdana", 35)
        self.FONT2 = ("Verdana", 14)
        self.FONT3 = ("Verdana", 22)

        self.BACKEND_API_SECRET = config["BACKEND_API_SECRET"]

        # creating collection
        info = mydb["config-table"]
        config_info = info.find_one({"config_name": "ip"})
        self.QUESTION = info.find_one({"config_name": "typing_test"})["question"]
        self.BACKEND_URL = config_info["ip"]
        # print(self.BACKEND_URL)

        if config["UNDER_DEVELOPMENT"] == "TRUE":
            print("Application backend opening UNDER_DEVELOPEMENT")
            # self.BACKEND_URL = "http://localhost:5000"

        self.prev_state = ""
        self.current_state = "login_screen"

        # self.autosaver_active = True

        self.app_data = {
            "username": tk.StringVar(),
            "user_password": tk.StringVar(),
            "test_password": tk.StringVar(),
            "name": tk.StringVar(),
            "batch": tk.StringVar(),
            "name": tk.StringVar(),
            "token": "",
        }

        self.login_state = {
            "login_in_progress": False,
            "login_status": False,
            "login_status_text": tk.StringVar(),
        }

        self.start_test_state = {
            "start_test_in_progress": False,
            "start_test_status": False,
            "start_test_status_text": tk.StringVar(),
        }

        self.timer_state = {
            "local_elapsed_time_incrementer_active": True,
            "time_left": tk.StringVar(),
            "elapsed_time": 0,
            "counter": 0,
            "timer_ping_in_progress": False,
        }

        self.reading_timer_state = {
            "reading_local_elapsed_time_incrementer_active": True,
            "reading_time_left": tk.StringVar(),
            "reading_elapsed_time": 0,
            "reading_counter": 0,
            "reading_timer_ping_in_progress": False,
        }

        self.network_error_state = {
            "network_working_fine": True,
            "network_status": tk.StringVar(),
        }

        self.submit_only_screen_state = {
            "counter": 0,
            "submit_only_screen_ping_active": True,
            "submit_only_screen_ping_lock": False,
            "status": tk.StringVar(),
            "message": tk.StringVar(),
        }

        self.thread_list = []

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        self.frame_classes = [
            login_screen.LoginScreen,
            start_screen.StartScreen,
            start_screen_typing_test.StartScreenTypingTest,
            test_screen.TestScreen,
            solving_screen.SolvingScreen,
            speed_test_screen.SpeedTestScreen,
            submitted_test_screen.SubmittedTestScreen,
            network_handler_screen.NetworkHandlerScreen,
            submit_only_screen.SubmitOnlyScreen,
        ]

        # iterating through a tuple consisting
        # of the different page layouts
        for F in self.frame_classes:
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(login_screen.LoginScreen)

        # to display the current frame passed as
        # parameter

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login_method(self):
        print(self.app_data)
        database_utility.user_password_match(
            {
                "username": self.app_data["username"].get().strip(),
                "user_password": self.app_data["user_password"].get().strip(),
                "test_password": self.app_data["test_password"].get().strip(),
            },
            self,
        )

        # t = threading.Thread(target = window_handler.autosaver, args=(self.app_data['username'].get(), self))
        # self.thread_list.append(t)
        # t.start()

    def start_test_method(self):
        database_utility.update_start_time(self)

    def start_solving_method(self):
        result = database_utility.update_reading_submission_received(self)

        if result == "SUCCESS":
            self.prev_state = self.current_state
            self.current_state = "solving_screen"
            self.show_frame(solving_screen.SolvingScreen)
            self.reading_timer_state[
                "reading_local_elapsed_time_incrementer_active"
            ] = False

            self.timer_state["local_elapsed_time_incrementer_active"] = True
            timer_utility.local_elapsed_time_incrementer(self)
        else:
            """
            show a message box to indicate error
            """
            tk.messagebox.showerror(
                title="Network Error",
                message="Please check your internet connection and Try Again",
            )
            pass

    def submit_test_method(self):
        localfolder_utility.closeFiles(self)
        """
            send files to cloud
        """

        """
                            Submission not received even though elapsed time is exceeded
                            Send to Submit Only Screen
                            So that saved files can be sent to the cloud
        """

        self.prev_state = self.current_state
        self.current_state = "submit_only_screen"
        self.submit_only_screen_state["message"].set(
            "Submitting your test.......Please Wait"
        )
        self.show_frame(submit_only_screen.SubmitOnlyScreen)
        timer_utility.submit_only_screen_incrementer(self)
        self.reading_timer_state["reading_local_elapsed_time_incrementer_active"] = (
            False
        )
        self.timer_state["local_elapsed_time_incrementer_active"] = False

    def end_test_method(self):
        timer_utility.destroy_application(self)
        print("Test Ended")
        # exit()
        self.destroy()

    def __str__(self):
        output_str = "app_data:" + "\n"
        output_str += "username: " + self.app_data["username"].get() + "\n"
        output_str += "user_password: " + self.app_data["user_password"].get() + "\n"
        output_str += "test_password: " + self.app_data["test_password"].get() + "\n"
        output_str += "elapsed_time: " + str(self.timer_state["elapsed_time"]) + "\n"
        output_str += "token: " + str(self.app_data["token"]) + "\n"
        return output_str
