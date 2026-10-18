from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

# -----------------------------
# Neighborhood Table
# -----------------------------
class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    geometry = Column(JSON)

    parks_count = Column(Integer, default=0)
    libraries_count = Column(Integer, default=0)
    community_centers_count = Column(Integer, default=0)
    yoga_studios_count = Column(Integer, default=0)

    population_density = Column(Float, nullable=True)
    transit_score = Column(Float, nullable=True)
    wellness_score = Column(Float, nullable=True)

    # FIX: Add these two relationships
    indicators = relationship("Indicator", back_populates="neighborhood")
    scores = relationship("OpportunityScore", back_populates="neighborhood")



# -----------------------------
# Indicator Table
# -----------------------------
class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"))
    type = Column(String, nullable=False)  # parks, libraries, transit, yoga_studios, etc.
    value = Column(Float, nullable=True)   # numeric score or count

    neighborhood = relationship("Neighborhood", back_populates="indicators")


# -----------------------------
# Opportunity Score Table
# -----------------------------
class OpportunityScore(Base):
    __tablename__ = "opportunity_scores"

    id = Column(Integer, primary_key=True, index=True)
    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"))
    score = Column(Float, nullable=False)
    details = Column(JSON, nullable=True)  # breakdown of scoring factors

    neighborhood = relationship("Neighborhood", back_populates="scores")


# -----------------------------
# Create all tables
# -----------------------------




class Park(Base):
    __tablename__ = "parks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    facility_type = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    acres = Column(Float)
    ward = Column(Integer)
    zip_code = Column(String)
    park_class = Column(String)
    features = Column(String)  # JSON string of features


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    zip_code = Column(String)
    phone = Column(String)
    website = Column(String)




class TrainStation(Base):
    __tablename__ = "train_stations"

    id = Column(Integer, primary_key=True, index=True)
    stop_id = Column(String)          # CTA stop_id
    stop_name = Column(String)
    station_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    red = Column(String)
    blue = Column(String)
    g = Column(String)
    brn = Column(String)
    p = Column(String)
    y = Column(String)
    pnk = Column(String)
    o = Column(String)

class BusStop(Base):
    __tablename__ = "bus_stops"

    id = Column(Integer, primary_key=True, index=True)
    stop_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    routes = Column(String)




