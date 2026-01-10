# seed.py -> Fills test data to the database

import random
from datetime import datetime, timedelta

from db import SessionLocal
from models import Item, Booking

ITEMS = [
    ("Football", "Some ball"),
    ("Frankenstein", "Crazy book"),
    ("Cricket Bat", "For cricket"),
    ("Mouse", "Not a computer one"),
    ("Helicopter", "Useful for flying"),
]

def seed():
    db = SessionLocal()

    db.query(Booking).delete()
    db.query(Item).delete()
    db.commit()

    items = []
    for name, desc in ITEMS:
        item = Item(
            name=name,
            description=desc,
            image_path="stuff/stuff",
            hold_time=random.randint(2, 5),
            occupy_time=random.randint(7, 20),
        )
        db.add(item)
        items.append(item)

    db.commit() 

    db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully")
