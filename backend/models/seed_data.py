from schemas import db
from datetime import datetime

def seed_data():
    # clear existing data
    db.clients.delete_many({})
    db.orders.delete_many({})
    db.payments.delete_many({})
    db.courses.delete_many({})
    db.classes.delete_many({})
    db.attendance.delete_many({})

    # insert courses
    yoga_course_id = db.courses.insert_one({
        "title": "Yoga Beginner",
        "description": "Intro to Yoga fundamentals",
        "instructor": "Alice",
        "status": "active",
        "start_date": datetime(2025,7,5),
        "end_date": datetime(2025,7,31)
    }).inserted_id

    pilates_course_id = db.courses.insert_one({
        "title": "Pilates Intermediate",
        "description": "Core strengthening",
        "instructor": "Bob",
        "status": "active",
        "start_date": datetime(2025,7,6),
        "end_date": datetime(2025,7,30)
    }).inserted_id

    # insert classes
    class1_id = db.classes.insert_one({
        "course_id": yoga_course_id,
        "date": datetime(2025,7,6),
        "instructor": "Alice",
        "status": "scheduled",
        "capacity": 20
    }).inserted_id

    class2_id = db.classes.insert_one({
        "course_id": pilates_course_id,
        "date": datetime(2025,7,8),
        "instructor": "Bob",
        "status": "scheduled",
        "capacity": 15
    }).inserted_id

    # insert client
    client_id = db.clients.insert_one({
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "9876543210",
        "enrolled_services": [
            {"course_id": yoga_course_id, "status": "active"}
        ],
        "created_at": datetime.now()
    }).inserted_id

    # insert order
    order_id = db.orders.insert_one({
        "client_id": client_id,
        "service_name": "Yoga Beginner",
        "amount": 1500,
        "status": "paid",
        "created_at": datetime.now()
    }).inserted_id

    # insert payment
    db.payments.insert_one({
        "order_id": order_id,
        "amount": 1500,
        "payment_date": datetime.now(),
        "method": "credit_card"
    })

    # insert attendance
    db.attendance.insert_one({
        "class_id": class1_id,
        "client_id": client_id,
        "attended": True
    })

    print("✅ Sample data seeded successfully!")

if __name__ == "__main__":
    seed_data()
