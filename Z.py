import os
import pymongo
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()
PASSWORD = os.environ['PASSWORD']

# MongoDB connection
client = pymongo.MongoClient(
    f"mongodb+srv://jaljeevanmissioniimb:{PASSWORD}@jjmcluster.0ygt3tb.mongodb.net/?retryWrites=true&w=majority&appName=JJMCluster"
)
db = client["jaljeevanmissioniimb"]
chatbot_collection = db["Chatbot"]
user_collection = db["User"]

# LOAD A JSON FILE AND ASSIGN ITS QUESTION,ANSWER IN MONGODB DATABASE #

def create_entry(question, answer, username):
    chatbot_collection.insert_one({
        "question": question,
        "answer": answer,
        "updated_on": datetime.now(),
        "updated_by": username
    })
    print("Entry created successfully!")


if __name__=="__main__":
    # LOAD JSON QnA File
    with open("suggested_questions.json", 'r') as file:
        qna_list = json.load(file)
    for item in qna_list:
        question = item['question']
        answer = item['answer']
        print(question, answer)
        # create_entry(question, answer, "admin")
