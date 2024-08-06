"""
FINAL SUBMISSION

This file will convert the user submission docs into a single pdf and will store
it to google drive

Installations needed:
1. PyPDF2 :  pip install PyPDF2  (pdf merger)
2. docx2pdf : pip install docx2pdf (doc to pdf converter)
3. pip install pywin32
"""

import os
import shutil
import requests
import psutil
import sys
import comtypes.client
import time
import json
import boto3
import win32com.client
from PyPDF2 import (
    PdfFileMerger,
    PdfFileWriter,
    PdfFileReader,
    PdfReader,
    PdfWriter,
    PdfMerger,
)
from docx2pdf import convert
import pythoncom
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
from config_module import config

CWD = os.getcwd()
if getattr(sys, "frozen", False):
    CWD = sys._MEIPASS


def checkProcessExist(a):
    if a.lower() in (p.name().lower() for p in psutil.process_iter()):
        return True
    return False


def windowTerminator(pname):
    num = 0
    while num < 5:
        ans = checkProcessExist(pname)
        if ans == False:
            break
        time.sleep(1)
        num += 1
        os.system("taskkill /F /IM " + pname)


def docpdfconvert1(in_file, out_file):
    try:
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(in_file)
        doc.SaveAs(out_file, FileFormat=17)
        doc.Close()
        word.Quit()
        return True
    except:
        return False


def docpdfconvert2(in_file):
    try:
        convert(in_file)
        return True
    except:
        return False


"""
AWS S3 Credentials
"""

s3 = boto3.resource(
    service_name="s3",
    region_name="us-east-2",
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
)

bucket_name = config["bucket_name"]

ppt_slide_count = 0  # global variable to count number of slides in ppt


def add_detail_footer(src_file, dest_file, roll_no, batch, qs_name):
    date = datetime.datetime.now()
    date_string = date.strftime("%d/%m/%Y %H:%M:%S")

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(
        20,
        20,
        "Roll Number: "
        + str(roll_no)
        + str(" " * 8)
        + " Batch: "
        + str(batch)
        + str(" " * 8)
        + " Date: "
        + str(date_string)
        + str(" " * 8)
        + "Section: "
        + str(qs_name),
    )
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(src_file, "rb"))
    n = len(existing_pdf.pages)
    output = PdfWriter()

    for i in range(n):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # finally, write "output" to a real file
    outputStream = open(dest_file, "wb")
    output.write(outputStream)
    outputStream.close()
    print("n = " + str(n))


def final_submission(controller):
    global ppt_slide_count
    pythoncom.CoInitialize()
    print("final_submission() called")
    username = controller.app_data["username"].get()
    print(type(username))
    batch = controller.app_data["batch"].get()

    batch_name = ""

    if batch == "Slot 1":
        batch_name += "Batch 1"
    elif batch == "Slot 2":
        batch_name += "Batch 2"
    else:
        batch_name += "Batch 3"

    """
    Creating Folder and files on amazon S3  for user's submissions
    """

    user_folder_name = ""
    # Creating folder of submission of that user and 2 files in it. One merged pdf of word and ppt and other excel file
    try:
        user_folder_name = batch_name + "/" + username + "/"
        s3.Bucket(bucket_name).put_object(Bucket=bucket_name, Key=user_folder_name)
    except Exception as e:
        print("Folder not uploaded: " + str(e))
        return "FAIL"

    doc_file_path = os.path.join(
        CWD, "data", "test_submission", username, username + ".docx"
    )
    excel_file_path = os.path.join(
        CWD, "data", "test_submission", username, username + ".xlsx"
    )
    ppt_file_path = os.path.join(
        CWD, "data", "test_submission", username, username + ".pptx"
    )

    doc_pdf_path, excel_pdf_path, ppt_pdf_path = "", "", ""
    try:
        """
        CONVERTING DOC TO PDF
        """
        try:
            if os.path.exists(doc_file_path):
                try:
                    windowTerminator("WINWORD.EXE")
                except Exception as e:
                    print("nOT ABLE TO KILL", e)
                    pass

                doc_pdf_path = os.path.join(
                    CWD, "data", "test_submission", username, username + ".pdf"
                )

                # converting docx to pdf
                isConverted1 = docpdfconvert1(doc_file_path, doc_pdf_path)
                if isConverted1 == False:
                    isConverted2 = docpdfconvert2(doc_file_path)

                add_detail_footer(
                    doc_pdf_path, doc_pdf_path, username, batch, "MS Word"
                )

        except Exception as e:
            print("Cannot make pdf of doc: " + str(e))

        try:
            if os.path.exists(excel_file_path):
                try:
                    windowTerminator("EXCEL.EXE")
                except:
                    pass

                excel = win32com.client.Dispatch("Excel.Application")

                in_file = excel_file_path  # Read Excel File
                out_file = os.path.splitext(in_file)[0] + "excel.pdf"

                sheets = excel.Workbooks.Open(in_file)

                sheets.ExportAsFixedFormat(0, out_file)  # Convert into PDF File
                sheets.Close(True)
                excel.Quit()

                excel_pdf_path = os.path.join(
                    CWD, "data", "test_submission", username, username + "excel.pdf"
                )
                add_detail_footer(
                    excel_pdf_path, excel_pdf_path, username, batch, "MS Excel"
                )

        except Exception as e:
            print("Cannot make pdf of excel: " + str(e))

        """
        Converting PPT to PDF
        """

        try:
            if os.path.exists(ppt_file_path):
                try:
                    windowTerminator("POWERPNT.EXE")
                except:
                    pass

                # converting pptx to pdf
                in_file = ppt_file_path
                out_file = os.path.splitext(in_file)[0] + "ppt"
                powerpoint = win32com.client.Dispatch("Powerpoint.Application")
                pdf = powerpoint.Presentations.Open(in_file, WithWindow=False)
                ppt_slide_count = len(pdf.Slides)  # counts the number of slides in ppt
                pdf.SaveAs(out_file, 32)
                pdf.Close()
                powerpoint.Quit()

                ppt_pdf_path = os.path.join(
                    CWD, "data", "test_submission", username, username + "ppt.pdf"
                )
                add_detail_footer(
                    ppt_pdf_path, ppt_pdf_path, username, batch, "MS PowerPoint"
                )

        except Exception as e:
            print("Cannot make pdf of ppt: " + str(e))

        """
        MERGING PDFS into rollno.pdf
        """
        try:
            pdfs = [doc_pdf_path, excel_pdf_path, ppt_pdf_path]

            merger = PdfMerger()

            for pdf in pdfs:
                merger.append(pdf)

            merger.write(
                os.path.join(
                    CWD, "data", "test_submission", username, username + "final.pdf"
                )
            )
            merger.close()
        except Exception as e:
            print("Merged pdf not created: " + str(e))

        """
        Batch name allocation using Batch Slot
        """

        try:
            merged_key = ""
            if os.path.exists(
                os.path.join(
                    CWD, "data", "test_submission", username, username + "Final.pdf"
                )
            ):
                # merged_id = createFile(username+'Final.pdf',os.path.join(CWD, 'data', 'test_submission', username,username+'Final.pdf'),'application/pdf',user_folderId)
                merged_key += user_folder_name + username + "Final.pdf"
                s3.Bucket(bucket_name).upload_file(
                    Filename=os.path.join(
                        CWD, "data", "test_submission", username, username + "Final.pdf"
                    ),
                    Key=merged_key,
                )
                print(merged_key)

        except Exception as e:
            print("Merged file not uploaded: " + str(e))
            return "FAIL"

        # Sending Files

        try:

            doc_id = s3.Bucket(bucket_name).upload_file(
                Filename=doc_file_path, Key=user_folder_name + username + ".docx"
            )
        except Exception as e:
            print("Doc file not uploaded: " + str(e))
            return "FAIL"

        try:
            excel_id = s3.Bucket(bucket_name).upload_file(
                Filename=excel_file_path, Key=user_folder_name + username + ".xlsx"
            )
        except Exception as e:
            print("Excel file not able to upload: " + str(e))
            return "FAIL"

        try:
            ppt_id = s3.Bucket(bucket_name).upload_file(
                Filename=ppt_file_path, Key=user_folder_name + username + ".pptx"
            )
        except Exception as e:
            print("PPT file not able to upload: " + str(e))
            return "FAIL"

        """
        API CREATION for fetching username, batch and his folder id 
        """
        try:
            url = controller.BACKEND_URL + "/api/userdata/update_submission_folder_id"
            myobj = json.dumps(
                {
                    "username": username,
                    "submission_folder_id": user_folder_name,
                    "merged_file_id": merged_key,
                }
            )
            headers = {
                "Content-Type": "application/json",
                "token": controller.app_data["token"],
                "apikey": controller.BACKEND_API_SECRET,
            }
            x = requests.post(url, data=myobj, headers=headers)
        except:
            return "Fail"

    except:
        return "Fail"

    return "SUCCESS"


def final_typing_submission(controller):
    username = controller.app_data["username"].get()
    print(type(username))
    batch = controller.app_data["batch"].get()
    print("final_typing_submission() called")

    # generate pdf with these data
    try:
        date = datetime.datetime.now()
        date_string = date.strftime("%d/%m/%Y %H:%M:%S")
        new_pdf_path = os.path.join(
            CWD, "data", "test_submission", username, f"{username}Final.pdf"
        )

        # Create a PDF canvas
        from reportlab.platypus import Paragraph

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # Draw text on the canvas
        can.drawString(
            20,
            20,
            f"Roll Number: {username}        Batch: {batch}        Date: {date_string}",
        )

        input_text = Paragraph(
            "<para align=justify><font size=14><b>Candidate's Response</b></font><br></br><font size=12>%s</font></para>"
            % controller.input_text
        )

        input_text.wrapOn(can, 400, 400)
        input_text.drawOn(can, 100, 400)

        can.save()
        packet.seek(0)
        with open(new_pdf_path, "wb") as outputStream:
            outputStream.write(packet.getbuffer())

        # do a post request on /api/userdata/wpm
        url = controller.BACKEND_URL + "/api/userdata/wpm"
        myobj = json.dumps(
            {
                "username": username,
                "wpm": controller.wpm,
                "wpm_time": controller.time,
                "wpm_normal": controller.wpm_normal
            }
        )
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET,
        }
        x = requests.post(url, data=myobj, headers=headers)
    except Exception as e:
        print("Error in final_typing_submission: " + str(e))
        return "Fail"
    try:
        user_folder_name = ""
        batch_name = ""
        if batch == "Slot 1":
            batch_name += "Batch 1"
        elif batch == "Slot 2":
            batch_name += "Batch 2"
        else:
            batch_name += "Batch 3"
        user_folder_name = batch_name + "/" + username + "/"
        s3.Bucket(bucket_name).put_object(Bucket=bucket_name, Key=user_folder_name)
        merged_key = ""
        if os.path.exists(
            os.path.join(
                CWD, "data", "test_submission", username, username + "Final.pdf"
            )
        ):
            merged_key += user_folder_name + username + "Final.pdf"
            s3.Bucket(bucket_name).upload_file(
                Filename=os.path.join(
                    CWD, "data", "test_submission", username, username + "Final.pdf"
                ),
                Key=merged_key,
            )
            print(merged_key)
        url = controller.BACKEND_URL + "/api/userdata/update_submission_folder_id"
        myobj = json.dumps(
            {
                "username": username,
                "submission_folder_id": user_folder_name,
                "merged_file_id": merged_key,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET,
        }
        x = requests.post(url, data=myobj, headers=headers)
    except Exception as e:
        print("Error in final_typing_submission: " + str(e))
        return "Fail"
    return "SUCCESS"
