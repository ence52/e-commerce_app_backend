from datetime import datetime
from typing import List
from pydantic import BaseModel

class ImageCreateSchema(BaseModel):

    url: str
    class Config:
        from_attributes = True

class ImageSchema(ImageCreateSchema):
    product_id: int

class ProductBaseSchema(BaseModel):
    name: str
    brand: str
    model: str
    description: str
    price: float
    rating: float
    category_id: int
    images: List[ImageCreateSchema]
    stock: int

    class Config:
        from_attributes = True

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(ProductBaseSchema):
    pass

class ProductSchema(ProductBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
