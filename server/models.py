from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = "episodes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship("Appearance", back_populates="episode", cascade='all, delete-orphan')

    def to_dict_basic(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }

    def to_dict(self):
        # You can expand this dictionary if you want more details
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number,
            "appearances": [appearance.to_dict_basic() for appearance in self.appearances]  # Assuming Appearance has a to_dict_basic method
        }


class Appearance(db.Model):
    __tablename__ = "appearances"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    def to_dict_basic(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "episode_id": self.episode_id,
            "guest_id": self.guest_id,
            "episode": self.episode.to_dict_basic(),
            "guest": self.guest.to_dict_basic()
        }
    
    @validates("rating")
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be 1 to 5 characters (inclusive)")
        return rating

class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship("Appearance", back_populates="guest", cascade='all, delete-orphan')

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }