from typing import Annotated
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.core.security import  ALGORITHM, SECRET_KEY
from app.db.models.cart import CartModel
from app.db.models.user import UserModel
from app.db.session import SessionLocal
from app.schemas.token_data import  TokenData
from app.schemas.user import  UserCreateSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session,user_id):
    return db.query(UserModel).filter(UserModel.id==user_id).first()
    
def get_user_by_email(db: Session,email):
    return db.query(UserModel).filter(UserModel.email==email).first()


def get_cart_info_by_user_id(db: Session,user_id):
    return db.query(CartModel).filter(CartModel.user_id==user_id).first()

def get_user_cart_id(db: Session, user_id: int) -> int:
    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if cart:
        return cart.id
    return None

def create_user(db:Session,user:UserCreateSchema):
    db_user = get_user_by_email(db=db,email=user.email)
    if db_user :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This e-mail is already in use!")

    db_user = UserModel(name=user.name,email=user.email)
    
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_cart= CartModel(user_id=db_user.id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_user

def delete_user(db:Session,user_id:int):
    user= get_user(db=db,user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {user_id} is not found!")
    db.delete(user)
    db.commit()
    return {"detail":f"User with id {user_id} has been deleted"}

async def get_current_user(token: str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user=get_user_by_email(db=db,email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user:UserModel=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive User")
    return current_user

