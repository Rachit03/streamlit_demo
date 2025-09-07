from streamlit_javascript import st_javascript
import streamlit as st

def get_user_location():
    ip = st_javascript("""
        async () => {
            const res = await fetch('https://api.ipify.org?format=json');
            const data = await res.json();
            return data.ip;
        }
    """)

    if not ip:
        st.warning("IP not yet retrieved. Please wait or refresh.")
        st.stop()

    st.write("*" * 20)
    st.write("ip:", ip)

    location_data = get_ip_info(ip)

    st.write("*" * 20)
    st.write("location_data:", location_data)

    return location_data
get_user_location()
