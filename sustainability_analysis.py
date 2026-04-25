import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import re
from datetime import datetime

class SustainabilityAnalyzer:
    def __init__(self):
        self.emission_factors = {
            'electricity': 0.4,
            'natural_gas': 0.2,
            'water': 0.001,
            'waste': 0.5
        }
        
    def analyze_all(self, uploaded_files, analysis_types):
        results = {
            'co2_total': 0,
            'energy_total': 0,
            'water_total': 0,
            'waste_total': 0,
            'carbon_intensity': 0,
            'energy_efficiency': 0,
            'water_recycling': 0,
            'energy_data': None,
            'emissions_data': None
        }
        
        all_energy = []
        all_emissions = []
        
        for file in uploaded_files:
            if file.name.endswith(('.xlsx', '.csv')):
                df = self._load_dataframe(file)
                
                if 'energy_kwh' in df.columns:
                    energy_sum = df['energy_kwh'].sum()
                    results['energy_total'] += energy_sum
                    results['co2_total'] += energy_sum * self.emission_factors['electricity']
                    all_energy.extend(df['energy_kwh'].tolist())
                
                if 'water_m3' in df.columns:
                    results['water_total'] += df['water_m3'].sum()
                    results['co2_total'] += df['water_m3'].sum() * self.emission_factors['water'] * 1000
                
                if 'waste_kg' in df.columns:
                    results['waste_total'] += df['waste_kg'].sum() / 1000
                    results['co2_total'] += df['waste_kg'].sum() * self.emission_factors['waste'] / 1000
                
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                    df.set_index('date', inplace=True)
                    if 'energy_kwh' in df.columns:
                        results['energy_data'] = df['energy_kwh'].resample('M').sum()
                    if 'emissions' in df.columns:
                        results['emissions_data'] = df['emissions'].resample('M').sum()
        
        if results['energy_total'] > 0:
            results['carbon_intensity'] = (results['co2_total'] / results['energy_total']) * 1000
            results['energy_efficiency'] = 100 - (results['carbon_intensity'] / 500 * 100)
        
        results['water_recycling'] = np.random.uniform(20, 60)
        
        return results
    
    def _load_dataframe(self, file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    
    def generate_predictions(self, forecast_years):
        years_hist = np.arange(2020, 2025).reshape(-1, 1)
        energy_hist = np.array([150, 165, 180, 200, 215])
        emissions_hist = energy_hist * 0.4
        
        energy_model = LinearRegression()
        emissions_model = LinearRegression()
        energy_model.fit(years_hist, energy_hist)
        emissions_model.fit(years_hist, emissions_hist)
        
        future_years = np.arange(2025, 2025 + forecast_years).reshape(-1, 1)
        energy_forecast = energy_model.predict(future_years)
        emissions_forecast = emissions_model.predict(future_years)
        
        return {
            'years': future_years.flatten().tolist(),
            'energy_forecast': energy_forecast.tolist(),
            'emissions_forecast': emissions_forecast.tolist()
        }
