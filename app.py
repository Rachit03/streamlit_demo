import streamlit as st
from streamlit_javascript import st_javascript
import requests
import json

st.title("Client IP Address & Location Details")

# Method 1: Server-side approach (most reliable)
st.subheader("🖥️ Server-side IP Detection")

try:
    # Get IP and details from server-side
    response = requests.get('https://ipapi.co/json/', timeout=10)
    if response.status_code == 200:
        server_data = response.json()
        
        st.success("✅ Server-side detection successful!")
        
        # Display server-detected info
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🌐 IP Address", server_data.get('ip', 'Unknown'))
            st.metric("🏳️ Country", server_data.get('country_name', 'Unknown'))
            st.metric("🏛️ Region", server_data.get('region', 'Unknown'))
            st.metric("🏙️ City", server_data.get('city', 'Unknown'))
        
        with col2:
            st.metric("📮 ZIP Code", server_data.get('postal', 'Unknown'))
            st.metric("🕒 Timezone", server_data.get('timezone', 'Unknown'))
            st.metric("🌐 ISP", server_data.get('org', 'Unknown'))
            st.metric("📍 Coordinates", f"{server_data.get('latitude', 'N/A')}, {server_data.get('longitude', 'N/A')}")
        
        with st.expander("🔍 View All Server Data"):
            st.json(server_data)
            
        st.info("⚠️ **Note**: This shows your server's public IP (where Streamlit app is hosted), not your client IP.")
    
    else:
        st.error("❌ Server-side detection failed")
        server_data = None

except Exception as e:
    st.error(f"❌ Server-side detection error: {str(e)}")
    server_data = None

st.divider()

# Method 2: Simple client-side approach
st.subheader("💻 Client-side IP Detection")

# Very simple JavaScript - just get IP
simple_js = """
fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => data.ip)
    .catch(error => null);
"""

if st.button("🔍 Get My Client IP", type="primary"):
    with st.spinner('Fetching your client IP...'):
        client_ip = st_javascript(simple_js, key="simple_ip")
        
        if client_ip and client_ip != "null":
            st.success(f"✅ Your client IP address: **{client_ip}**")
            
            # Try to get location data for the client IP server-side
            try:
                location_response = requests.get(f'https://ipapi.co/{client_ip}/json/', timeout=10)
                if location_response.status_code == 200:
                    location_data = location_response.json()
                    
                    st.subheader("📍 Client IP Location Details")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🏳️ Country", location_data.get('country_name', 'Unknown'))
                        st.metric("🏛️ Region", location_data.get('region', 'Unknown'))
                        st.metric("🏙️ City", location_data.get('city', 'Unknown'))
                        st.metric("📮 ZIP Code", location_data.get('postal', 'Unknown'))
                    
                    with col2:
                        st.metric("🕒 Timezone", location_data.get('timezone', 'Unknown'))
                        st.metric("🌐 ISP", location_data.get('org', 'Unknown'))
                        st.metric("📍 Latitude", location_data.get('latitude', 'Unknown'))
                        st.metric("📍 Longitude", location_data.get('longitude', 'Unknown'))
                    
                    with st.expander("🔍 View All Client Location Data"):
                        st.json(location_data)
                
            except Exception as e:
                st.warning(f"⚠️ Could not fetch location details: {str(e)}")
        else:
            st.error("❌ Could not fetch client IP")

st.divider()

# Method 3: Alternative services
st.subheader("🔄 Alternative Services")

col1, col2 = st.columns(2)

with col1:
    if st.button("Try ipinfo.io"):
        try:
            response = requests.get('https://ipinfo.io/json', timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ ipinfo.io response:")
                st.json(data)
            else:
                st.error("❌ Failed to fetch from ipinfo.io")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with col2:
    if st.button("Try ip-api.com"):
        try:
            response = requests.get('https://ip-api.com/json/', timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ ip-api.com response:")
                st.json(data)
            else:
                st.error("❌ Failed to fetch from ip-api.com")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Instructions
st.divider()
st.markdown("""
### 📝 How this works:

1. **Server-side Detection**: Shows the IP of the Streamlit server (automatic)
2. **Client-side Detection**: Uses JavaScript to get YOUR actual IP address (click button)
3. **Alternative Services**: Test different IP detection services

### 🔍 Understanding the Results:

- **Server IP**: The IP where your Streamlit app is hosted
- **Client IP**: Your actual public IP address (more useful)
- **Location Data**: Based on IP geolocation (may not be 100% accurate)

### ⚠️ Troubleshooting:

If client-side detection fails:
- Your network/firewall might block the requests
- Browser security policies might prevent the JavaScript
- Try the alternative services to see which ones work
""")

st.info("🔒 **Privacy**: This app doesn't store or log any of your IP information.")
