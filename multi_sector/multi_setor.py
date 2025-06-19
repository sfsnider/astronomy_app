import streamlit as st
import matplotlib.pyplot as plt
import lightkurve as lk
import astroquery  
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
import astropy.units as u        
from astroquery.simbad import Simbad
import pandas as pd

st.set_page_config(page_title="Multi Sector Light Curve Viewer", layout="wide")
st.title("🪐  Multi Sector Light Curve Viewer")


st.text("This app allows you to view light curves from multiple sectors of the TESS mission. " )
st.text("You can select the sectors you want to view and see their light curves side by side.")

# Insert containers separated into tabs:
tabs = st.tabs(["🔭 Search    ", "📊 Analytics", "⚙️ Settings"])

# Home Page Tab
with tabs[0]:
    st.header("🔭 Search")
    st.write("Welcome to the home page inside a tab.")
    st.image("https://placekitten.com/400/300", caption="Just a kitten")

# Analytics Page Tab
with tabs[1]:
    st.header("📊 Analytics Page")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Users", value="1,234", delta="+3%")
    with col2:
        st.metric(label="Revenue", value="$12.4K", delta="-1.2%")

# Settings Page Tab
with tabs[2]:
    st.header("⚙️ Settings Page")
    username = st.text_input("Change username")
    notifications = st.checkbox("Enable notifications")
    if st.button("Save Settings"):
        st.success("Settings saved.")
