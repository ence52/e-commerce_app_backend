from app.core.security import verify_password
from app.crud.user import get_user_by_email
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db:Session,email:str,password:str):
    user=get_user_by_email(db,email)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user