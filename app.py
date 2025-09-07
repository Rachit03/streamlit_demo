import streamlit as st
from streamlit_javascript import st_javascript

st.set_page_config(page_title="IP & Location Info", layout="centered")
st.title("Client IP & Location Details")

with st.spinner("Fetching your IP and location info..."):
    geo_data = st_javascript("""
        await fetch('https://ipapi.co/json/')
            .then(res => res.json())
            .then(data => data)
    """)

if geo_data and isinstance(geo_data, dict) and "ip" in geo_data:
    st.success("Successfully fetched your IP and location information.")

    st.subheader("📍 Your Info")
    st.markdown(f"- **IP Address**: `{geo_data['ip']}`")
    st.markdown(f"- **Country**: `{geo_data['country_name']}`")
    st.markdown(f"- **Region/State**: `{geo_data['region']}`")
    st.markdown(f"- **City**: `{geo_data['city']}`")
    st.markdown(f"- **Latitude**: `{geo_data['latitude']}`")
    st.markdown(f"- **Longitude**: `{geo_data['longitude']}`")

    # Optional: Show location on map
    st.map({
        "lat": [geo_data["latitude"]],
        "lon": [geo_data["longitude"]]
    })

else:
    st.error("Could not fetch location details.")
