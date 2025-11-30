from app.database import SessionLocal, engine
from app.models import tables

def create_test_user():
    db = SessionLocal()
    # Check if user exists
    user = db.query(tables.User).filter(tables.User.email == "test@example.com").first()
    if not user:
        print("Creating test user...")
        new_user = tables.User(email="test@example.com")
        db.add(new_user)
        db.commit()
        print("User created with ID: 1")
    else:
        print("Test user already exists.")
    db.close()

if __name__ == "__main__":
    create_test_user()