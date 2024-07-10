

from pydantic import BaseModel

from app.schemas.product import ProductDetailSchema


class CartItemBaseSchema(BaseModel):
    cart_id:int
    product_id:int
    quantity:int
    

class CartItemSchema(CartItemBaseSchema):
    id:int
    class Config:
        from_attributes=True