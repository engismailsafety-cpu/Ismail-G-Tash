from fpdf import FPDF
import plotly.io as pio
import pandas as pd
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Sustainability Report - AI Agent", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | QHSE Master - Alexandria University", 0, 0, "C")

def generate_pdf_report(results):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    pdf.cell(0, 10, f"Report Date: {datetime.now().strftime('%Y-%m-%d')}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Carbon Footprint", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Total CO2 emissions: {results['co2']:.2f} tons", 0, 1)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Predictions (2025-2030)", 0, 1)
    pdf.set_font("Arial", size=10)
    for year, val in results["predictions"].items():
        pdf.cell(0, 8, f"{year}: {val:.1f} units", 0, 1)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. GRI Standards Mapping", 0, 1)
    pdf.set_font("Arial", size=8)
    for file, mapping in results["gri_mapping"].items():
        pdf.cell(0, 8, f"- {file}: {mapping}", 0, 1)
    
    pdf.output("sustainability_report.pdf")
    return "sustainability_report.pdf"