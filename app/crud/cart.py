from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.user import get_cart_info_by_user_id, get_user_cart_id
from app.db.models.cart import CartModel
from app.db.models.cart_item import CartItemModel
from app.db.models.product import ProductModel
from app.db.models.user import UserModel
from app.schemas.cart import CartProductsSchema
from app.schemas.cart_item import CartItemSchema

def get_cart_info_by_id(db:Session,current_user:UserModel):
    cart_id = get_user_cart_id(db,current_user.id)
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def get_cart_items_by_user(db:Session,current_user:UserModel):
    cart_id=get_user_cart_id(db,current_user.id)
    items = db.query(ProductModel)\
              .join(CartItemModel, ProductModel.id == CartItemModel.product_id)\
              .filter(CartItemModel.cart_id == cart_id)\
              .all()
    return items

def get_cart_item_count_by_user(db:Session,current_user:UserModel):
    cart = db.query(CartModel).filter(CartModel.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.item_count

def get_cart_item_quantity_by_id(db:Session,current_user:UserModel,product_id:int):
    cart_id = get_user_cart_id(db,current_user.id)
    cart = db.query(CartItemModel).filter(CartItemModel.cart_id == cart_id,CartItemModel.product_id==product_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Product not found in this Cart")
    return cart.quantity



def add_item_to_cart(db:Session,current_user:UserModel,product_id:int):
    cart_id = get_user_cart_id(db=db,user_id=current_user.id)
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        cart_item=CartItemModel(cart_id=cart_id,product_id=product_id,quantity=1)
        db.add(cart_item)
        increase_cart_item_count_by_id(db,cart_id)
    else:
        cart_item.quantity+=1

    get_cart_total_price(db,current_user)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def decrease_item_from_cart(db:Session,current_user:UserModel,product_id:int):
    cart_id=get_user_cart_id(db,current_user.id)
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in this Cart!")
    elif cart_item.quantity==1:
        db.delete(cart_item)
        decrease_cart_item_count_by_id(db,cart_id)
        return {"detail":f"Product removed from cart!"}
    else:
        cart_item.quantity-=1
    get_cart_total_price(db,current_user)    
    db.commit()
    db.refresh(cart_item)
    return {"detail":f"Product {product_id} quantity successfully decreased"}

def remove_item_from_cart(db:Session,current_user:UserModel,product_id):
    cart_id = get_user_cart_id(db,current_user.id)
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in this Cart!")
    
    db.delete(cart_item)
    decrease_cart_item_count_by_id(db,cart_id)
    get_cart_total_price(db,current_user)
    db.commit()
    return {"detail":f"Product {product_id} removed from cart!"}

def empty_cart(db:Session,current_user:UserModel):
    cart_id=get_user_cart_id(db,current_user.id)
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id).delete()
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    cart.item_count=0
    cart.total_price=0
    db.commit()
    return{"detail":"All items removed from cart!"}


def increase_cart_item_count_by_id(db:Session,cart_id):
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    cart.item_count+=1
    db.commit()
    db.refresh(cart)


def decrease_cart_item_count_by_id(db:Session,cart_id):
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    cart.item_count-=1
    db.commit()
    db.refresh(cart)

def get_cart_total_price(db:Session, current_user:UserModel):
    cart_id = get_user_cart_id(db,current_user.id)
    total_price = db.query(func.sum(ProductModel.price * CartItemModel.quantity))\
                         .join(CartItemModel, ProductModel.id == CartItemModel.product_id)\
                         .filter(CartItemModel.cart_id == cart_id)\
                         .scalar()
    total_price = total_price or 0.0
    db.query(CartModel).filter(CartModel.id == cart_id).update({"total_price": total_price or 0.0})
    db.commit()
    return total_price