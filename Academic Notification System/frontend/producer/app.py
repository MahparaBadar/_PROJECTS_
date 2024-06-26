import streamlit as st
import requests

# st.title("Producer Notification")

# Page Title
st.title("Mahpara's Academic Notification System - Producer Interface")



# Project Description
st.markdown("""
### Create Notifications
As an administrator, you can create and send notifications to ensure everyone stays informed:
- **Title**: The subject of the notification.
- **Message**: The body of the notification.
- **Recipient**: The intended recipients (e.g., students, teachers, parents).
""")



# Input fields for the notification
title = st.text_input("Title")
message = st.text_area("Message")
recipient = st.text_input("Recipient")

# Function to send notification
def send_notification(title, message, recipient):
    payload = {
        "title": title,
        "message": message,
        "recipient": recipient
    }
    response = requests.post("http://backend:8080/notify/", json=payload)
    return response

if st.button("Send Notification"):
    if not title or not message or not recipient:
        st.error("All fields are required!")
    else:
        response = send_notification(title, message, recipient)
        if response.status_code == 200:
            st.success("Notification sent successfully!")
        elif response.status_code == 404:
            st.error("Recipient not found")
        else:
            st.error("Failed to send notification")

