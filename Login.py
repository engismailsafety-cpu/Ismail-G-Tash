# app.py (جزء من الكود)

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from report_generator import generate_pdf_report
from sustainability_analysis import analyze_sustainability

# ========== LOGIN ==========
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>🌱 Sustainability AI Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>GRI Standards | ESG Integration</p>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.stop()

check_password()

# ========== MAIN UI ==========
st.set_page_config(page_title="Sustainability AI Agent", layout="wide")
st.title("🌱 Sustainability Report Analysis")
st.caption("AI Agent | GRI Standards | ESG Integration")

st.markdown("---")
st.markdown("**Team Leader:** Ismail Kamal | **Under Supervision:** Dr. Mohamed Tash")
st.markdown("**QHSE Master at Alexandria University**")
st.markdown("**Team Members:** Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh")
st.markdown("---")

# Upload section
uploaded_files = st.file_uploader("Upload Excel, CSV, PDF, Word, Images", 
                                   type=["xlsx", "csv", "pdf", "docx", "jpg", "png"], 
                                   accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully")
    
    if st.button("🔍 Run AI Sustainability Analysis"):
        with st.spinner("AI Agent analyzing data, images, and text..."):
            results = analyze_sustainability(uploaded_files)
        
        # Display results
        st.subheader("📊 Carbon Footprint")
        st.metric("Total CO₂ (tons)", f"{results['co2']:.2f}")
        
        st.subheader("🔮 Predictions")
        st.line_chart(results["predictions"])
        
        st.subheader("🖼️ Image Analysis")
        for img_res in results["image_results"]:
            st.write(f"- {img_res['label']}: {img_res['confidence']:.2f}")
        
        st.subheader("📄 Text Classification (GRI)")
        st.json(results["gri_mapping"])
        
        # PDF Report
        if st.button("📑 Generate Full PDF Report"):
            pdf_path = generate_pdf_report(results)
            with open(pdf_path, "rb") as f:
                st.download_button("Download Report", f, file_name="sustainability_report.pdf")