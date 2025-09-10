import streamlit as st
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

# --- Usage ---
ip = get_user_ip_javascript()
st.write("Your IP is:", ip)
