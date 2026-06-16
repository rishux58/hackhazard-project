import ee
from google.oauth2.service_account import Credentials
import os

# Initialize the Earth Engine API
def initialize_gee():
    try:
        # File dhoondhne ka smart tareeka (Local aur Cloud dono ke liye)
        possible_paths = [
            'gee_key.json',                     # Tere PC ke liye
            'app/gee_key.json',                 # PC ka dusra path
            '/etc/secrets/gee_key.json',        # Render ka hidden path
            '/etc/secrets/app/gee_key.json'     # Render ka subfolder path
        ]
        
        SERVICE_ACCOUNT_FILE = None
        for path in possible_paths:
            if os.path.exists(path):
                SERVICE_ACCOUNT_FILE = path
                break
        
        if not SERVICE_ACCOUNT_FILE:
            raise FileNotFoundError("Google Cloud JSON key Render par nahi mili!")

        # Login karne ka logic
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/earthengine'])
        
        # Earth Engine chalu karo
        ee.Initialize(credentials=scoped_credentials)
        print("✅ GEE Authenticated successfully on Cloud!")
        
    except Exception as e:
        print(f"❌ GEE Init failed: {e}")

# Example function to get image for an area
def get_satellite_data(lat, lon, start_date, end_date):
    point = ee.Geometry.Point([float(lon), float(lat)])
    collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .sort('CLOUD_COVER')
    
    # Agar data nahi mila us saal ka, toh crash na ho
    if collection.size().getInfo() == 0:
        return None
        
    return collection.first()

# YAHAN CHANGE HAI: lat aur lon parameters add kiye hain geometry ke liye
def calculate_greenery(image, lat, lon):
    if image is None:
        return 0.0 # Agar us saal ki image nahi mili toh 0%

    # 5km radius ka buffer banaya (Error hamesha ke liye khatam)
    point = ee.Geometry.Point([float(lon), float(lat)])
    region = point.buffer(5000)

    # NDVI Formula: (NIR - Red) / (NIR + Red)
    # Landsat 8 mein: Band 5 (NIR), Band 4 (Red)
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    
    # Greenery threshold: 0.3 se upar matlab vegetation
    greenery = ndvi.gt(0.3)
    
    # Poore area mein greenery ka mean (average) nikalna
    stats = greenery.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region, # image.geometry() HATA DIYA HAI
        scale=30,
        maxPixels=1e9
    )
    
    # Value nikalna aur crash se bachna
    val = stats.getInfo().get('NDVI')
    if val is None:
        return 0.0
        
    # Percentage mein convert karo
    return round(val * 100, 2)