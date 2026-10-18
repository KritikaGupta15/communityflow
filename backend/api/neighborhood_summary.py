from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood
from llm import generate_summary

router = APIRouter()

@router.get("/neighborhoods/{neighborhood_id}/summary")
def neighborhood_summary(neighborhood_id: int):
    db: Session = SessionLocal()
    n = db.query(Neighborhood).filter(Neighborhood.id == neighborhood_id).first()

    if not n:
        raise HTTPException(status_code=404, detail="Neighborhood not found")

    summary = generate_summary({
        "name": n.name,
        "parks": n.parks_count,
        "libraries": n.libraries_count,
        "centers": n.community_centers_count,
        "transit": n.transit_score,
        "population": n.population_density,
        "wellness": n.wellness_score
    })

    return {"neighborhood": n.name, "summary": summary}
