import threading
import datetime
import requests
import json
import solving_screen
import timer_utility
import test_screen

NETWORK_CHECK_PING_INTERVAL = 10  # save elapsed time to db every 30 seconds
TOTAL_WRITING_TIME = 1800  # 30 min = 1800 seconds

# This can also be used to reinitialize timer in case of network failure


def network_check_ping(controller):
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
        controller.network_error_state['network_status'].set('Trying To Reconnect...')
        response = requests.get(api_url, headers = headers)
        response_data = response.json()
        result = True
    except:
        print("network_handler_utility : exception 1")
        result = False

    print("resp: " + str(response_data))
    print("network_state: " + str(controller.network_error_state) + \
        "current_state: " + str(controller.current_state))

    if result == True and response.status_code == 200:
        if controller.current_state == 'test_screen':
            op = timer_utility.reading_initialize_timer_state(controller)
            if op == "SUCCESS":
                print("sending back to TestScreen")
                controller.show_frame(test_screen.TestScreen)
                controller.reading_timer_state['reading_local_elapsed_time_incrementer_active'] = True
                timer_utility.reading_local_elapsed_time_incrementer(
                    controller)
                result = True
            else:
                print("Filed to initialize reading timer state")
                result = False

        elif controller.current_state == 'solving_screen':
            op = timer_utility.initialize_timer_state(controller)
            if op == "SUCCESS":
                print("sending back to SolvingScreen")
                controller.show_frame(solving_screen.SolvingScreen)
                controller.timer_state['local_elapsed_time_incrementer_active'] = True
                timer_utility.local_elapsed_time_incrementer(controller)
                result = True
            else:
                print("Filed to initialize solving timer state")
                result = False

    if result == False or response.status_code != 200:
        controller.network_error_state['network_working_fine'] = False
        controller.network_error_state['network_status'].set('Failed To Reconnect...')
        threading.Timer(NETWORK_CHECK_PING_INTERVAL,
                        network_check_ping, [controller]).start()
    else:
        controller.network_error_state['network_status'].set('')
        controller.network_error_state['network_working_fine'] = True
