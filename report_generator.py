from fpdf import FPDF
import pandas as pd
from datetime import datetime
import io

class PDFReportGenerator:
    def __init__(self):
        self.pdf = None
    
    def generate_report(self, results):
        self.pdf = FPDF()
        self.pdf.add_page()
        
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "Sustainability Report", ln=True, align="C")
        self.pdf.set_font("Arial", "I", 10)
        self.pdf.cell(0, 10, f"Generated: {results['timestamp']}", ln=True, align="C")
        self.pdf.ln(10)
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Team Information", ln=True)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 6, "Team Leader: Ismail Kamal", ln=True)
        self.pdf.cell(0, 6, "Supervisor: Dr. Mohamed Tash", ln=True)
        self.pdf.cell(0, 6, "Program: QHSE Master - Alexandria University", ln=True)
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Executive Summary", ln=True)
        self.pdf.set_font("Arial", "", 10)
        summary = "This report presents a comprehensive sustainability analysis using AI-driven methods. "
        summary += f"Total carbon footprint: {results['analysis'].get('co2_total', 0):.2f} tCO₂e. "
        summary += f"Energy consumption: {results['analysis'].get('energy_total', 0):.2f} MWh. "
        self.pdf.multi_cell(0, 6, summary)
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Key Performance Indicators", ln=True)
        
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(80, 8, "Metric", 1)
        self.pdf.cell(80, 8, "Value", 1)
        self.pdf.ln()
        
        self.pdf.set_font("Arial", "", 10)
        metrics = [
            ("Carbon Footprint (tCO₂e)", f"{results['analysis'].get('co2_total', 0):.2f}"),
            ("Energy Consumption (MWh)", f"{results['analysis'].get('energy_total', 0):.2f}"),
            ("Water Usage (m³)", f"{results['analysis'].get('water_total', 0):.2f}"),
            ("Waste Generated (tons)", f"{results['analysis'].get('waste_total', 0):.2f}"),
            ("Carbon Intensity (kgCO₂e/MWh)", f"{results['analysis'].get('carbon_intensity', 0):.2f}"),
            ("Energy Efficiency (%)", f"{results['analysis'].get('energy_efficiency', 0):.2f}")
        ]
        
        for metric, value in metrics:
            self.pdf.cell(80, 8, metric, 1)
            self.pdf.cell(80, 8, value, 1)
            self.pdf.ln()
        
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "AI Agent Insights & Recommendations", ln=True)
        self.pdf.set_font("Arial", "", 10)
        recommendations = [
            "1. Implement renewable energy sources to reduce carbon emissions by 30%",
            "2. Install water recycling systems to reduce freshwater withdrawal",
            "3. Adopt waste-to-energy technologies for circular economy",
            "4. Enhance monitoring systems for real-time sustainability tracking",
            "5. Set science-based targets for emissions reduction"
        ]
        
        for rec in recommendations:
            self.pdf.cell(0, 6, rec, ln=True)
        
        self.pdf.ln(5)
        
        if 'predictions' in results:
            self.pdf.set_font("Arial", "B", 12)
            self.pdf.cell(0, 10, "Sustainability Forecast", ln=True)
            self.pdf.set_font("Arial", "", 10)
            self.pdf.cell(0, 6, "Energy and emissions forecasts for 2025-2030:", ln=True)
            self.pdf.ln(3)
            
            self.pdf.set_font("Arial", "B", 9)
            self.pdf.cell(40, 7, "Year", 1)
            self.pdf.cell(70, 7, "Energy Forecast (MWh)", 1)
            self.pdf.cell(70, 7, "Emissions Forecast (tCO₂e)", 1)
            self.pdf.ln()
            
            self.pdf.set_font("Arial", "", 9)
            for year, energy, emissions in zip(
                results['predictions']['years'],
                results['predictions']['energy_forecast'],
                results['predictions']['emissions_forecast']
            ):
                self.pdf.cell(40, 7, str(int(year)), 1)
                self.pdf.cell(70, 7, f"{energy:.1f}", 1)
                self.pdf.cell(70, 7, f"{emissions:.1f}", 1)
                self.pdf.ln()
        
        self.pdf.ln(5)
        
        self.pdf.set_y(-15)
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.cell(0, 10, f"Page {self.pdf.page_no()} | QHSE Master - Alexandria University | AI Sustainability Agent", 0, 0, "C")
        
        output_path = f"sustainability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.pdf.output(output_path)
        
        return output_path
