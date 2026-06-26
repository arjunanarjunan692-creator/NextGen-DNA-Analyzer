import streamlit as st
from database.db_manager import register_new_user

def show_register_page():
    st.markdown("<h2 style='text-align: center; color: #1e293b;'>Create Research Account</h2>", unsafe_allow_html=True)
    
    # Clean standard fields layout matching our current database configuration
    new_name = st.text_input("Full Name / System Operator")
    new_email = st.text_input("Research Email ID")
    new_password = st.text_input("Choose Password", type="password")
    
    if st.button("Register Account Identity", use_container_width=True):
        if new_name and new_email and new_password:
            success = register_new_user(new_name, new_email, new_password)
            if success:
                st.success("Registration successful! Switch to login mode panel now.")
            else:
                st.error("Error creating user. Email might already exist in system database records.")
        else:
            st.warning("Please fill all configuration fields.")