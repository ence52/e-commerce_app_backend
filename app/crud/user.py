from fastapi import HTTPException,status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.db.models.user import UserModel
from app.schemas.user import  UserCreateSchema

def get_user(db: Session,user_id):
    return db.query(UserModel).filter(UserModel.id==user_id).first()

def create_user(db:Session,user:UserCreateSchema):
    db_user = get_user_by_email(db=db,email=user.email)
    if db_user :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This e-mail is already in use!")

    db_user = UserModel(name=user.name,email=user.email)
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db:Session,email:EmailStr):
    db_user = db.query(UserModel).filter(UserModel.email==email).first()
    return db_user

def delete_user(db:Session,user_id:int):
    user= get_user(db=db,user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {user_id} is not found!")
    db.delete(user)
    db.commit()
    return {"detail":f"User with id {user_id} has been deleted"}