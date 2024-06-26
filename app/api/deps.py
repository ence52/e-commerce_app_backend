from app.core.security import check_password
from app.db.models.user import UserModel
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db:Session,email:str,password:str):
    user=db.query(UserModel).filter(UserModel.email==email).first()
    if not user:
        return False
    if not check_password(password,user.hashed_password):
        return False
    return user