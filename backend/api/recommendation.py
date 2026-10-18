# api/recommendations.py
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood

router = APIRouter()

def extract_centroid(geometry_data):
    """Calculates center latitude and longitude from GeoJSON geometry."""
    if not geometry_data:
        return 41.8781, -87.6298  # Default Chicago center fallback
    
    try:
        geom_type = geometry_data.get("type")
        coords = geometry_data.get("coordinates")
        
        if geom_type == "Polygon":
            # coords[0] contains the outer boundary ring: [[lng, lat], [lng, lat], ...]
            ring = coords[0]
            lats = [pt[1] for pt in ring]
            lngs = [pt[0] for pt in ring]
            return sum(lats) / len(lats), sum(lngs) / len(lngs)
            
        elif geom_type == "MultiPolygon":
            # coords[0][0] is the first polygon's outer ring
            ring = coords[0][0]
            lats = [pt[1] for pt in ring]
            lngs = [pt[0] for pt in ring]
            return sum(lats) / len(lats), sum(lngs) / len(lngs)
    except Exception:
        pass
    
    return 41.8781, -87.6298

@router.get("/recommendations")
def get_recommendations(
    min_transit_score: float = Query(0.0, description="Minimum transit score required"),
    min_parks: int = Query(0, description="Minimum number of parks required"),
    min_libraries: int = Query(0, description="Minimum number of libraries required"),
    keyword: str = Query(None, description="Optional preference keyword")
):
    db: Session = SessionLocal()
    
    query = db.query(Neighborhood).filter(
        Neighborhood.transit_score >= min_transit_score,
        Neighborhood.parks_count >= min_parks,
        Neighborhood.libraries_count >= min_libraries
    )
    
    neighborhoods = query.all()
    db.close()

    results = []
    for n in neighborhoods:
        lat, lng = extract_centroid(n.geometry)
        results.append({
            "id": n.id,
            "name": n.name,
            "wellness_score": n.wellness_score,
            "transit_score": n.transit_score,
            "parks_count": n.parks_count,
            "libraries_count": n.libraries_count,
            "latitude": lat,
            "longitude": lng
        })

    return {
        "filters_applied": {
            "min_transit_score": min_transit_score,
            "min_parks": min_parks,
            "min_libraries": min_libraries,
            "keyword": keyword
        },
        "total_matches": len(results),
        "recommendations": results
    }