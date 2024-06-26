from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,status
from app.api.deps import authenticate_user
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.crud.user import create_user, delete_user, get_user
from app.db.session import SessionLocal
from app.schemas.user import UserLoginSchema, UserSchema, UserCreateSchema
from sqlalchemy.orm import Session

router = APIRouter()

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

@router.get('/{user_id}',response_model=UserSchema)
def read_user(user_id:int,db: Session = Depends(get_db)):
    db_user=get_user(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    return db_user

@router.post('/login')
def login_for_access_token(db: Session=Depends(get_db),user: UserLoginSchema=Depends()):
    user = authenticate_user(db,user.email,user.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password",headers={"WWW-Authenticate":"Bearer"})
    
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.email},expires_delta=access_token_expires)
    return {"access_token":access_token,"token_type":"bearer"}

@router.delete('/{user_id}',response_model=dict)
def delete_user_endpoint(user_id:int,db: Session= Depends(get_db)):
    return delete_user(db,user_id)
