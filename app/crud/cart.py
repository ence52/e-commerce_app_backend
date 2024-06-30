from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.cart import CartModel
from app.db.models.cart_item import CartItemModel
from app.db.models.product import ProductModel

def get_cart_info_by_id(db:Session,cart_id):
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart



def add_item_to_cart(db:Session,cart_id,product_id):
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        cart_item=CartItemModel(cart_id=cart_id,product_id=product_id,quantity=1)
        db.add(cart_item)
        increase_cart_item_count_by_id(db,cart_id)
        
    else:
        cart_item.quantity+=1
        
        
    get_cart_total_price(db,cart_id)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def decrease_item_from_cart(db:Session,cart_id,product_id):
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in this Cart!")
    elif cart_item.quantity==1:
        db.delete(cart_item)
        decrease_cart_item_count_by_id(db,cart_id)
        return {"detail":f"Product removed from cart!"}
    else:
        cart_item.quantity-=1
    get_cart_total_price(db,cart_id)    
    db.commit()
    db.refresh(cart_item)
    return {"detail":f"Product {product_id} quantity successfully decreased"}

def remove_item_from_cart(db:Session,cart_id,product_id):
    cart_item = db.query(CartItemModel).filter(CartItemModel.cart_id==cart_id,CartItemModel.product_id==product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in this Cart!")
    
    db.delete(cart_item)
    decrease_cart_item_count_by_id(db,cart_id)
    get_cart_total_price(db,cart_id)
    db.commit()
    return {"detail":f"Product {product_id} removed from cart!"}

def empty_cart(db:Session,cart_id):

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

def get_cart_total_price(db:Session, cart_id):
    total_price = db.query(func.sum(ProductModel.price * CartItemModel.quantity))\
                         .join(CartItemModel, ProductModel.id == CartItemModel.product_id)\
                         .filter(CartItemModel.cart_id == cart_id)\
                         .scalar()

    db.query(CartModel).filter(CartModel.id == cart_id).update({"total_price": total_price or 0.0})
    db.commit()
    return total_price