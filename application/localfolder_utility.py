import os
import sys
import shutil
import keyboard
from pywinauto.findwindows import find_window
from win32gui import SetForegroundWindow

CWD = os.getcwd()
if getattr(sys, 'frozen', False):
    CWD = sys._MEIPASS

def create_test_folder(controller):
   
    username = controller.app_data['username'].get()
    batch = controller.app_data['batch'].get()
    data_folder = os.path.join(CWD, 'data')
    sample_folder = os.path.join(data_folder, 'sample')
    
    test_submission = os.path.join(data_folder, 'test_submission')
    user_submission = os.path.join(test_submission, username)

    doc_file = os.path.join(user_submission, username+'.docx')
    excel_file = os.path.join(user_submission, username+'.xlsx')
    ppt_file = os.path.join(user_submission, username+'.pptx')

    try:
        if not os.path.exists(test_submission):
            os.mkdir(test_submission)
    except Exception as e:
        print(e)
        print("cannot create test_submission folder")

    try:
        if not os.path.exists(user_submission):
            os.mkdir(user_submission)
    except Exception as e:
        print(e)
        print("cannot create user_submission folder")

    try:
        if not os.path.exists(doc_file):
            shutil.copyfile(os.path.join(sample_folder, 'sample.docx'), doc_file)

    except Exception as e:
        print(e)
        print("cannot create username.docx")

    try:
        if not os.path.exists(excel_file):
            shutil.copyfile(os.path.join(sample_folder, 'sample.xlsx'), excel_file)
           
    except:
        print("cannot create username.xlsx")

    try:
        if not os.path.exists(ppt_file):
            shutil.copyfile(os.path.join(sample_folder, 'sample.pptx'), ppt_file)
    except:
        print("cannot create username.ppt")


def openDocFile(controller):
    username = controller.app_data['username'].get()
    file_path = os.path.join(CWD, 'data', 'test_submission', username, username+'.docx')
    try:
        if os.path.exists(file_path):
            os.startfile(file_path)
            SetForegroundWindow(find_window(file_path))
            # keyboard.send("cmd+right")

    except:
        print("Cannot start doc file")

def openExcelFile(controller):
    username = controller.app_data['username'].get()
    file_path = os.path.join(CWD, 'data', 'test_submission', username, username+'.xlsx')

    try:
        if os.path.exists(file_path):
            os.startfile(file_path)
            SetForegroundWindow(find_window(file_path))
            # keyboard.send("cmd+right")
            
    except:
        print("Cannot start excel file")

def openPptFile(controller):
    username = controller.app_data['username'].get()
    file_path = os.path.join(CWD, 'data', 'test_submission', username, username+'.pptx')
    try:
        if os.path.exists(file_path):
            os.startfile(file_path)
            SetForegroundWindow(find_window(file_path))
            # keyboard.send("cmd+right")
    except:
        print("Cannot start ppt file")

def closeFiles(controller):
    try:
        os.system('TASKKILL/F /IM winword.exe')
    except:
        print("Cannot kill winword.exe")

    try:
        os.system('TASKKILL/F /IM excel.exe')
    except:
        print("Cannot kill excel.exe")

    try:
        os.system('TASKKILL/F /IM powerpnt.exe')
    except:
        print("Cannot kill powerpnt.exe")