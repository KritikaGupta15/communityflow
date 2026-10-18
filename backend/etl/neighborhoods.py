import json
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood

def load_neighborhoods():
    db: Session = SessionLocal()

    print("Loading Chicago neighborhoods...")

    # Load GeoJSON file
    with open("data/chicago.geojson", "r") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        name = feature["properties"].get("name")
        geometry = feature["geometry"]

        neighborhood = Neighborhood(
            name=name,
            geometry=geometry
        )

        db.add(neighborhood)

    db.commit()
    db.close()

    print("Neighborhoods loaded successfully.")
