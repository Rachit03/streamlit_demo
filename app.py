import streamlit as st
import requests

def get_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except Exception as e:
        return f"Error fetching IP: {e}"

st.title("Client IP Address")

ip_address = get_ip()
st.write("Your IP Address is:", ip_address)
