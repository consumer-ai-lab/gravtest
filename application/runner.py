###########################################################
###########################################################
# THIS FILE IS FOR TESTING SPECIFIC FRAME OF THE APPLICATION

from tkinter import *
import tkinter as tk
import root
import test_screen
import timer_utility
import solving_screen
import speed_test_screen
import submitted_test_screen
import network_handler_screen
import network_handler_utility
import final_submission
import start_screen

# creating tkinter window
window = root.Root()
window.configure(bg='white')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
screen_resolution = str(screen_width)+'x'+str(screen_height)

window.geometry(screen_resolution)
window.state('zoomed')


window.app_data = {
    'username': tk.StringVar(),
    'user_password': tk.StringVar(),
    'test_password': tk.StringVar(),
}

window.app_data['username'].set('r4')
window.app_data['user_password'].set('p4')
window.app_data['test_password'].set('p4')

window.login_state = {
    'login_in_progress': False,
    'login_status': False,
    'login_status_text': tk.StringVar()
}

window.start_test_state = {
    'start_test_in_progress': False,
    'start_test_status': False,
    'start_test_status_text': tk.StringVar()
}

if __name__ == '__main__':
    # final_submission.final_submission(window)
    # window.show_frame(solving_screen.SolvingScreen)
    window.show_frame(speed_test_screen.SpeedTestScreen)
    window.mainloop()
    print("post mainloop")
