import matplotlib.pyplot as plt
from flask import render_template, request, redirect, url_for, Response

from data.models import Payment, Student, db
# from models.__init__ import db
from flask import sessions
from app import app
from datetime import date, datetime

from sqlalchemy import extract, func

@app.route("/")
def index():
    students = Student.query.all()

    # --- Revenue per month (only Paid payments) ---
    revenue_data = (
        db.session.query(
            extract("year", Payment.month).label("year"),
            extract("month", Payment.month).label("month"),
            func.sum(Payment.amount).label("total")
        )
        .filter(Payment.status == "Paid")
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    # Convert query result into labels + values for Chart.js
    labels = [f"{int(r.year)}-{int(r.month):02d}" for r in revenue_data]
    values = [float(r.total) for r in revenue_data]

    return render_template("index.html", students=students, labels=labels, values=values)



# --- Add Student ---
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]
        seat_number = request.form["seat_number"]

        student = Student(
            name=name,
            phone_number=phone_number,
            seat_number=seat_number
        )
        db.session.add(student)
        db.session.commit()

        # Optionally: create a default "Unpaid" Payment record for current month
        payment = Payment(
            Student_id=student.id,
            month=datetime(datetime.today().year, datetime.today().month, 1),
            status="Unpaid",
            amount=0.00
        )
        db.session.add(payment)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_student.html")


# --- Edit Student ---
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.phone_number = request.form["phone_number"]
        
        student.removal_reason = request.form.get("removal_reason", None)

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_student.html", student=student)


# --- Delete Student ---
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)  # This will also delete Payments because of cascade
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


# --- Add / Edit Payment for a Student ---
@app.route("/payment/<int:student_id>", methods=["GET", "POST"])
def manage_payment(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        month = datetime.strptime(request.form["month"], "%Y-%m-%d").date()
        status = request.form["status"]
        amount = request.form["amount"]

        # Check if payment for this month already exists
        payment = Payment.query.filter_by(Student_id=student.id, month=month).first()
        if payment:
            payment.status = status
            payment.amount = amount
        else:
            payment = Payment(
                Student_id=student.id,
                month=month,
                status=status,
                amount=amount
            )
            db.session.add(payment)

        db.session.commit()
        return redirect(url_for("index"))

    payments = Payment.query.filter_by(Student_id=student.id).all()
    return render_template("payment.html", student=student, payments=payments)