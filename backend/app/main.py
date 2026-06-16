""" # 1. Sabse upar Imports
from fastapi import FastAPI
from sat_engine import initialize_gee, get_satellite_data, calculate_greenery
from ai_logic import get_environmental_insight
from db_helper import Neo4jHandler # <--- Ye add kar

# 2. App aur DB Setup (Ye top pe hona chahiye)
app = FastAPI()
db = Neo4jHandler("neo4j+s://d78410b2.databases.neo4j.io:7687", "neo4j", "xsOm73GcFzzaJ4m4UBv8eOwoSu6eMcqT4oN3B6Su054")

# 3. GEE Init
initialize_gee()

# 4. Endpoints
@app.get("/analyze")
def analyze_area(lat: float, lon: float, area_name: str = "Unknown"):
    img = get_satellite_data(lat, lon, "2023-01-01", "2023-12-31")
    greenery_pct = calculate_greenery(img)
    insight = get_environmental_insight(greenery_pct, area_name)
    
    # Save to Neo4j
    # db.save_analysis(area_name, float(greenery_pct), insight)
    
    return {"greenery_percentage": round(greenery_pct, 2), "ai_analysis": insight} """





from datetime import datetime # Ye top pe add kar lena
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sat_engine import initialize_gee, get_satellite_data, calculate_greenery
from ai_logic import get_environmental_insight
from db_helper import Neo4jHandler

# App aur DB Setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon ke liye "*" (allow all) best hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Credentials ko .env se manage karna best practice hai
db = Neo4jHandler("neo4j+s://d78410b2.databases.neo4j.io:7687", "neo4j", "xsOm73GcFzzaJ4m4UBv8eOwoSu6eMcqT4oN3B6Su054")

# GEE Init
initialize_gee()


@app.get("/analyze")
def analyze_area(lat: float, lon: float, past_year: int , area_name: str):
    try:
        # Dynamic Year Detection
        present_year = datetime.now().year 
        
        # 1. Past Data
        img_past = get_satellite_data(lat, lon, f"{past_year}-01-01", f"{past_year}-12-31")
        greenery_past= calculate_greenery(img_past, lat, lon)
        
        # 2. Present Data (Current Year)
        img_present = get_satellite_data(lat, lon, f"{present_year}-01-01", f"{present_year}-12-31")
        greenery_present= calculate_greenery(img_present, lat, lon)

        
        # 3. AI Comparison
        comparison_text = f"Greenery in {past_year} was {greenery_past}%, and in {present_year} it is {greenery_present}%."
        insight = get_environmental_insight(comparison_text, area_name)
        
        # 4. Database Sync (Graph Model)
        try:
            db.save_analysis(area_name, float(greenery_present), insight)
        except Exception as db_err:
            print(f"Database sync failed: {db_err}")
            
        # 5. Final JSON Response
        return {
            "area": area_name,
            "past_year": past_year,
            "present_year": present_year,
            "past_greenery": round(greenery_past, 2),
            "present_greenery": round(greenery_present, 2),
            "ai_analysis": insight
        }
    
    except Exception as e:
        return {"error": f"Failed to process analysis: {str(e)}"}