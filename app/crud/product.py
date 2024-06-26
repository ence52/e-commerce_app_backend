
import datetime
from typing import List
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.db.models.category import CategoryModel
from app.db.models.product import Image, ProductModel
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema

def get_product_by_id(db:Session,product_id):
    return db.query(ProductModel).filter(ProductModel.id==product_id).first()

def create_product(db:Session,product:ProductCreateSchema):
    db_product = ProductModel(
        name = product.name,
        brand = product.brand,
        model = product.model,
        description = product.description,
        price = product.price,
        category_id = product.category_id,
        stock= product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    

    for image in product.images:
        db_image = Image(
            url=image.url,
            product_id=db_product.id  
        )
        db.add(db_image)

    db.commit()
    db.refresh(db_product)
    return db_product


def create_products_with_list(db:Session,products:List[ProductCreateSchema]):
    for product in products:
        create_product(db,product)
    

def delete_product(db:Session,product_id):
    product= get_product_by_id(db,product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {product_id} is not found!")
    db.delete(product)
    db.commit()
    return {"detail":f"Product with id {product_id} has been deleted"}

def get_all_products(db:Session):
    return db.query(ProductModel).all()



def update_product(db:Session,product_id:int,product:ProductUpdateSchema):
    db_product = get_product_by_id(db,product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {product_id} is not found!")
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    UTC_PLUS_3 = datetime.timezone(datetime.timedelta(hours=3))
    db_product.updated_at=datetime.datetime.now(UTC_PLUS_3)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_images(db:Session,product_id:int):
    return db.query(Image).filter(Image.product_id==product_id).all()