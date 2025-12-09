
from data.models import db
import enum
from datetime import datetime
from sqlalchemy import Enum
# Enum for student shift

class Student(db.Model):
    __tablename__ = "Students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    Payments = db.relationship("Payment", back_populates="Student", cascade="all, delete-orphan")
