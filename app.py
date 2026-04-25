import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

from sustainability_analysis import SustainabilityAnalyzer
from report_generator import PDFReportGenerator
from image_analyzer import ImageAnalyzer
from text_classifier import TextClassifier

st.set_page_config(
    page_title="Sustainability AI Agent",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    .insight-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #1e3c72;
        color: white;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = SustainabilityAnalyzer()
    if 'results' not in st.session_state:
        st.session_state.results = None

init_session_state()

def check_password():
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 3rem; background: white; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h1 style='color: #1e3c72;'>🌱 Sustainability AI Agent</h1>
                <p style='color: #666;'>GRI Standards | ESG Integration | QHSE Master</p>
                <hr>
                <h3>🔐 Login</h3>
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Login", use_container_width=True):
                    if username == "admin" and password == "1234":
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
        st.stop()

check_password()

st.markdown(f"""
<div class='main-header'>
    <h1>🌱 Sustainability AI Agent</h1>
    <p>Advanced Analytics | GRI Standards | ESG Integration | AI-Powered Insights</p>
    <hr>
    <p><strong>🏆 Team Leader:</strong> Ismail Kamal | <strong>👨‍🏫 Under Supervision:</strong> Dr. Mohamed Tash</p>
    <p><strong>📚 QHSE Master - Alexandria University</strong></p>
    <p><strong>👥 Team Members:</strong> Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sustainability.png", width=80)
    st.markdown("## 📂 Data Upload")
    uploaded_files = st.file_uploader(
        "Upload your files",
        type=["xlsx", "csv", "pdf", "docx", "jpg", "png", "jpeg"],
        accept_multiple_files=True,
        help="Upload Excel, CSV, PDF, Word documents, or images"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    analysis_type = st.multiselect(
        "Select Analysis Type",
        ["Carbon Footprint", "Energy Efficiency", "Water Management", "Waste Analysis", "Image Analysis", "Text Mining"],
        default=["Carbon Footprint", "Energy Efficiency", "Water Management"]
    )
    
    forecast_years = st.slider("Forecast Years", 1, 10, 5)
    
    st.markdown("---")
    st.markdown("### 📊 GRI Standards")
    gri_standards = st.multiselect(
        "Select GRI Standards",
        ["GRI 302: Energy", "GRI 303: Water", "GRI 305: Emissions", "GRI 306: Waste", "GRI 403: Occupational Health"],
        default=["GRI 302: Energy", "GRI 305: Emissions"]
    )

if uploaded_files:
    if st.button("🚀 Run Complete Sustainability Analysis", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Agent is analyzing your data..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📊 Step 1/5: Extracting data from files...")
            progress_bar.progress(20)
            
            results = st.session_state.analyzer.analyze_all(uploaded_files, analysis_type)
            progress_bar.progress(40)
            
            status_text.text("🖼️ Step 2/5: Analyzing images...")
            image_analyzer = ImageAnalyzer()
            image_files = [f for f in uploaded_files if f.type in ['image/jpeg', 'image/png', 'image/jpg']]
            image_results = image_analyzer.analyze_images(image_files)
            progress_bar.progress(60)
            
            status_text.text("📄 Step 3/5: Classifying text against GRI standards...")
            text_classifier = TextClassifier()
            doc_files = [f for f in uploaded_files if f.type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']]
            text_results = text_classifier.classify_documents(doc_files)
            progress_bar.progress(80)
            
            status_text.text("🔮 Step 4/5: Generating forecasts...")
            predictions = st.session_state.analyzer.generate_predictions(forecast_years)
            progress_bar.progress(100)
            
            status_text.text("✅ Analysis complete!")
            
            st.session_state.results = {
                "analysis": results,
                "image_analysis": image_results,
                "text_classification": text_results,
                "predictions": predictions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    if st.session_state.results:
        results_data = st.session_state.results
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🖼️ Image Analysis", "📄 Text Mining", "🔮 Forecasts", "📑 Report"])
        
        with tab1:
            st.markdown("## 📊 Sustainability Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>🌍 Carbon Footprint</h3>
                    <h2>{results_data['analysis'].get('co2_total', 0):.2f} tCO₂e</h2>
                    <small>Scope 1 & 2 emissions</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>⚡ Energy Consumption</h3>
                    <h2>{results_data['analysis'].get('energy_total', 0):.2f} MWh</h2>
                    <small>Total energy used</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>💧 Water Usage</h3>
                    <h2>{results_data['analysis'].get('water_total', 0):.2f} m³</h2>
                    <small>Total water withdrawal</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>🗑️ Waste Generated</h3>
                    <h2>{results_data['analysis'].get('waste_total', 0):.2f} tons</h2>
                    <small>Total waste</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 🤖 AI Agent Insights")
            st.markdown(f"""
            <div class='insight-box'>
                <strong>📈 Key Findings:</strong><br>
                • Carbon intensity: {results_data['analysis'].get('carbon_intensity', 0):.2f} kgCO₂e/MWh<br>
                • Energy efficiency: {results_data['analysis'].get('energy_efficiency', 0):.2f}%<br>
                • Water recycling rate: {results_data['analysis'].get('water_recycling', 0):.2f}%<br><br>
                <strong>💡 Recommendations:</strong><br>
                • Implement renewable energy sources to reduce emissions by 30%<br>
                • Install water treatment facilities for recycling<br>
                • Adopt waste-to-energy technologies
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("## 🖼️ Image Analysis Results")
            if results_data['image_analysis']:
                for img_res in results_data['image_analysis']:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if 'image' in img_res:
                            st.image(img_res['image'], caption=img_res['filename'], width=200)
                    with col2:
                        st.markdown(f"**File:** {img_res['filename']}")
                        st.markdown(f"**Classification:** {img_res['classification']}")
                        st.markdown(f"**Confidence:** {img_res['confidence']:.2%}")
                        if img_res.get('green_area_percentage'):
                            st.markdown(f"**🌿 Green Area:** {img_res['green_area_percentage']:.1f}%")
                        if img_res.get('pollution_index'):
                            st.markdown(f"**⚠️ Pollution Index:** {img_res['pollution_index']:.2f}")
                    st.markdown("---")
            else:
                st.info("No images uploaded for analysis")
        
        with tab3:
            st.markdown("## 📄 Text Mining & GRI Classification")
            if results_data['text_classification']:
                for doc in results_data['text_classification']:
                    st.markdown(f"### 📁 {doc['filename']}")
                    st.markdown("**GRI Standards Mapping:**")
                    gri_df = pd.DataFrame(doc['gri_scores'].items(), columns=['Standard', 'Confidence'])
                    fig = px.bar(gri_df, x='Standard', y='Confidence', title="GRI Alignment")
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"**Sentiment Analysis:** {doc['sentiment']} (Score: {doc['sentiment_score']:.2f})")
                    st.markdown("---")
            else:
                st.info("No text documents uploaded for analysis")
        
        with tab4:
            st.markdown("## 🔮 AI Forecasts & Predictions")
            if results_data['predictions']:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=results_data['predictions']['years'],
                    y=results_data['predictions']['energy_forecast'],
                    mode='lines+markers',
                    name='Energy Forecast',
                    line=dict(color='#1e3c72', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=results_data['predictions']['years'],
                    y=results_data['predictions']['emissions_forecast'],
                    mode='lines+markers',
                    name='Emissions Forecast',
                    line=dict(color='#dc2626', width=3)
                ))
                fig.update_layout(
                    title="Sustainability Forecast (2025-2030)",
                    xaxis_title="Year",
                    yaxis_title="Value",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Generate forecasts by running analysis first")
        
        with tab5:
            st.markdown("## 📑 Generate Comprehensive Report")
            if st.button("Generate Report", type="primary"):
                with st.spinner("Generating professional report..."):
                    generator = PDFReportGenerator()
                    pdf_path = generator.generate_report(st.session_state.results)
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    st.success("✅ Report generated successfully!")
                    st.download_button(
                        label="📥 Download Sustainability Report",
                        data=pdf_bytes,
                        file_name=f"sustainability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
else:
    st.info("👈 Please upload files from the sidebar to begin the sustainability analysis")

st.markdown("""
<footer>
    <p>🌱 Sustainability AI Agent | Developed by Ismail Kamal & Team | QHSE Master - Alexandria University | Under Supervision of Dr. Mohamed Tash</p>
</footer>
""", unsafe_allow_html=True)
