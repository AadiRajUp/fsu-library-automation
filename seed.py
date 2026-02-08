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
    "पागल बस्ती",
    'The Alchemist',
    'फिरफिरे',
    'इजोरिया',
    'वसन्ती',
    'Mein Kampf',
    'पहेँलपुर',
    'यो जिन्दगी खै के जिन्दगी',
    'Pshychology of Money',
    'Animal Farm',
    'सत्प्रयास',
    'Babel',
    'अन्तर्मनको यात्रा',
    'पानीकाे घाम',
    'Mother Mary Comes to Me',
    'Six of Crows',
    'Rich Dad Poor Dad',
    'फिरफिरे',
    'माधवी',
    'The perks of being a wallflower',
    '1984',
    'The Wealth of Nations',
    'चीरहरण',
    'साया',
    'The Kite Runner',
    'Battles of the New Republic',
    'Life of Pi',
    'Sapiens - A Brief History of Humankind',
    'Das Capital',
    'Steve Jobs by Walter Issacson',
    'खलंगामा',
    'To Kill a Mockingbird',
    'नीलाे प्रेम',
    'शून्य मूल्य',
    'आत्मवृत्तान्त',
    'राधा',
    'धनको धब्बा',
    'सिमसारा',
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
            available=False,
            catagory = 1,
        )
        booking = Booking(
                user_email = 'legacy',
                booked_date = datetime.now(),
                item = item,
            )
        db.add(item)
        db.add(booking)
        items.append(item)

    db.commit() 

    db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully")
