import streamlit as st
import requests

# Page Title
st.title("Mahpara's Academic Notification System - Consumer Interface")

# Project Description
st.markdown("""
### Academic Alerts
Stay informed with Mahpara's Academic Alerts:
- **Timely Notifications**: Receive updates on courses, assignments, and events.
- **Personalized Updates**: Tailored alerts for students, teachers, and parents.

### Features
- User authentication (Signup and Login)
- Notification creation and retrieval
""")


# Function to handle user signup
def signup(username, password):
    signup_data = {
        "username": username,
        "password": password
    }
    response = requests.post("http://backend:8080/signup/", json=signup_data)
    return response

# Function to handle user login
def login(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post("http://backend:8080/token/", data=login_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        st.sidebar.success("Login Successful")
        return access_token
    else:
        st.sidebar.error("Login Failed")
        return None

# Function to handle notifications retrieval
def get_notifications(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://backend:8080/notifications/", headers=headers)
    return response

# Sidebar for Login and Signup
st.sidebar.title("User Authentication")

signup_expander = st.sidebar.expander("Sign Up")
with signup_expander:
    signup_username = st.text_input("Sign Up Username", key="signup_username")
    signup_password = st.text_input("Sign Up Password", type="password", key="signup_password")
    if st.button("Sign Up", key="signup_button"):
        signup_response = signup(signup_username, signup_password)
        if signup_response.status_code == 200:
            st.sidebar.success("Sign Up Successful")
        elif signup_response.status_code == 400:
            st.sidebar.error("Username already registered")
        else:
            st.sidebar.error("Sign Up Failed")

login_expander = st.sidebar.expander("Login")
with login_expander:
    login_username = st.text_input("Login Username", key="login_username")
    login_password = st.text_input("Login Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        access_token = login(login_username, login_password)
        if access_token:
            notifications_response = get_notifications(access_token)
            if notifications_response.status_code == 200:
                notifications = notifications_response.json()
                for index, notification in enumerate(notifications):
                    notification_md = f"""
**Notification {index + 1}**

**Title:** {notification['title']}

**Message:** {notification['message']}

**Recipient:** {notification['recipient']}
"""
                    st.markdown(notification_md)
            else:
                st.error("Failed to retrieve notifications")
