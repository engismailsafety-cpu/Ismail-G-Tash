import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from image_analyzer import analyze_images
from text_classifier import classify_texts

def analyze_sustainability(files):
    all_data = {"co2": 0, "water": 0, "energy": 0, "waste": 0}
    
    for file in files:
        if file.name.endswith(("xlsx", "csv")):
            df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
            if "energy_kwh" in df.columns:
                all_data["energy"] = df["energy_kwh"].sum()
                all_data["co2"] += df["energy_kwh"].sum() * 0.4  # عامل انبعاث تقريبي
            if "water_m3" in df.columns:
                all_data["water"] = df["water_m3"].sum()
            if "waste_kg" in df.columns:
                all_data["waste"] = df["waste_kg"].sum()
        
        elif file.name.endswith(("jpg", "png")):
            img_results = analyze_images([file])
        
        elif file.name.endswith(("pdf", "docx")):
            text_results = classify_texts([file])
    
    # تنبؤ بالاستهلاك للسنوات القادمة
    years = np.arange(2020, 2025).reshape(-1, 1)
    energy_hist = [120, 135, 150, 170, 190]  # مثال
    model = LinearRegression()
    model.fit(years.flatten().reshape(-1,1), energy_hist)
    future_years = np.arange(2025, 2030).reshape(-1,1)
    predictions = model.predict(future_years)
    
    return {
        "co2": all_data["co2"],
        "water": all_data["water"],
        "energy": all_data["energy"],
        "waste": all_data["waste"],
        "predictions": pd.Series(predictions, index=[2025,2026,2027,2028,2029]),
        "image_results": img_results,
        "gri_mapping": text_results
    }