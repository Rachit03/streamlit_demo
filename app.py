import streamlit as st
from streamlit_javascript import st_javascript
import time

st.title("Client IP Address & Location Details")

# Simple and reliable JavaScript code
js_code = """
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

fetch('https://ipapi.co/json/', {
    signal: controller.signal,
    method: 'GET',
    headers: {
        'Accept': 'application/json',
    }
})
.then(response => {
    clearTimeout(timeoutId);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    return {
        ip: data.ip || 'Unknown',
        country: data.country_name || 'Unknown',
        countryCode: data.country_code || 'Unknown',
        region: data.region || 'Unknown',
        city: data.city || 'Unknown',
        zip: data.postal || 'Unknown',
        latitude: data.latitude || 'Unknown',
        longitude: data.longitude || 'Unknown',
        timezone: data.timezone || 'Unknown',
        isp: data.org || 'Unknown'
    };
})
.catch(error => {
    clearTimeout(timeoutId);
    console.error('Primary service failed, trying fallback...');
    
    // Fallback to ipify for just IP
    return fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => ({
            ip: data.ip || 'Unknown',
            country: 'Limited service',
            countryCode: 'N/A',
            region: 'N/A',
            city: 'Limited service',
            zip: 'N/A',
            latitude: 'N/A',
            longitude: 'N/A',
            timezone: 'N/A',
            isp: 'N/A'
        }))
        .catch(fallbackError => {
            console.error('All services failed:', fallbackError);
            return {
                ip: 'Unable to fetch',
                country: 'Error',
                countryCode: 'Error',
                region: 'Error',
                city: 'Error',
                zip: 'Error',
                latitude: 'Error',
                longitude: 'Error',
                timezone: 'Error',
                isp: 'Error'
            };
        });
});
"""

# Initialize session state to track loading
if 'ip_data_loaded' not in st.session_state:
    st.session_state.ip_data_loaded = False

# Button to fetch data
if st.button("🔍 Get My IP Details", type="primary"):
    st.session_state.ip_data_loaded = False
    
    with st.spinner('🌐 Fetching your IP address and location details...'):
        # Execute JavaScript
        ip_details = st_javascript(js_code, key=f"ip_fetch_{int(time.time())}")
        
        # Small delay to ensure JavaScript execution
        time.sleep(1)
        
        # Check if we got valid data
        if ip_details and isinstance(ip_details, dict) and ip_details.get('ip') and ip_details['ip'] not in ['Unknown', 'Unable to fetch', '']:
            st.session_state.ip_details = ip_details
            st.session_state.ip_data_loaded = True
        else:
            st.error("❌ Unable to fetch IP details. This might be due to network restrictions or browser security policies.")
            st.info("💡 Try refreshing the page or checking your internet connection.")

# Display results if available
if st.session_state.get('ip_data_loaded') and 'ip_details' in st.session_state:
    ip_details = st.session_state.ip_details
    
    st.success("✅ IP details fetched successfully!")
    
    # Main IP display
    st.markdown(f"### 📍 Your IP Address: `{ip_details['ip']}`")
    
    # Create tabs for different categories of information
    tab1, tab2, tab3 = st.tabs(["🌍 Location", "📡 Network", "📊 Technical"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏳️ Country", ip_details['country'])
            st.metric("🏛️ Region/State", ip_details['region'])
            st.metric("🏙️ City", ip_details['city'])
        with col2:
            st.metric("📮 ZIP/Postal Code", ip_details['zip'])
            st.metric("🕒 Timezone", ip_details['timezone'])
            st.metric("🗺️ Country Code", ip_details['countryCode'])
    
    with tab2:
        st.metric("🌐 ISP/Organization", ip_details['isp'])
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📍 Latitude", ip_details['latitude'])
        with col2:
            st.metric("📍 Longitude", ip_details['longitude'])
    
    # Raw data expandable section
    with st.expander("🔍 View Raw JSON Data"):
        st.json(ip_details)
        
    # Add a note about data source
    st.info("ℹ️ Location data is provided by IP geolocation services and may not be 100% accurate.")

# Instructions
if not st.session_state.get('ip_data_loaded'):
    st.markdown("""
    ### 📝 Instructions:
    1. Click the **"Get My IP Details"** button above to fetch your information
    2. The app will detect your public IP address and location details
    3. Results will be displayed in organized tabs below
    
    **Note**: Location accuracy depends on your ISP and may show your ISP's location rather than your exact location.
    """)

# Add some spacing
st.markdown("---")
st.markdown("*This app respects your privacy - no data is stored or logged.*")
