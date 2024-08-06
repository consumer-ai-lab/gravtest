import os
import sys
import pymongo
from dotenv import dotenv_values
import certifi

# env config
try:
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False):
        extDataDir = sys._MEIPASS

    env_path = os.path.join(extDataDir, '.env')

    config = dict(dotenv_values(env_path))
    # print(config)
    print("ENV imported")
except Exception as e:
    print("Error while configuring .env")
    print(e)

# database
try:
    db_client = pymongo.MongoClient(
        config["MONGO_URL"], tlsCAFile=certifi.where())
    print("Database connected")
except Exception as e:
    print("Error while connecting mongo db")
    print(e)

# creating database
# mydb = db_client['myFirstDatabase']

# creating collection
# info = mydb["config-table"]

# print(info.find_one({"config_name":"ip"})["ip"])
