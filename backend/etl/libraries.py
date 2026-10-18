# etl/libraries.py

import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Library

API_URL = "https://data.cityofchicago.org/resource/x8fc-8rcq.json" # Chicago Public Library locations

def load_libraries():
    print("Loading Chicago libraries...")

    response = requests.get(API_URL)
    data = response.json()

    db: Session = SessionLocal()

    # Clear existing libraries to avoid duplicates
    db.query(Library).delete()
    db.commit()

    for row in data:
        try:
            latitude = None
            longitude = None

            # 1. Check direct row fields
            if row.get("latitude") and row.get("longitude"):
                try:
                    latitude = float(row["latitude"])
                    longitude = float(row["longitude"])
                except (ValueError, TypeError):
                    pass

            # 2. Fallback: check 'location' field (dict or GeoJSON)
            loc = row.get("location")
            if (latitude is None or longitude is None) and loc:
                if isinstance(loc, dict):
                    if "latitude" in loc and "longitude" in loc:
                        latitude = float(loc["latitude"])
                        longitude = float(loc["longitude"])
                    elif "coordinates" in loc:
                        coords = loc["coordinates"]
                        if len(coords) >= 2:
                            longitude = float(coords[0])
                            latitude = float(coords[1])

            library = Library(
                name=row.get("name_"),
                address=row.get("address"),
                latitude=latitude,
                longitude=longitude,
                zip_code=row.get("zip")
            )

            db.add(library)

        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    db.commit()
    db.close()

    print("Libraries loaded successfully with coordinates.")

if __name__ == "__main__":
    load_libraries()