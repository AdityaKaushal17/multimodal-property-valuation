import os
import math
import requests
import pandas as pd
from tqdm import tqdm
from PIL import Image
from io import BytesIO

def deg2num(lat_deg, lon_deg, zoom):
    """Converts lat/long to tile x,y coordinates"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_satellite_image(lat, lon, zoom, output_path):
    """
    Downloads a tile from Esri World Imagery (No API key required).
    Zoom 19 is roughly 0.3m per pixel resolution.
    """
    xtile, ytile = deg2num(lat, lon, zoom)
    
    # Using Esri World Imagery (Legal for educational use)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ytile}/{xtile}"
    
    headers = {
        'User-Agent': 'PropertyValuationProject/1.0 (Contact: your-email@example.com)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(output_path)
            return True
    except Exception as e:
        print(f"Error downloading {lat}, {lon}: {e}")
    return False

def main():
    # 1. Load your base data
    input_file = "test2(test(1)).csv"
    df = pd.read_csv(input_file)
    
    # 2. Setup storage
    output_dir = "property_images_test1"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Starting download for {len(df)} properties...")

    # 3. Iterate and Fetch
    # Note: We use the index or a unique ID to name the files
    success_count = 0
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        # Ensure your column names match: 'lat' and 'long'
        lat = row['lat']
        lon = row['long']
        property_id = index # Or row['id'] if available
        
        file_path = os.path.join(output_dir, f"prop_{property_id}.jpg")
        
        # Avoid re-downloading if file exists
        if not os.path.exists(file_path):
            success = download_satellite_image(lat, lon, 19, file_path)
            if success:
                success_count += 1
        else:
            success_count += 1

    print(f"Finished! Total images available: {success_count}")

if __name__ == "__main__":
    main()