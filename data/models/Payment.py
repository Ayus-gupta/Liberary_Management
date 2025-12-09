
from datetime import datetime
from data.models import db

class Payment(db.Model):
    __tablename__ = "Payments"

    id = db.Column(db.Integer, primary_key=True)
    Student_id = db.Column(db.Integer, db.ForeignKey("Students.id"), nullable=False)
    month = db.Column(db.Date, nullable=False)  # store as first day of month
    status = db.Column(db.String(10), default="Unpaid")  # Paid / Unpaid
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    Student = db.relationship("Student", back_populates="Payments")
