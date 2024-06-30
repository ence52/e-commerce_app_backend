
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.crud.category import get_all_categories, get_all_products_by_category_id, get_category_info_by_id
from app.db.session import SessionLocal
from app.schemas.category import CategorySchema
from app.schemas.product import ProductSchema


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/{category_id}/products',response_model=List[ProductSchema])
def get_all_products_by_category_id_endpoint(category_id:int,db:Session=Depends(get_db)):
    products= get_all_products_by_category_id(db,category_id)
    if not products :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Products not found for this category!")
    return products

@router.get('/{category_id}',response_model=CategorySchema)
def get_category_info_by_id_endpoint(category_id:int,db:Session=Depends(get_db)):
    category= get_category_info_by_id(db,category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found!")
    return category

@router.get('',response_model=List[CategorySchema])
def get_all_categories_endpoint(db:Session=Depends(get_db)):
    return get_all_categories(db)