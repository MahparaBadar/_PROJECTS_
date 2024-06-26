import streamlit as st
import requests

st.title("Mahpara's Recipe Quest")

# Sign Up
st.header("Sign Up")
signup_username = st.text_input("Username", key="signup_username")
signup_password = st.text_input("Password", type="password", key="signup_password")
if st.button("Sign Up"):
    response = requests.post("http://backend:8000/signup/", json={"username": signup_username, "password": signup_password})
    if response.status_code == 200:
        st.success("User created successfully")
    else:
        st.error(f"Error creating user: {response.text}")

# Login
st.header("Login")
login_username = st.text_input("Username", key="login_username")
login_password = st.text_input("Password", type="password", key="login_password")
if st.button("Login"):
    response = requests.post("http://backend:8000/token", data={"username": login_username, "password": login_password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state["token"] = token
        st.success("Logged in successfully")
    else:
        st.error(f"Error logging in: {response.text}")

# Register Favorite Cuisine
if "token" in st.session_state:
    st.header("Register Favorite Cuisine")
    cuisine = st.text_input("Favorite Cuisine")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    if st.button("Register Cuisine"):
        response = requests.post("http://backend:8000/favorite_cuisine/", json={"cuisine": cuisine}, headers=headers)
        if response.status_code == 200:
            st.success("Cuisine registered successfully")
        else:
            st.error(f"Error registering cuisine: {response.text}")

    # Get Recipe
    st.header("Get Recipe")
    if st.button("Get Recipe"):
        response = requests.get("http://backend:8000/recipe/", headers=headers)
        if response.status_code == 200:
            recipe = response.json()["recipe"]
            st.write(f"Recipe for {response.json()['cuisine']}:")
            st.write(recipe)
        else:
            st.error(f"Error fetching recipe: {response.text}")


