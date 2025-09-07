import streamlit as st
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Get Client IP", layout="centered")
st.title("Client IP Address")

with st.spinner("Fetching your IP address..."):
    ip = st_javascript("await fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => data.ip)")

if ip:
    st.success(f"Your IP Address is: {ip}")
else:
    st.error("Could not fetch your IP address.")
