#-------------------------------------------------------------------------------------------
# models.py -> contains database models and relevants (pickle for now, TODO: use a database)
#-------------------------------------------------------------------------------------------

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base
from db import SessionLocal

# ---------------- CONSTANTS ----------------
DATA_BASE_URL = "sqlite:://app.db"
# -------------------------------------------

# ---------------- Database Models ----------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image_path = Column(String, nullable=True)

    available = Column(Boolean, default=True)

    hold_time = Column(Integer, default=3)  # Max-days before return must be done
    occupy_time = Column(Integer, default=15) # Max-days after booking item must be taken

    bookings = relationship("Booking", back_populates="item")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    user_email = Column(String, nullable=False)

    booked_date = Column(DateTime, default=datetime.now())
    occupied_date = Column(DateTime, nullable=True)

    on_hold_state = Column(Boolean, default=True)
    on_occupied_state = Column(Boolean, default=False)
    is_expired = Column(Boolean, default=False)

    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="bookings")


# ---------------- DATABASE FUNCTIONS ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def item_by_id(db, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_all_items(db):
    return db.query(Item).all()

def get_available_items(db):
    return db.query(Item).filter(Item.available == True).all()

def get_expired_bookings(db):
    return db.query(Booking).filter(Booking.is_expired == True).all()

def get_items_on_hold(db):
    return db.query(Item).join(Booking).filter(
        Booking.on_hold_state == True,
        Booking.is_expired == False
    ).all()

def get_user_bookings(db, email: str):
    return db.query(Booking).filter(
        Booking.user_email == email
    ).all()


def get_items_on_occupy(db):
    return db.query(Item).join(Booking).filter(
        Booking.on_occupied_state == True,
        Booking.is_expired == False
    ).all()