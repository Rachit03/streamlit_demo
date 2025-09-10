import streamlit as st
import streamlit.components.v1 as components
import requests
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="User IP Detection",
    page_icon="🌐",
    layout="wide"
)

# def get_user_ip_javascript():
#     """Method 1: Get user IP using JavaScript and external API"""
#     html_code = """
#     <div style="padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
#         <h4>🔍 Detecting Your IP Address...</h4>
#         <div id="ip-result">Loading...</div>
#     </div>
    
#     <script>
#     async function fetchUserIP() {
#         try {
#             // Try multiple IP detection services for reliability
#             const services = [
#                 'https://api.ipify.org?format=json',
#                 'https://ipapi.co/json/',
#                 'https://ip-api.com/json/'
#             ];
            
#             let ipInfo = null;
            
#             for (const service of services) {
#                 try {
#                     const response = await fetch(service);
#                     const data = await response.json();
                    
#                     if (service.includes('ipify')) {
#                         ipInfo = { ip: data.ip };
#                     } else if (service.includes('ipapi.co')) {
#                         ipInfo = {
#                             ip: data.ip,
#                             city: data.city,
#                             region: data.region,
#                             country: data.country_name,
#                             timezone: data.timezone
#                         };
#                     } else if (service.includes('ip-api')) {
#                         ipInfo = {
#                             ip: data.query,
#                             city: data.city,
#                             region: data.regionName,
#                             country: data.country,
#                             timezone: data.timezone
#                         };
#                     }
                    
#                     break; // Success, exit loop
#                 } catch (error) {
#                     console.log(`Service ${service} failed:`, error);
#                     continue; // Try next service
#                 }
#             }
            
#             if (ipInfo) {
#                 let resultHTML = `<strong>✅ Your IP Address: ${ipInfo.ip}</strong><br>`;
                
#                 if (ipInfo.city && ipInfo.country) {
#                     resultHTML += `📍 Location: ${ipInfo.city}, ${ipInfo.region}, ${ipInfo.country}<br>`;
#                 }
#                 if (ipInfo.timezone) {
#                     resultHTML += `🕐 Timezone: ${ipInfo.timezone}`;
#                 }
                
#                 document.getElementById('ip-result').innerHTML = resultHTML;
                
#                 // Send data back to Streamlit
#                 window.parent.postMessage({
#                     type: 'streamlit:setComponentValue',
#                     value: ipInfo
#                 }, '*');
#             } else {
#                 throw new Error('All IP detection services failed');
#             }
            
#         } catch (error) {
#             console.error('Error fetching IP:', error);
#             document.getElementById('ip-result').innerHTML = 
#                 '<strong>❌ Error:</strong> Unable to detect IP address. Please check your internet connection.';
            
#             window.parent.postMessage({
#                 type: 'streamlit:setComponentValue',
#                 value: { error: 'Unable to fetch IP' }
#             }, '*');
#         }
#     }
    
#     // Execute when page loads
#     fetchUserIP();
#     </script>
#     """
    
#     result = components.html(html_code, height=200)
#     return result
import streamlit.components.v1 as components

def get_user_ip_javascript():
    """Return only user IP using JavaScript"""
    html_code = """
    <script>
    async function fetchUserIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            
            // Send only IP back to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: data.ip
            }, '*');
        } catch (error) {
            console.error('Error fetching IP:', error);
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: null
            }, '*');
        }
    }
    fetchUserIP();
    </script>
    """
    return components.html(html_code, height=0, width=0)

def get_user_ip_server_side():
    """Method 2: Server-side IP detection (may show server IP if behind proxy)"""
    try:
        # This gets the IP as seen by the external service
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return "Unable to fetch IP"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def get_detailed_ip_info(ip_address):
    """Get detailed information about an IP address"""
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def main():
    st.title("🌐 User IP Address Detection")
    st.markdown("---")
    
    # Create tabs for different methods
    tab1, tab2, tab3 = st.tabs(["🎯 Client-Side Detection", "🖥️ Server-Side Detection", "📊 IP Analytics"])
    
    with tab1:
        st.header("Method 1: JavaScript Client-Side Detection")
        st.info("This method runs JavaScript in your browser to get your actual IP address.")
        
        # Get user IP using JavaScript
        user_ip_data = get_user_ip_javascript()
        st.write("Your IP is:", user_ip_data)
        if user_ip_data and isinstance(user_ip_data, dict) and 'ip' in user_ip_data:
            st.success("✅ Successfully detected your IP!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Your IP Address", user_ip_data['ip'])
                if 'country' in user_ip_data:
                    st.metric("Country", user_ip_data['country'])
            
            with col2:
                if 'city' in user_ip_data and user_ip_data['city']:
                    st.metric("City", user_ip_data['city'])
                if 'timezone' in user_ip_data:
                    st.metric("Timezone", user_ip_data['timezone'])
            
            # Store in session state for other tabs
            st.session_state['detected_ip'] = user_ip_data['ip']
    
    with tab2:
        st.header("Method 2: Server-Side Detection")
        st.warning("⚠️ This method may show the server's IP if the app is behind a proxy/load balancer.")
        
        if st.button("🔍 Detect IP (Server-Side)", type="primary"):
            with st.spinner("Detecting IP..."):
                server_ip = get_user_ip_server_side()
                st.code(f"Detected IP: {server_ip}")
                
                if server_ip and not server_ip.startswith("Error") and not server_ip.startswith("Unable"):
                    st.session_state['server_detected_ip'] = server_ip
    
    with tab3:
        st.header("📊 Detailed IP Analysis")
        
        # IP input for manual analysis
        manual_ip = st.text_input("🔍 Enter IP Address for Analysis:", 
                                placeholder="e.g., 8.8.8.8")
        
        # Use detected IP if available
        ip_to_analyze = None
        if manual_ip:
            ip_to_analyze = manual_ip
        elif 'detected_ip' in st.session_state:
            ip_to_analyze = st.session_state['detected_ip']
            st.info(f"Using detected IP: {ip_to_analyze}")
        
        if st.button("📈 Analyze IP", type="primary") and ip_to_analyze:
            with st.spinner("Analyzing IP address..."):
                ip_details = get_detailed_ip_info(ip_to_analyze)
                
                if ip_details:
                    st.success("✅ Analysis Complete!")
                    
                    # Create columns for better layout
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("🌍 Location Info")
                        st.write(f"**IP:** {ip_details.get('ip', 'N/A')}")
                        st.write(f"**City:** {ip_details.get('city', 'N/A')}")
                        st.write(f"**Region:** {ip_details.get('region', 'N/A')}")
                        st.write(f"**Country:** {ip_details.get('country_name', 'N/A')}")
                        st.write(f"**Postal Code:** {ip_details.get('postal', 'N/A')}")
                    
                    with col2:
                        st.subheader("🌐 Network Info")
                        st.write(f"**ISP:** {ip_details.get('org', 'N/A')}")
                        st.write(f"**ASN:** {ip_details.get('asn', 'N/A')}")
                        st.write(f"**Timezone:** {ip_details.get('timezone', 'N/A')}")
                        st.write(f"**Currency:** {ip_details.get('currency', 'N/A')}")
                    
                    with col3:
                        st.subheader("📍 Coordinates")
                        if ip_details.get('latitude') and ip_details.get('longitude'):
                            st.write(f"**Latitude:** {ip_details.get('latitude')}")
                            st.write(f"**Longitude:** {ip_details.get('longitude')}")
                            
                            # Show map if coordinates are available
                            try:
                                import pandas as pd
                                map_data = pd.DataFrame({
                                    'lat': [float(ip_details.get('latitude'))],
                                    'lon': [float(ip_details.get('longitude'))]
                                })
                                st.map(map_data)
                            except (ValueError, ImportError):
                                st.write("Map visualization not available")
                        else:
                            st.write("Coordinates not available")
                    
                    # Show raw JSON data
                    with st.expander("🔍 Raw IP Data (JSON)"):
                        st.json(ip_details)
                else:
                    st.error("❌ Failed to analyze IP address. Please try again.")
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### 📝 How it works:
    
    1. **Client-Side Detection**: Uses JavaScript to call external IP detection APIs from your browser
    2. **Server-Side Detection**: Makes API calls from the server (may show server IP if behind proxy)
    3. **IP Analysis**: Provides detailed geolocation and network information about any IP address
    
    ### 🔒 Privacy Note:
    This app uses external services to detect IP addresses. Your IP address is temporarily processed but not stored permanently.
    """)
    
    # Current timestamp
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
