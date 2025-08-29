import pymongo
import csv
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv("govhack.env")
csv_file = os.getenv("CSV")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[os.getenv("DB_NAME")]
collection = db["Users"]

def csv_to_mongo(filename):
    records = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["username"]
            password = row["password"]
            firstname = row["firstname"]
            security_question = row["security_question"]
            security_answer = row["security_answer"]
            records.append({
                "username": username,
                "password": password,
                "firstname": firstname,
                "security_question": security_question,
                "security_answer": security_answer
            })
    collection.insert_many(records)


def mongo_to_tfrecord(mongo_collection):
    mongo_records = list(mongo_collection.find())

if __name__ == "__main__":
    csv_to_mongo(csv_file)

