# seed.py -> Fills test data to the database

import random
from datetime import datetime, timedelta

from db import SessionLocal
from models import Item, Booking

ITEMS = [
    "Siddhartha",
    "The Power Of Your Subconsious Mind",
    "My Brilliant Friend",
    "Zero to One",
    "The Art of War",
    "How to Win And Influence People",
    "The Greate Gatsby",
    "The Plague",
    "One Thousand Years of Solitude",
    "Frankenstien",
    "The Autobiography of A Yogi",
    "Metamorphosis",
    "The Diary of a Young Girl",
    "Pride and Prejudice",
    "The 3 Mistakes of My Life",
    "A Short History of Nepal",
    "The Bill Jar",
    "Russian History - A short Introduction",
    "The Napolean Wars",
    "Fascim",
    "करोडौँ कस्तुरी",
    "सुम्निमा",
    "सेरो धरती",
    "प्रिय सुकी",
    "कर्नाली ब्लुज",
    "जीवन काँडा कि फुल",
    "शिरीषको फूल",
    "गुलाबी उमेर",
    "सेतो बाघ",
    "एक्लो",
    "समर लभ",
    "एक सर्को माया",
    "दमिनी भीर",
    "पागल बस्ती"
]

def seed():
    db = SessionLocal()

    db.query(Booking).delete()
    db.query(Item).delete()
    db.commit()

    items = []
    for name in ITEMS:
        item = Item(
            name=name,
            description="",
            image_path="",
            hold_time=2,
            occupy_time=15,
            available=False
        )
        booking = Booking(
                user_email = 'legacy',
                booked_date = datetime.now(),
                item = item
            )
        db.add(item)
        db.add(booking)
        items.append(item)

    db.commit() 

    db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully")
