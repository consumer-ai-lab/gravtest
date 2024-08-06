import threading
import datetime
import keyboard
import requests
import json
import network_handler_screen
import network_handler_utility
import database_utility
import solving_screen
import submitted_test_screen
import localfolder_utility
import submit_only_screen
import final_submission
import time
import os
from config_module import db_client
import tkinter as tk
from tkinter import messagebox

mydb = db_client['myFirstDatabase']
info = mydb["config-table"]

time_record = info.find_one({"config_name":"time"})

PING_INTERVAL = time_record["PING_INTERVAL"]
TOTAL_WRITING_TIME = time_record["TOTAL_WRITING_TIME"]
TOTAL_READING_TIME = time_record["READING_TIME"]


def ColorFlasher(label_object, elapsed_time, cutoff):
    if elapsed_time >= cutoff:
        if elapsed_time % 2 == 0:
            label_object.config(bg="red")
            label_object.config(fg="white")
        else:
            label_object.config(bg="white")
            label_object.config(fg="black")


def ping_elapsed_time(controller, seconds_elapsed):
    # print("pinged start")
    def api_thread_function():
        api_url = controller.BACKEND_URL+'/api/userdata/update_elapsed_time'

        data = json.dumps({
            'username': controller.app_data['username'].get(),
            'elapsed_time': seconds_elapsed
        })
        headers = {
            "Content-Type": "application/json"
        }

        result = False
        response_data = 0
        response = None

        try:
            headers = {
                "Content-Type": "application/json",
                "token": controller.app_data["token"],
                "apikey": controller.BACKEND_API_SECRET
            }
            response = requests.post(api_url, data=data, headers=headers)
            response_data = response.status_code
            result = True
        except:
            result = False

        print("resp: " + str(response_data))

        if result == True and response_data == 200:
            print("ping success")
        else:
            print("Ping Failed")
            controller.network_error_state['network_working_fine'] = False
            controller.timer_state['local_elapsed_time_incrementer_active'] = False
            network_handler_utility.network_check_ping(controller)
            controller.show_frame(network_handler_screen.NetworkHandlerScreen)

        print(str(controller.login_state))

    t = threading.Thread(target=api_thread_function)
    controller.thread_list.append(t)
    t.start()


def convert_seconds_time_left(seconds):
    min, sec = divmod(seconds, 60)
    time_left_string = "%02d:%02d" % (min, sec)
    return time_left_string


def save_work_popup(controller):
    messagebox = tk.messagebox.askokcancel("ALERT!!!!!!",
        "Please save all your work!", icon='warning'
        )
    if messagebox == 'yes':
        pass
    


def local_elapsed_time_incrementer(controller):
    seconds_elapsed = controller.timer_state['elapsed_time']
    controller.timer_state['elapsed_time'] = seconds_elapsed + 1

    ColorFlasher(controller.solving_timer_label_object, seconds_elapsed, 1740)

    if seconds_elapsed == TOTAL_WRITING_TIME - 300:
        print("5 minutes left")
        save_work_popup(controller)

    if seconds_elapsed == TOTAL_WRITING_TIME:
        localfolder_utility.closeFiles(controller)

        controller.prev_state = controller.current_state
        controller.current_state = 'submit_only_screen'
        controller.submit_only_screen_state['message'].set(
            'Test Time Is Over.......Submitting the test, Please Wait')
        controller.show_frame(submit_only_screen.SubmitOnlyScreen)
        submit_only_screen_incrementer(controller)
        controller.timer_state['local_elapsed_time_incrementer_active'] = False
        return

    counter = controller.timer_state['counter']
    controller.timer_state['counter'] = counter + 1

    time_left_string = convert_seconds_time_left(
        TOTAL_WRITING_TIME - seconds_elapsed)
    controller.timer_state['time_left'].set(time_left_string)

    # print("seconds elapsed = " + str(seconds_elapsed))
    # print("counter = " + str(counter))
    # print("time_left = " + str(time_left_string) + "\n")

    if counter == PING_INTERVAL:
        ping_elapsed_time(controller, seconds_elapsed)
        controller.timer_state['counter'] = 0
    if controller.timer_state['local_elapsed_time_incrementer_active'] == True:
        threading.Timer(1.0, local_elapsed_time_incrementer,
                        [controller]).start()


# This can also be used to reinitialize timer in case of network failure
def initialize_timer_state(controller):
    username = controller.app_data['username'].get()
    api_url = controller.BACKEND_URL + \
        '/api/userdata/get_elapsed_time/?username=' + username

    result = False
    response_data = {}

    try:
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET
        }
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        result = True
    except:
        result = False

    if result == True and response.status_code == 200:
        try:
            controller.timer_state['elapsed_time'] = response_data['elapsed_time']
        except:
            controller.timer_state['elapsed_time'] = 0
        time_left_string = convert_seconds_time_left(
            TOTAL_WRITING_TIME - controller.timer_state['elapsed_time'])
        controller.timer_state['time_left'].set(time_left_string)
        controller.timer_state['counter'] = 0
        return "SUCCESS"
    else:
        # call network error handler
        return "FAILURE"


##########################################################


def reading_ping_elapsed_time(controller, seconds_elapsed):
    # print("pinged start")
    def api_thread_function():
        api_url = controller.BACKEND_URL+'/api/userdata/update_reading_elapsed_time'

        data = json.dumps({
            'username': controller.app_data['username'].get(),
            'reading_elapsed_time': seconds_elapsed
        })
        headers = {
            "Content-Type": "application/json"
        }

        result = False
        response_data = {}

        try:
            headers = {
                "Content-Type": "application/json",
                "token": controller.app_data["token"],
                "apikey": controller.BACKEND_API_SECRET
            }
            response = requests.post(api_url, data=data, headers=headers)
            response_data = response.status_code
            result = True
        except:
            result = False

        print("resp: " + str(response_data))

        if result == True and response_data == 200:
            print("ping success")
        else:
            print("Ping Failed")
            controller.network_error_state['network_working_fine'] = False
            controller.reading_timer_state['reading_local_elapsed_time_incrementer_active'] = False
            network_handler_utility.network_check_ping(controller)
            controller.show_frame(network_handler_screen.NetworkHandlerScreen)

        print(str(controller.login_state))

    t = threading.Thread(target=api_thread_function)
    controller.thread_list.append(t)
    t.start()


def reading_local_elapsed_time_incrementer(controller):
    seconds_elapsed = controller.reading_timer_state['reading_elapsed_time']
    controller.reading_timer_state['reading_elapsed_time'] = seconds_elapsed + 1

    ColorFlasher(controller.reading_timer_label_object, seconds_elapsed, 240)

    if seconds_elapsed == TOTAL_READING_TIME:
        try:
            reading_ping_elapsed_time(controller, seconds_elapsed)
            database_utility.update_reading_submission_received(controller)
        except:
            # even if network error happens, simply send to next screen
            # solving screen will anyways handle network failure
            pass
        controller.prev_state = controller.current_state
        controller.current_state = 'solving_screen'
        controller.show_frame(solving_screen.SolvingScreen)
        local_elapsed_time_incrementer(controller)
        keyboard.cmd("cmd+left")
        return

    counter = controller.reading_timer_state['reading_counter']
    controller.reading_timer_state['reading_counter'] = counter + 1

    time_left_string = convert_seconds_time_left(
        TOTAL_READING_TIME - seconds_elapsed)
    controller.reading_timer_state['reading_time_left'].set(time_left_string)

    # print("reading seconds elapsed = " + str(seconds_elapsed))
    # print("reading counter = " + str(counter))
    # print("reading time_left = " + str(time_left_string) + "\n")

    if counter == PING_INTERVAL:
        reading_ping_elapsed_time(controller, seconds_elapsed)
        controller.reading_timer_state['reading_counter'] = 0
    if controller.reading_timer_state['reading_local_elapsed_time_incrementer_active'] == True:
        threading.Timer(1.0, reading_local_elapsed_time_incrementer,
                        [controller]).start()


# This can also be used to reinitialize timer in case of network failure
def reading_initialize_timer_state(controller):
    username = controller.app_data['username'].get()
    api_url = controller.BACKEND_URL + \
        '/api/userdata/get_reading_elapsed_time/?username=' + username

    result = False
    response_data = {}

    try:
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET
        }
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        result = True
    except:
        result = False

    if result == True and response.status_code == 200:
        try:
            controller.reading_timer_state['reading_elapsed_time'] = response_data['reading_elapsed_time']
        except:
            controller.reading_timer_state['reading_elapsed_time'] = 0
        time_left_string = convert_seconds_time_left(
            TOTAL_READING_TIME - controller.reading_timer_state['reading_elapsed_time'])
        controller.reading_timer_state['reading_time_left'].set(
            time_left_string)
        controller.reading_timer_state['reading_counter'] = 0
        return "SUCCESS"
    else:
        # call network error handler
        return "FAILURE"


# Submit Only Screen Ping


def ping_submit_only_screen(controller):

    def api_thread_function():
        controller.submit_only_screen_state['status'].set(
            'Trying To Make Submission')
        slot = controller.app_data['batch'].get()
        result1 = "FAIL"
        if (slot == "Slot 3"):
            result1 = final_submission.final_typing_submission(controller)
        else:
            result1 = final_submission.final_submission(controller)  # set result1 = upload_files_to_cloud()
        result2 = "FAIL"
        if result1 == "SUCCESS":
            result2 = database_utility.update_submission_received(controller)

        if result1 == "SUCCESS" and result2 == "SUCCESS":
            controller.submit_only_screen_state['submit_only_screen_ping_active'] = False
            controller.prev_state = controller.current_state
            controller.current_state = 'submitted_test_screen'
            controller.show_frame(submitted_test_screen.SubmittedTestScreen)
        else:
            time.sleep(3)
            controller.submit_only_screen_state['status'].set(
                'Network Error...Trying Again')
    api_thread_function()
    # t = threading.Thread(target=api_thread_function)
    # t.start()
    # controller.thread_list.append(t)


def submit_only_screen_incrementer(controller):

    def api_thread_function():
        while controller.submit_only_screen_state['submit_only_screen_ping_active'] == True:
            ping_submit_only_screen(controller)

    t = threading.Thread(target=api_thread_function)
    controller.thread_list.append(t)
    t.start()


def destroy_application(controller):
    controller.timer_state['local_elapsed_time_incrementer_active'] = False
    controller.reading_timer_state['reading_local_elapsed_time_incrementer_active'] = False
    controller.submit_only_screen_state['submit_only_screen_ping_active'] = False
    # controller.autosaver_active = False

    try:
        os.system('TASKKILL/F /IM WINWORD.exe')
    except Exception as e:
        print("NOT ABLE TO KILL", e)
        pass

    try:
        os.system('TASKKILL/F /IM EXCEL.exe')
    except Exception as e:
        print("NOT ABLE TO KILL", e)
        pass

    try:
        os.system('TASKKILL/F /IM POWERPNT.exe')
    except Exception as e:
        print("NOT ABLE TO KILL", e)
        pass
