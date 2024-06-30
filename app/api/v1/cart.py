from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.cart import add_item_to_cart, decrease_item_from_cart, empty_cart, get_cart_info_by_id, get_cart_total_price, remove_item_from_cart
from app.db.session import SessionLocal
from app.schemas.cart import CartSchema
from app.schemas.cart_item import CartItemSchema


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/{cart_id}',response_model=CartSchema)
def get_cart_info_by_id_endpoint(cart_id:int,db:Session=Depends(get_db)):
    cart= get_cart_info_by_id(db,cart_id)
    return cart

@router.get('/{cart_id}/total_price',response_model= int)
def get_cart_total_price_endpoint(cart_id:int,db:Session=Depends(get_db)):
    total_price= get_cart_total_price(db,cart_id)
    return total_price


@router.post('/{cart_id}/items/{product_id}',response_model=CartItemSchema)
def add_product_to_cart(cart_id:int,product_id,db:Session=Depends(get_db)):
    return add_item_to_cart(db,cart_id,product_id)

@router.delete('/{cart_id}/items/{product_id}',response_model=dict)
def decrease_product_from_cart(cart_id:int,product_id,db:Session=Depends(get_db)):
    return decrease_item_from_cart(db,cart_id,product_id)

@router.delete('/{cart_id}/items/{product_id}/all',response_model=dict)
def remove_product_from_cart(cart_id:int,product_id,db:Session=Depends(get_db)):
    return remove_item_from_cart(db,cart_id,product_id)

@router.delete('/{cart_id}/items')
def delete_all_items_by_cart_id(cart_id:int,db:Session=Depends(get_db)):
    return empty_cart(db,cart_id)