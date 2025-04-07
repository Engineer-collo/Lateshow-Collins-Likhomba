import random
from faker import Faker
from app import db,app
from models import Appearance,Episode,Guest

# Initialize Faker
fake = Faker()

def seed_episodes(num_entries=200):  # Update to 200 entries
    for _ in range(num_entries):
        # Create an Episode
        episode = Episode(
            date=fake.date_this_decade(),
            number=random.randint(1, 100)
        )
        db.session.add(episode)
        db.session.commit()

def seed_guests(num_entries=200):  # Update to 200 entries
    for _ in range(num_entries):
        # Create a Guest
        guest = Guest(
            name=fake.name(),
            occupation=fake.job()
        )
        db.session.add(guest)
        db.session.commit()

def seed_appearances(num_entries=200):  # Update to 200 entries
    # First, fetch all episodes and guests
    episodes = Episode.query.all()
    guests = Guest.query.all()
    
    for _ in range(num_entries):
        # Randomly select an episode and a guest
        episode = random.choice(episodes)
        guest = random.choice(guests)
        
        # Create an Appearance with a random rating between 1 and 5
        appearance = Appearance(
            rating=random.randint(1, 5),
            episode_id=episode.id,
            guest_id=guest.id
        )
        db.session.add(appearance)
    
    db.session.commit()

def seed_database():
    seed_episodes(200)  # Seed 200 Episodes
    seed_guests(200)    # Seed 200 Guests
    seed_appearances(200)  # Seed 200 Appearances

if __name__ == "__main__":
    # Make sure the database is initialized
    with app.app_context():  # Replace 'app' with your actual Flask app instance
        db.create_all()  # Create all tables
        seed_database()  # Seed data
        print("Database seeded with 200 entries!")
