import os
import streamlit as st
import pymongo
from dotenv import load_dotenv
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

# Title
st.title("Jal Jeevan Mission CRUD App")

# Authentication function
def authenticate(username, password):
    user = user_collection.find_one({"username": username, "password": password})
    return user is not None

# Function to create a new question and answer
def create_entry(question, answer, username):
    chatbot_collection.insert_one({
        "question": question,
        "answer": answer,
        "updated_on": datetime.now(),
        "updated_by": username
    })
    st.success("Entry created successfully!")

# Function to read entries
def read_entries():
    entries = chatbot_collection.find()
    for entry in entries:
        st.write(f"Question: {entry['question']}")
        st.write(f"Answer: {entry['answer']}")
        # st.write(f"Updated on: {entry['updated_on']} ; By: {entry['updated_by']}")
        st.write("---")

def read_entries_auth():
    entries = chatbot_collection.find()
    for entry in entries:
        st.write(f"Question: {entry['question']}")
        st.write(f"Answer: {entry['answer']}")
        st.write(f"Updated on: {entry['updated_on']} , By: {entry['updated_by']}")
        st.write("---")

# Function to update an entry
def update_entry(question, new_answer, username):
    chatbot_collection.update_one(
        {"question": question},
        {"$set": {"answer": new_answer, "updated_on": datetime.now(), "updated_by": username}}
    )
    st.success("Entry updated successfully!")

# Function to delete an entry
def delete_entry(question):
    chatbot_collection.delete_one({"question": question})
    st.success("Entry deleted successfully!")

# Sidebar for Login
st.sidebar.title("Login")
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.sidebar.success("Logged out successfully")

if st.session_state.authenticated:
    option = st.selectbox("Select Operation", ["Create", "Read", "Update", "Delete"])

    if option == "Create":
        st.subheader("Create a new entry")
        question = st.text_input("Question")
        answer = st.text_input("Answer")
        if st.button("Create"):
            create_entry(question, answer, st.session_state.username)

    elif option == "Read":
        st.subheader("All Entries")
        read_entries_auth()

    elif option == "Update":
        st.subheader("Update an entry")
        entries = list(chatbot_collection.find())
        questions = [entry['question'] for entry in entries]
        selected_question = st.selectbox("Select Question to update", questions)
        new_answer = st.text_input("New Answer")
        if st.button("Update"):
            update_entry(selected_question, new_answer, st.session_state.username)

    elif option == "Delete":
        st.subheader("Delete an entry")
        entries = list(chatbot_collection.find())
        questions = [entry['question'] for entry in entries]
        selected_question = st.selectbox("Select Question to delete", questions)
        if st.button("Delete"):
            delete_entry(selected_question)
else:
    st.subheader("All Entries")
    read_entries()
