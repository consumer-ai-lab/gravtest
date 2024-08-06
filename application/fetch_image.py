'''
#######  FILE FOR FETCHING QUESTION PAPER  ########

Attributes OF API :    (Querying using test_password)
timeSlot
password
type   - > word/excel/ppt
selectedFile   ->  string (put directly as src in image)
'''

import requests
import os

class FetchImage:
    word_image=""
    excel_image=""
    ppt_image=""
    def __init__(self):
        pass
    
    @classmethod
    def fetchImage(cls,controller):
        word_id=""
        excel_id=""
        ppt_id=""
        test_password=controller.app_data["test_password"].get()
        headers = {
            "Content-Type": "application/json",
            "token": controller.app_data["token"],
            "apikey": controller.BACKEND_API_SECRET
        }
        response = requests.get(controller.BACKEND_URL+'/api/questionData/?pass='+test_password+'&key='+controller.BACKEND_API_SECRET, headers = headers)
        print(response.status_code)

        #checking if we got any response
        if(response.status_code==200):
            data = response.json()
            print(data)

            for question in data:
                if(question["fileType"] == "word"):
                    word_id += question["driveId"]
                if(question["fileType"] == "excel"):
                    excel_id += question["driveId"]
                if(question["fileType"] == "ppt"):
                    ppt_id += question["driveId"]
            # print(questions)
            print("WordiD",word_id)
            print("ExcelId",excel_id)
            print("PPT",ppt_id)

            w_i="https://questiondata.s3.us-east-2.amazonaws.com/" + word_id
            e_i = "https://questiondata.s3.us-east-2.amazonaws.com/" + excel_id
            p_i="https://questiondata.s3.us-east-2.amazonaws.com/" + ppt_id

            print(w_i)

            cls.word_image += w_i
            cls.excel_image += e_i
            cls.ppt_image += p_i

            print(cls.word_image)

            return True

        else:
            return False