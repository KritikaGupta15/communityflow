from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import Neighborhood

from api.recommendation import router as recommendations_router
from api.neighborhood_summary import router as summary_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from api.neighborhood_summary import router as summary_router
app.include_router(summary_router)


@app.get("/neighborhoods")
def get_neighborhoods():

    db = SessionLocal()

    neighborhoods = db.query(Neighborhood).all()

    results = []

    for n in neighborhoods:
        results.append({
            "id": n.id,
            "name": n.name,
            "wellness_score": n.wellness_score,
            "transit_score": n.transit_score,
            "parks_count": n.parks_count,
            "libraries_count": n.libraries_count
        })

    db.close()

    return results


app.include_router(recommendations_router)