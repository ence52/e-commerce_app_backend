from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.cart import add_item_to_cart, decrease_item_from_cart, empty_cart, get_cart_info_by_id, get_cart_item_count_by_id, get_cart_item_quantity_by_id, get_cart_items_by_user,   get_cart_total_price, remove_item_from_cart
from app.crud.user import get_current_active_user
from app.db.models.user import UserModel
from app.db.session import SessionLocal
from app.schemas.cart import  CartSchema
from app.schemas.cart_item import CartItemSchema
from app.schemas.product import  ProductSchema


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=CartSchema)
def get_cart_info_by_id_endpoint(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return get_cart_info_by_id(db,current_user)

@router.post('/items',response_model=List[ProductSchema])
def get_cart_items_by_id_endpoint(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return get_cart_items_by_user(db=db,current_user=current_user)

@router.post('/item_count',response_model=int)
def get_cart_item_count_by_id_endpoint(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return get_cart_item_count_by_id(db,current_user)
    

@router.post('/total_price',response_model= float)
def get_cart_total_price_endpoint(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    total_price= get_cart_total_price(db,current_user)
    return total_price


@router.get('/items/{product_id}/quantity',response_model=int)
def get_cart_item_quantity_by_id_enpoint(product_id:int,current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return get_cart_item_quantity_by_id(db,current_user,product_id)

@router.post('/items/{product_id}/add',response_model=CartItemSchema)
def add_product_to_cart(product_id:int,current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return  add_item_to_cart(db,current_user,product_id)

@router.post('/items/{product_id}/decrease',response_model=dict)
def decrease_product_from_cart(product_id:int,current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return decrease_item_from_cart(db,current_user,product_id)

@router.delete('/items/{product_id}/all',response_model=dict)
def remove_product_from_cart(product_id:int,current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return remove_item_from_cart(db,current_user,product_id)

@router.delete('/items')
def delete_all_items_by_cart_id(current_user: Annotated[UserModel, Depends(get_current_active_user)],db:Session=Depends(get_db)):
    return empty_cart(db,current_user)