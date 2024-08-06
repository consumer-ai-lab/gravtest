import keyboard
from win32gui import GetWindowText, GetForegroundWindow
import time
import psutil
import ctypes
from ctypes import wintypes
import os
import threading
'''
Microsoft word:  WINWORD.EXE
Microsoft PPT:  POWERPNT.EXE
Microsoft Excel: EXCEL.EXE
'''

# def autosaver(roll_no, controller):
#     roll_no = str(roll_no)
#     while(controller.autosaver_active == True):
#         print("inside autosaver: " + roll_no)
#         process_list = (i.name() for i in psutil.process_iter())
#         if "WINWORD.EXE" in process_list or "EXCEL.EXE" in process_list or "POWERPNT.EXE" in process_list:
#             window_text = str(GetWindowText(GetForegroundWindow()))
#             # print("ia: " + roll_no + ", " + window_text)
#             if(roll_no in window_text or
#                 roll_no in window_text
#                or roll_no in window_text):
#                 print("saving")
#                 keyboard.send("ctrl+s")
    
#         time.sleep(5)
        


