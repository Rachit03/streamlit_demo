import streamlit as st
from streamlit_javascript import st_javascript

st.title("Client IP Address")

ip = st_javascript("await fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => data.ip)")
st.write("Your IP Address is:", ip)
