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


def save_data_base(data: List[Item]) -> None:
    """
    Saves updated data into the database (pickle file for now).
    """
    try:
        with open(DATA_FILE, "wb") as file:
            pickle.dump(data, file)
    except Exception as e:
        print(f'[ERROR] Could not save database: {e}')


def load_data_base() -> List[Item]:
    """
    Loads data from the pickle database.
    """
    try:
        with open(DATA_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("[INFO] Stored data not found, returning empty list")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to load database: {e}")
        return []


def fill_test_data() -> None:
    """
    Fills random test data (overwrites existing database).
    """
    test_data = [
        Item(1, "Football", "Some ball", "stuff/stuff"),
        Item(2, "Frankenstein", "Crazy book", "stuff/stuff"),
        Item(3, "Cricket Bat", "For cricket", "stuff/stuff"),
        Item(4, "Mouse", "Not a computer one, a real one", "stuff/stuff"),
        Item(5, "Helicopter", "Useful for flying", "stuff/stuff"),
    ]

    with open(DATA_FILE, "wb") as file:
        pickle.dump(test_data, file)

    print("[INFO] Test data written successfully")
