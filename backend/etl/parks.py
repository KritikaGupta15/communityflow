# etl/parks.py

import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Park

API_URL = "https://data.cityofchicago.org/resource/4xwe-2j3y.json"

def load_parks():
    print("Loading Chicago parks...")

    response = requests.get(API_URL)
    data = response.json()

    db: Session = SessionLocal()

    # Clear existing parks to avoid duplicates with missing coords
    db.query(Park).delete()
    db.commit()

    for row in data:
        try:
            latitude = None
            longitude = None

            # 1. Check if latitude/longitude exist directly in the row
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
                    elif "coordinates" in loc: # GeoJSON format [longitude, latitude]
                        coords = loc["coordinates"]
                        if len(coords) >= 2:
                            longitude = float(coords[0])
                            latitude = float(coords[1])

            park = Park(
                name=row.get("park_name"),
                facility_type=row.get("park_type"),
                location=row.get("address"),
                latitude=latitude,
                longitude=longitude,
                acres=None,
                ward=None,
                zip_code=row.get("zip"),
                park_class=None,
                features=None
            )

            db.add(park)

        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    db.commit()
    db.close()

    print("Parks loaded successfully with coordinates.")

if __name__ == "__main__":
    load_parks()