from typing import List, Optional
from pydantic import BaseModel

from app.schemas.cart_item import CartItemSchema
from app.schemas.product import ProductDetailSchema


class CartBaseSchema(BaseModel):
 
    user_id:int
    total_price:float
    status:str
    discount_code:Optional[str] = None
    discount_amount:float
    cart_items:List[CartItemSchema]
    item_count:int

class CartSchema(CartBaseSchema):
    id: int
    

    class Config:
        from_attributes = True

class CartProductsSchema(BaseModel):
    id:int
    products: List[ProductDetailSchema]