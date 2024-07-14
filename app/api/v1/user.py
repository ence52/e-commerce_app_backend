from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi import security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.deps import authenticate_user
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.crud.user import create_user, delete_user, get_current_active_user,get_user,get_cart_info_by_user_id, get_user_by_email
from app.db.models.user import UserModel
from app.db.session import SessionLocal
from app.schemas.cart import CartSchema
from app.schemas.token_data import Token
from app.schemas.user import  UserInfoSchema, UserSchema, UserCreateSchema
from sqlalchemy.orm import Session

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/',response_model=UserSchema)
def create_new_user(user: UserCreateSchema,db: Session = Depends(get_db)):

    db_user=create_user(db=db,user=user)
    return db_user

@router.get('/')
def check_token(current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    return {"detail":"Successfull"}

@router.get('/info',response_model=UserInfoSchema)
def check_token(current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    return current_user


@router.get('/{user_id}',response_model=UserSchema)
def read_user(user_id:int,db: Session = Depends(get_db)):
    db_user=get_user(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    return db_user

@router.get('/email/{user_email}',response_model=UserSchema)
def read_user(user_email:str,db: Session = Depends(get_db)):
    db_user=get_user_by_email(db=db,email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    return db_user

@router.get('/{user_id}/cart',response_model=CartSchema)
def get_cart_info_by_user_id_endpoint(user_id:int,db:Session=Depends(get_db)):
    return get_cart_info_by_user_id(db,user_id)

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db))->Token:
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
