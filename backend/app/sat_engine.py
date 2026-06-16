import ee
from google.oauth2.service_account import Credentials
# Initialize the Earth Engine API
def initialize_gee():
    try:
        # JSON key file ka path
        SERVICE_ACCOUNT_FILE = 'gee_key.json' 
        
        # Service account se login karne ka logic
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/earthengine'])
        
        # Earth Engine chalu karo
        ee.Initialize(scoped_credentials)
        print("✅ GEE Authenticated successfully on Cloud!")
        
    except Exception as e:
        print(f"❌ GEE Init failed: {e}")
# Example function to get image for an area
def get_satellite_data(lat, lon, start_date, end_date):
    point = ee.Geometry.Point([lon, lat])
    collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .sort('CLOUD_COVER') \
        .first()
    return collection


def calculate_greenery(image):
    # NDVI Formula: (NIR - Red) / (NIR + Red)
    # Landsat 8 mein: Band 5 (NIR), Band 4 (Red)
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    
    # Greenery threshold: 0.3 se upar matlab vegetation
    greenery = ndvi.gt(0.3)
    
    # Poore area mein greenery ka mean (average) nikalna
    stats = greenery.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=image.geometry(),
        scale=30,
        maxPixels=1e9
    )
    
    # Percentage mein convert karo
    return stats.getInfo()['NDVI'] * 100