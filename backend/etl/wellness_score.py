# etl/wellness_score.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood

def compute_wellness_scores():
    db: Session = SessionLocal()

    print("Computing wellness scores...")

    neighborhoods = db.query(Neighborhood).all()

    for n in neighborhoods:
        # Avoid None values
        parks = n.parks_count or 0
        libraries = n.libraries_count or 0
        centers = n.community_centers_count or 0
        studios = n.yoga_studios_count or 0
        transit = n.transit_score or 0
        population = n.population_density or 0

        # Weighted scoring formula (simple version)
        score = (
            parks * 0.20 +
            libraries * 0.15 +
            centers * 0.15 +
            transit * 0.25 +
            population * 0.10 -
            studios * 0.15
        )

        n.wellness_score = round(score, 2)
        db.add(n)

    db.commit()
    db.close()

    print("Wellness scores computed successfully.")
