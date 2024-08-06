# importing tkinter module
from tkinter import *
import tkinter as tk
import root
import timer_utility
import os
import sys
import window_handler
from config_module import config

# creating tkinter window
window = root.Root()
window.configure(bg='white')

window.screen_width = window.winfo_screenwidth()
window.screen_height = window.winfo_screenheight()
window.screen_resolution = str(
    window.screen_width)+'x'+str(window.screen_height)

window.geometry(window.screen_resolution)
window.overrideredirect(True)
# window.state('zoomed')

if __name__ == '__main__':
    '''
    Making Test Excluded from System
    '''

    # If application is not under development make the window not exist-able
    if config["UNDER_DEVELOPMENT"] != "TRUE":
        print("Application: PRODUCTION")
        os.system(
            'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM explorer.exe')

    window.mainloop()
    os.system('start explorer')
    timer_utility.destroy_application(window)
