 # models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    carbon_entries = relationship("CarbonEntry", back_populates="user")

class CarbonEntry(Base):
    __tablename__ = "carbon_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    co2_emission = Column(Float, nullable=False)
    user = relationship("User", back_populates="carbon_entries")