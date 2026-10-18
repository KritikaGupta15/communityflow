# etl/indicator_join.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood, Park, Library, BusStop, TrainStation
from shapely.geometry import shape, Point

def get_lat_lon(obj):
    lat = getattr(obj, 'latitude', None)
    lon = getattr(obj, 'longitude', None)
    return lat, lon

def join_indicators():
    db: Session = SessionLocal()

    print("Joining indicators into neighborhoods...")

    neighborhoods = db.query(Neighborhood).all()
    parks = db.query(Park).all()
    libraries = db.query(Library).all()
    bus_stops = db.query(BusStop).all()
    train_stations = db.query(TrainStation).all()

    print(f"Loaded {len(neighborhoods)} neighborhoods, {len(parks)} parks, {len(libraries)} libraries, {len(bus_stops)} bus stops, {len(train_stations)} train stations.")

    for n in neighborhoods:
        try:
            raw_poly = shape(n.geometry)
            polygon = raw_poly.buffer(0) if not raw_poly.is_valid else raw_poly

            # Count parks
            n.parks_count = sum(
                polygon.contains(Point(lon, lat))
                for p in parks
                for lat, lon in [get_lat_lon(p)]
                if lat is not None and lon is not None
            )

            # Count libraries
            n.libraries_count = sum(
                polygon.contains(Point(lon, lat))
                for l in libraries
                for lat, lon in [get_lat_lon(l)]
                if lat is not None and lon is not None
            )

            # Count transit (bus + train)
            bus_count = sum(
                polygon.contains(Point(lon, lat))
                for b in bus_stops
                for lat, lon in [get_lat_lon(b)]
                if lat is not None and lon is not None
            )

            train_count = sum(
                polygon.contains(Point(lon, lat))
                for t in train_stations
                for lat, lon in [get_lat_lon(t)]
                if lat is not None and lon is not None
            )

            n.transit_score = bus_count + train_count
            db.add(n)
        except Exception as e:
            print(f"Error processing neighborhood {n.name}: {e}")

    db.commit()
    db.close()
    print("Indicators joined successfully with real coordinates!")

if __name__ == "__main__":
    join_indicators()