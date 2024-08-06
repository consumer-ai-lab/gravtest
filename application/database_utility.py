import json
import requests
import threading
import time
import submit_only_screen
import solving_screen
import start_screen
import start_screen_typing_test
import test_screen
import speed_test_screen
import datetime
import timer_utility
import localfolder_utility
import keyboard
import submitted_test_screen
import submit_only_screen
import fetch_image
import window_handler
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLLabel
from config_module import db_client

mydb = db_client['myFirstDatabase']
info = mydb["config-table"]

time_record = info.find_one({"config_name": "time"})
READING_TIME = time_record["READING_TIME"]
TOTAL_WRITING_TIME = time_record["TOTAL_WRITING_TIME"]


def user_password_match(login_request, controller):
    controller.login_state['login_in_progress'] = True
    controller.login_state['login_status_text'].set('Signing In...Please Wait')

    def api_thread_function():
        api_url = controller.BACKEND_URL+'/api/userdata/'

        data = json.dumps({
            'username': login_request['username'].strip(),
            'user_password': login_request['user_password'].strip(),
            'test_password': login_request['test_password'].strip().lower()
        })

        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET
        }

        result = True
        response = None
        response_data = {}
        try:
            response = requests.post(api_url, data=data, headers=headers)
            response_data = response.json()
            if response is None or response.status_code != 200:
                result = False
            else:
                result = True
        except:
            result = False

        # print(response)
        # print(response_data)

        if result == False:
            controller.login_state['login_in_progress'] = False
            controller.login_state['login_status_text'].set(
                'Network Error \nTry Signing In again.')
            controller.login_state['login_status'] = False
            return

        if result == True and response_data['result'] == 'fail':
            controller.login_state['login_in_progress'] = False
            controller.login_state['login_status_text'].set(
                'Incorrect Credentials \nTry Signing In again with correct username and password.')
            controller.login_state['login_status'] = False
        else:
            # calling fetch_image

            fetch_image.FetchImage.fetchImage(controller)
            test_screen.TestScreen.q1.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.word_image))
            test_screen.TestScreen.q2.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.excel_image))
            test_screen.TestScreen.q3.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.ppt_image))

            solving_screen.SolvingScreen.q1.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.word_image))
            solving_screen.SolvingScreen.q2.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.excel_image))
            solving_screen.SolvingScreen.q3.set_html(
                html="<img src='{0}' width='800'/>".format(fetch_image.FetchImage.ppt_image))

            controller.login_state['login_in_progress'] = False
            controller.login_state['login_status_text'].set('')
            controller.login_state['login_status'] = True
            controller.app_data['batch'].set(response_data["batch"])
            controller.app_data['name'].set(response_data["name"])
            controller.app_data['token'] = response_data['token']
            print(controller.app_data)

            localfolder_utility.create_test_folder(controller)

            elapsed_time = 0
            submission_received = False
            try:
                elapsed_time = response_data['elapsed_time']
            except:
                elapsed_time = 0

            try:
                submission_received = response_data['submission_received']
            except:
                submission_received = False

            reading_elapsed_time = 0
            reading_submission_received = False
            try:
                reading_elapsed_time = response_data['reading_elapsed_time']
            except:
                reading_elapsed_time = 0

            try:
                reading_submission_received = response_data['reading_submission_received']
            except:
                reading_submission_received = False

            # print("submission_receired: " + str(submission_received))
            # print("reading_submission_receired: " +
            #       str(reading_submission_received))
            # print("reading_time_elapsed: " + str(reading_elapsed_time))
            # print("elapsed_time: " + str(elapsed_time))

            if reading_submission_received == True or reading_elapsed_time >= READING_TIME:
                print("c1")
                if submission_received == True:
                    print("c2")
                    controller.prev_state = controller.current_state
                    controller.current_state = 'submitted_test_screen'
                    controller.show_frame(
                        submitted_test_screen.SubmittedTestScreen)
                elif submission_received == False and elapsed_time >= TOTAL_WRITING_TIME:
                    print("c3")
                    '''
                        Submission not received even though elapsed time is exceeded
                        Send to Submit Only Screen
                        So that saved files can be sent to the cloud
                    '''
                    controller.prev_state = controller.current_state
                    controller.current_state = 'submit_only_screen'
                    controller.submit_only_screen_state['message'].set(
                        'from login method')
                    controller.show_frame(submit_only_screen.SubmitOnlyScreen)
                    timer_utility.submit_only_screen_incrementer(controller)

                    controller.prev_state = controller.current_state
                    controller.current_state = 'submit_only_screen'
                    controller.submit_only_screen_state['message'].set(
                        'Test Time Is Over.......Please Wait Till Submission is done')
                    controller.show_frame(submit_only_screen.SubmitOnlyScreen)
                    timer_utility.submit_only_screen_incrementer(controller)
                    pass
                else:
                    print("c4")
                    time_left_string = timer_utility.convert_seconds_time_left(
                        TOTAL_WRITING_TIME-elapsed_time)
                    controller.timer_state['elapsed_time'] = elapsed_time
                    controller.timer_state['counter'] = 0
                    controller.timer_state['time_left'].set(time_left_string)

                    controller.prev_state = controller.current_state
                    controller.current_state = 'solving_screen'
                    controller.show_frame(solving_screen.SolvingScreen)
                    '''
                    RESIZE WINDOW TO ITS ACTUAL SIZE: To be added
                    '''
                    # window_handler.resizeFull(self)
                    timer_utility.local_elapsed_time_incrementer(controller)
            elif reading_elapsed_time == 0:
                print("c5")
                controller.prev_state = controller.current_state
                if controller.app_data["batch"].get() == "Slot 3":
                    controller.current_state = 'start_screen_typing_test'
                    controller.show_frame(
                        start_screen_typing_test.StartScreenTypingTest)
                else:
                    controller.current_state = 'start_screen'
                    controller.show_frame(start_screen.StartScreen)
            else:
                print("c6")
                time_left_string = timer_utility.convert_seconds_time_left(
                    READING_TIME-reading_elapsed_time)
                controller.reading_timer_state['reading_elapsed_time'] = reading_elapsed_time
                controller.reading_timer_state['reading_counter'] = 0
                controller.reading_timer_state['reading_time_left'].set(
                    time_left_string)

                controller.prev_state = controller.current_state
                controller.current_state = 'test_screen'
                controller.show_frame(test_screen.TestScreen)
                timer_utility.reading_local_elapsed_time_incrementer(
                    controller)

    t = threading.Thread(target=api_thread_function)
    controller.thread_list.append(t)
    t.start()


def update_start_time(controller):
    controller.start_test_state['start_test_in_progress'] = True
    controller.start_test_state['start_test_status_text'].set(
        'Starting Test...Please Wait')

    # print(str(controller.start_test_state))

    def api_thread_function():
        api_url = controller.BACKEND_URL+'/api/userdata/update_start_time'

        currDate = str(datetime.datetime.now())
        data = json.dumps({
            'username': controller.app_data['username'].get(),
            'start_time': currDate
        })
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET
        }
        print("header: ", str(headers))

        response_data = 0
        result = False

        try:
            response = requests.post(api_url, data=data, headers=headers)
            response_data = response.status_code
            result = True
        except:
            result = False

        if result == True and response_data == 200:
            localfolder_utility.create_test_folder(controller)
            controller.start_test_state['start_test_in_progress'] = False
            controller.start_test_state['start_test_status_text'].set('')
            controller.start_test_state['start_test_status'] = True

            if controller.app_data["batch"].get() != "Slot 3":
                controller.prev_state = controller.current_state
                controller.current_state = 'test_screen'

                controller.show_frame(test_screen.TestScreen)
                timer_utility.reading_local_elapsed_time_incrementer(
                    controller)
            else:
                controller.prev_state = controller.current_state
                controller.current_state = 'speed_test_screen'

                controller.show_frame(speed_test_screen.SpeedTestScreen)
                screen = controller.frames[speed_test_screen.SpeedTestScreen]
                if screen:
                    if isinstance(screen, speed_test_screen.SpeedTestScreen):
                        screen.start_test()

        else:
            controller.start_test_state['start_test_in_progress'] = False
            controller.start_test_state['start_test_status_text'].set(
                'Network Error...Try Again')
            controller.start_test_state['start_test_status'] = False

    t = threading.Thread(target=api_thread_function)
    controller.thread_list.append(t)
    t.start()


def get_user_object(controller):
    username = controller.app_data['username'].get()
    password = controller.app_data['user_password'].get()
    api_url = controller.BACKEND_URL+'/api/userdata/?username=' + username + \
        '&user_password=' + password
    result = False
    response_data = {}
    response = None

    headers = {
        "Content-Type": "application/json",
        "token": controller.app_data["token"],
        "apikey": controller.BACKEND_API_SECRET
    }

    try:
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        result = True
        return response_data
    except:
        result = False
        return None


def update_reading_submission_received(controller):

    api_url = controller.BACKEND_URL+'/api/userdata/update_reading_submission_received'

    data = json.dumps({
        'username': controller.app_data['username'].get(),
    })
    headers = {
        "Content-Type": "application/json",
        "token": controller.app_data["token"],
        "apikey": controller.BACKEND_API_SECRET
    }

    response_data = 0
    result = False

    try:
        response = requests.post(api_url, data=data, headers=headers)
        response_data = response.status_code
        result = True
    except:
        result = False

    if result == True and response_data == 200:
        return "SUCCESS"

    else:
        return "FAILURE"


def update_submission_received(controller):

    api_url = controller.BACKEND_URL+'/api/userdata/update_submission_received'

    data = json.dumps({
        'username': controller.app_data['username'].get(),
    })
    headers = {
        "Content-Type": "application/json",
        "token": controller.app_data["token"],
        "apikey": controller.BACKEND_API_SECRET
    }

    response_data = 0
    result = False

    try:
        response = requests.post(api_url, data=data, headers=headers)
        response_data = response.status_code
        result = True
    except:
        result = False

    if result == True and response_data == 200:
        return "SUCCESS"

    else:
        return "FAILURE"
