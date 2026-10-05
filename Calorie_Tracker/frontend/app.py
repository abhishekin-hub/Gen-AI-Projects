import os
import sys
import requests
import streamlit as st
from urllib3.util import response

API_URL = "http://localhost:8000/calorie"

st.title("CalTracker")
st.write("CalTracker allows users to calculate the calories intake for a specific dish or for the entire day.")

Tracker_type = st.radio("Tracker Options", ["Meal Calorie Tracker", "Full-Day Calorie Tracker"], horizontal= True, )

if Tracker_type == "Meal Calorie Tracker":
    st.write("Track your calories intake of a single meal.")
    
    dish_name = st.text_input("Enter the dish name")
    
    if st.button("Calculate Calories"):
        if not dish_name:
            st.error("Please enter a dish name")
        else:
            with st.spinner("Calculating Calories..."):
                payload = {"dish_name": dish_name}

                try:
                    response = requests.post(API_URL,json=payload)

                    if response.status_code == 200:
                        calories = response.json()
                        st.json(calories)

                    else:
                        st.error(f"Error calculating calories: {response.status_code}")
                    
                except requests.exceptions.RequestException as e: 
                    st.error(f"Could not connect to backend: {e}")


else:
    st.write("Track your calories intake for the entire day.")
    st.write("What you had for breakfast/Lunch/Dinner/Snacks?")
    
    if "meal_list" not in st.session_state:
        st.session_state.meal_list = []
    
    dish_name = st.text_input("Enter the dish name")
    
    if st.button("Add Meals"):
        if not dish_name:
            st.error("Please enter a dish name")
        else:
            st.session_state.meal_list.append(dish_name)
            st.success(f"Added: {dish_name}")
    
    if st.session_state.meal_list:
        st.write("### List of Meals:")
        for i, meal in enumerate(st.session_state.meal_list, 1):
            st.write(f"{i}. {meal}")

    if st.button("Calculate Calories"):
        if not st.session_state.meal_list:
            st.error("Please add at least one meal")
        else:
            with st.spinner("Calculating Calories..."):
                payload={"meal_list": st.session_state.meal_list}

                try:
                    response = requests.post(API_URL, json=payload)

                    if response.status_code == 200:
                        calories = response.json()
                        st.json(calories)
                    else:
                        st.error(f"Error calculating calories: {response.status_code}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to backend: {e}")