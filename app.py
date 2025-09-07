import streamlit as st
from streamlit_javascript import st_javascript
import requests
st.title("Client IP Address")

ip = st_javascript("await fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => data.ip)")
st.write("Your IP Address is:", ip)
import requests

def get_ip_info(ip_address):
    try:
        url = f"https://ipapi.co/{ip_address}/json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not retrieve data"}
    except Exception as e:
        return {"error": str(e)}

st.title("IP Address Lookup")
if ip:
    with st.spinner("Fetching IP information..."):
        data = get_ip_info(ip)
    
    if "error" in data:
        st.error(data["error"])
    else:
        st.json(data)
