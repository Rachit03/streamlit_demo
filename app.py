import streamlit as st
import requests

st.title("Get Your Public IP Address using ipify")

def fetch_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        if response.status_code == 200:
            return response.text.strip()
        else:
            st.warning(f"Unexpected response: {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Error fetching IP: {e}")
    return "Unavailable"

public_ip = fetch_public_ip()
st.write(f"Your public IP address is: **{public_ip}**")
