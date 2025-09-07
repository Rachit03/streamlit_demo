import streamlit as st
from streamlit_javascript import st_javascript
import json

st.title("Client IP Address & Location Details")

# Enhanced JavaScript code to fetch IP and location details
js_code = """
async function getIPDetails() {
    try {
        // First get the IP address
        const ipResponse = await fetch('https://api.ipify.org?format=json');
        const ipData = await ipResponse.json();
        const ip = ipData.ip;
        
        // Then get location details using the IP
        const locationResponse = await fetch(`http://ip-api.com/json/${ip}`);
        const locationData = await locationResponse.json();
        
        // Return combined data
        return {
            ip: ip,
            country: locationData.country || 'Unknown',
            countryCode: locationData.countryCode || 'Unknown',
            region: locationData.region || 'Unknown',
            regionName: locationData.regionName || 'Unknown',
            city: locationData.city || 'Unknown',
            zip: locationData.zip || 'Unknown',
            latitude: locationData.lat || 'Unknown',
            longitude: locationData.lon || 'Unknown',
            timezone: locationData.timezone || 'Unknown',
            isp: locationData.isp || 'Unknown',
            org: locationData.org || 'Unknown',
            as: locationData.as || 'Unknown'
        };
    } catch (error) {
        console.error('Error fetching IP details:', error);
        return {
            ip: 'Error fetching IP',
            country: 'Error',
            countryCode: 'Error',
            region: 'Error',
            regionName: 'Error',
            city: 'Error',
            zip: 'Error',
            latitude: 'Error',
            longitude: 'Error',
            timezone: 'Error',
            isp: 'Error',
            org: 'Error',
            as: 'Error'
        };
    }
}

return await getIPDetails();
"""

# Execute JavaScript and wait for response
with st.spinner('Fetching your IP address and location details...'):
    ip_details = st_javascript(js_code)

# Display results only when data is available
if ip_details and isinstance(ip_details, dict) and ip_details.get('ip'):
    st.success("✅ Details fetched successfully!")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Location Information")
        st.write(f"**IP Address:** {ip_details['ip']}")
        st.write(f"**Country:** {ip_details['country']} ({ip_details['countryCode']})")
        st.write(f"**State/Region:** {ip_details['regionName']} ({ip_details['region']})")
        st.write(f"**City:** {ip_details['city']}")
        st.write(f"**ZIP Code:** {ip_details['zip']}")
        st.write(f"**Timezone:** {ip_details['timezone']}")
    
    with col2:
        st.subheader("🌐 Network Information")
        st.write(f"**ISP:** {ip_details['isp']}")
        st.write(f"**Organization:** {ip_details['org']}")
        st.write(f"**AS:** {ip_details['as']}")
        st.write(f"**Latitude:** {ip_details['latitude']}")
        st.write(f"**Longitude:** {ip_details['longitude']}")
    
    # Optional: Show raw data in expander
    with st.expander("🔍 View Raw Data"):
        st.json(ip_details)
        
elif ip_details is None:
    st.info("⏳ Loading IP details... Please wait.")
else:
    st.error("❌ Failed to fetch IP details. Please refresh the page to try again.")
