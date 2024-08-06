'''
FINAL SUBMISSION

This file will convert the user submission docs into a single pdf and will store
it to google drive

Installations needed:
1. PyPDF2 :  pip install PyPDF2  (pdf merger)
2. docx2pdf : pip install docx2pdf (doc to pdf converter)
3. pip install pywin32
'''

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
from PyPDF2 import PdfMerger, PdfReader, PdfWriter, PdfFileMerger, PdfFileWriter, PdfFileReader
from docx2pdf import convert
import pythoncom
import botocore
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
import pymongo
from config_module import config

CWD = os.getcwd()
if getattr(sys, 'frozen', False):
    CWD = sys._MEIPASS


def docpdfconvert2(in_file):
    try:
        convert(in_file)
        return True
    except:
        return False


'''
AWS S3 Credentials
'''

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id = config["aws_access_key_id"],
    aws_secret_access_key = config["aws_secret_access_key"]
)

bucket_name = config["bucket_name"]

ppt_slide_count = 0  # global variable to count number of slides in ppt

list_of_error_roll_nos = []


def add_detail_footer(src_file, dest_file, roll_no, batch):
    date = datetime.datetime.now()
    date_string = date.strftime("%d/%m/%Y %H:%M:%S")

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(50, 765, "Roll Number: " + str(roll_no) +
                   str(" " * 10) + " Batch: " + str(batch) +
                   str(" " * 10) + " Date: " + str(date_string))
    can.save()

    packet_ppt = io.BytesIO()
    can_ppt = canvas.Canvas(packet_ppt, pagesize=A4)
    can_ppt.drawString(50, 500, "Roll Number: " + str(roll_no) +
                       str(" " * 10) + " Batch: " + str(batch) +
                       str(" " * 10) + " Date: " + str(date_string))
    can_ppt.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    packet_ppt.seek(0)
    new_ppt_pdf = PdfReader(packet_ppt)

    existing_pdf = PdfReader(open(src_file, "rb"))
    n = len(existing_pdf.pages)  # existing_pdf.getNumPages()
    output = PdfWriter()

    for i in range(n):
        page = existing_pdf.pages[i]

        if i <= (n - i - 1):
            page.merge_page(new_pdf.pages[0])
        else:
            page.merge_page(new_ppt_pdf.pages[0])
        output.add_page(page)

    # finally, write "output" to a real file
    outputStream = open(dest_file, "wb")
    output.write(outputStream)
    outputStream.close()
    print("n = " + str(n))


CWD = os.getcwd()


def final_submission(user_roll_no, batch):
    global ppt_slide_count
    ppt_slide_count = 0
    pythoncom.CoInitialize()
    print("final_submission() called")
    username = user_roll_no
    print(type(username))
    # download doc file and store path in doc_file_path

    merging_has_occurred = True
    destination_folder = os.path.join(CWD, 'prints')

    try:
        print("c1, check if merged file exists")
        s3.Object(bucket_name, batch + "/" + user_roll_no +
                  '/' + username + 'Final.pdf').load()
    except botocore.exceptions.ClientError as e:
        print("c2")
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            merging_has_occurred = False
        else:
            # Something else has gone wrong.
            return "FAIL"
    else:
        print("c3, merged file exists")
        # The object does exist.
        merging_has_occurred = False

    if merging_has_occurred:
        print("c4, download merged file")
        # the file is already merged, so download merged pdf and store in prints folder
        output_file_name = os.path.join(destination_folder, username + '.pdf')
        s3.Bucket(bucket_name).download_file(
            batch + "/" + user_roll_no + '/' + username + 'Final.pdf', output_file_name)
    else:
        # the file is not merged....
        # do the merging process and then send to prints folder
        print("c5, download all files")
        doc_file_path = os.path.join(CWD, 'processing', user_roll_no + '.docx')
        excel_file_path = os.path.join(
            CWD, 'processing', user_roll_no + '.xlsx')
        ppt_file_path = os.path.join(CWD, 'processing', user_roll_no + '.pptx')

        print(doc_file_path)
        s3.Bucket(bucket_name).download_file(batch + "/" +
                                             user_roll_no + '/' + username + '.docx', doc_file_path)
        s3.Bucket(bucket_name).download_file(batch + "/" +
                                             user_roll_no + '/' + username + '.xlsx', excel_file_path)
        s3.Bucket(bucket_name).download_file(batch + "/" +
                                             user_roll_no + '/' + username + '.pptx', ppt_file_path)
        try:
            print("c6, convert all files to pdf")
            try:
                print("c7, convert doc to pdf")
                if os.path.exists(doc_file_path):
                    docpdfconvert2(doc_file_path)
            except Exception as e:
                print("Cannot make pdf of doc: " + str(e))
                return "FAIL"

            try:
                print("c8, convert excel to pdf")
                if os.path.exists(excel_file_path):
                    excel = win32com.client.Dispatch("Excel.Application")
                    in_file = excel_file_path  # Read Excel File
                    out_file = os.path.splitext(in_file)[0] + "excel.pdf"
                    print(in_file, out_file)
                    sheets = excel.Workbooks.Open(in_file)
                    print(sheets)
                    sheets.ExportAsFixedFormat(
                        0, out_file
                    )  # Convert into PDF File
                    sheets.Close(True)
                    excel.Quit()
            except Exception as e:
                print("Cannot make pdf of excel: " + str(e))
                return "FAIL"

            try:
                print("c9, convert ppt to pdf")
                if os.path.exists(ppt_file_path):
                    # converting pptx to pdf
                    in_file = ppt_file_path
                    out_file = os.path.splitext(in_file)[0] + "ppt"
                    powerpoint = win32com.client.Dispatch(
                        "Powerpoint.Application")
                    pdf = powerpoint.Presentations.Open(
                        in_file, WithWindow=False)
                    # counts the number of slides in ppt
                    ppt_slide_count = len(pdf.Slides)
                    pdf.SaveAs(out_file, 32)
                    pdf.Close()
                    powerpoint.Quit()
            except Exception as e:
                print("Cannot make pdf of ppt: " + str(e))
                return "FAIL"

            '''
            MERGING PDFS into rollno.pdf
            '''
            try:
                print("c10, merge pdfs")
                pdfs = [os.path.join(CWD, 'processing', username + '.pdf'), os.path.join(
                    CWD, 'processing', username + 'excel.pdf'), os.path.join(CWD, 'processing', username + 'ppt.pdf')]

                merger = PdfMerger()

                for pdf in pdfs:
                    merger.append(pdf)

                merger.write(os.path.join(
                    CWD, 'processing', username + 'merger.pdf'))
                merger.close()
            except Exception as e:
                print("Merged pdf not created: " + str(e))
                return "FAIL"

            '''
            Adding Name Header
            '''
            try:
                add_detail_footer(os.path.join(CWD, 'processing', username + 'merger.pdf'),
                                os.path.join(destination_folder, username + '.pdf'), username, batch)
            except Exception as e:
                print("Could not add name header", str(e))
                return "FAIL"
        except:
            return "FAIL"
    return "SUCCESS"


# final_submission("12798", "Batch 1")

import ssl

client = pymongo.MongoClient(config["MONGO_URL"])
mydb = client['myFirstDatabase']
userCollection = mydb.users
test_password = 'b3wcll3'
batch_name = 'Batch 3'

# data = userCollection.find({'test_password': test_password})

# for i in data:
#     print(str(i))

# for i in data:
#     if i['submission_received'] == True:
#         temp = final_submission(i['username'], batch_name)
#         if (temp == "FAIL"):
#             list_of_error_roll_nos.append(i['username'])
#     else:
#         list_of_error_roll_nos.append(i['username'])

final_submission("13143", "Batch 3")

print("errors: ")
for i in list_of_error_roll_nos:
    print(i)
