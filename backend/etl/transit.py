import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import TrainStation, BusStop

TRAIN_API = "https://data.cityofchicago.org/resource/8mj8-j3c4.json"
BUS_API = "https://data.cityofchicago.org/api/v3/views/qs84-j7wh/query.json"


def load_train_stations():
    print("Loading CTA train stations...")

    response = requests.get(TRAIN_API)
    data = response.json()

    db: Session = SessionLocal()

    for row in data:
        try:
            loc = row.get("location")
            latitude = None
            longitude = None

            if loc and "coordinates" in loc:
                coords = loc["coordinates"]
                longitude = float(coords[0])
                latitude = float(coords[1])

            station = TrainStation(
                stop_id=row.get("stop_id"),
                stop_name=row.get("stop_name"),
                station_name=row.get("station_name"),
                latitude=latitude,
                longitude=longitude,
                red=row.get("red"),
                blue=row.get("blue"),
                g=row.get("g"),
                brn=row.get("brn"),
                p=row.get("p"),
                y=row.get("y"),
                pnk=row.get("pnk"),
                o=row.get("o")
            )

            db.add(station)

        except Exception as e:
            print("Skipping train row:", e)

    db.commit()
    db.close()
    print("Train stations loaded successfully.")


def load_bus_stops():
    print("Loading CTA bus stops...")
    print("BUS API URL:", BUS_API)

    response = requests.get(BUS_API)
    data = response.json()

    print("DEBUG BUS ROW:", data[:1])

    db: Session = SessionLocal()

    for row in data:
        try:
            geom = row.get("the_geom")
            latitude = None
            longitude = None

            if geom and "coordinates" in geom:
                coords = geom["coordinates"]
                longitude = float(coords[0])
                latitude = float(coords[1])

            stop_name = row.get("public_nam")
            routes = row.get("routesstpg")

            stop = BusStop(
                stop_name=stop_name,
                latitude=latitude,
                longitude=longitude,
                routes=routes
            )

            db.add(stop)

        except Exception as e:
            print("Skipping bus row:", e)

    db.commit()
    db.close()
    print("Bus stops loaded successfully.")
