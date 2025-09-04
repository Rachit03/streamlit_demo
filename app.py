import streamlit as st

def get_client_ip():
    # Try to extract headers where proxies/load balancers may pass client IP
    headers = st.context.headers if hasattr(st, "context") and hasattr(st.context, "headers") else None
    if headers:
        # Check common headers
        if "x-forwarded-for" in headers:
            ip = headers["x-forwarded-for"].split(",")[0]
        elif "remote-addr" in headers:
            ip = headers["remote-addr"]
        else:
            ip = "Unknown"
    else:
        ip = "Localhost (no headers)"
    return ip

st.title("Get User IP in Streamlit")

ip_address = get_client_ip()
st.write(f"Your IP Address is: **{ip_address}**")
