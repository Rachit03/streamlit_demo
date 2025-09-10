import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("Get User IP")

# Run JavaScript inside the browser and get result back into Python
ip = streamlit_js_eval(
    js_expressions="fetch('https://api.ipify.org?format=json').then(r => r.json()).then(d => d.ip)",
    key="get_ip"
)

if ip:
    st.success(f"Your IP is: {ip}")
else:
    st.info("Fetching your IP...")
