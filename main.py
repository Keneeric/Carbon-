# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User, CarbonEntry
from schemas import UserCreate, UserResponse, CarbonEntryCreate, CarbonEntryResponse
from auth import hash_password, authenticate_user, create_access_token

app = FastAPI(title="Carbon Footprint API")

Base.metadata.create_all(bind=engine)

EMISSION_FACTOR = 0.4  # kg CO2 per mile (example)

# User Authentication Routes
@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(user.email, user.password, db)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Carbon Footprint CRUD Endpoints
@app.post("/track", response_model=CarbonEntryResponse)
def create_carbon_entry(entry: CarbonEntryCreate, db: Session = Depends(get_db)):
    user_id = 1  # Hardcoded for now; replace with auth later
    co2_emission = entry.value * EMISSION_FACTOR if entry.category == "transportation" else 0.0
    new_entry = CarbonEntry(
        user_id=user_id,
        category=entry.category,
        value=entry.value,
        co2_emission=co2_emission
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@app.get("/entries/{user_id}", response_model=list[CarbonEntryResponse])
def read_carbon_entries(user_id: int, db: Session = Depends(get_db)):
    entries = db.query(CarbonEntry).filter(CarbonEntry.user_id == user_id).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found for this user")
    return entries

@app.put("/entries/{entry_id}", response_model=CarbonEntryResponse)
def update_carbon_entry(entry_id: int, entry: CarbonEntryCreate, db: Session = Depends(get_db)):
    db_entry = db.query(CarbonEntry).filter(CarbonEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db_entry.category = entry.category
    db_entry.value = entry.value
    db_entry.co2_emission = entry.value * EMISSION_FACTOR if entry.category == "transportation" else 0.0
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.delete("/entries/{entry_id}")
def delete_carbon_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(CarbonEntry).filter(CarbonEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(db_entry)
    db.commit()
    return {"message": "Entry deleted"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Carbon Footprint API"}