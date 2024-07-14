from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.crud.favorite import get_all, toggle_favorite
from app.crud.user import get_current_active_user
from app.db.models.user import UserModel
from app.db.session import SessionLocal
from app.schemas.favorite import FavoriteSchema
from app.schemas.product import ProductSchema


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[ProductSchema])
def get_favorites(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    favorites= get_all(db=db,current_user=current_user)
    print(favorites)
    return favorites

@router.post('/',response_model=dict)
def toggle_favorite_endpoint(product_id:int,current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return toggle_favorite(db=db,current_user=current_user, product_id=product_id)