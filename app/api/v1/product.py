from typing import List
from fastapi import APIRouter, Depends, HTTPException,status

from app.crud.product import create_product, create_products_with_list, delete_product, get_all_products, get_images, get_product_by_id, search_products_by_name, update_product
from app.db.session import SessionLocal
from app.schemas.product import ImageSchema, ProductCreateSchema, ProductDetailSchema, ProductUpdateSchema
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/{product_id}',response_model=ProductDetailSchema)
def read_product(product_id:int, db:Session=Depends(get_db)):
    db_product = get_product_by_id(db=db,product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found!")
    return db_product

@router.get('/',response_model=List[ProductDetailSchema])
def get_all_products_endpoint(db:Session=Depends(get_db)):
    return get_all_products(db)

@router.get('/search/{search_text}',response_model=List[ProductDetailSchema])
def get_all_products_endpoint(search_text:str,db:Session=Depends(get_db)):
    return search_products_by_name(db,search_text)



@router.get('/{product_id}/images',response_model=List[ImageSchema])
def get_images_by_id(product_id:int,db:Session=Depends(get_db)):
    return get_images(db,product_id)



@router.post('/',response_model=ProductDetailSchema)
def create_new_product(product: ProductCreateSchema,db: Session = Depends(get_db)):

    db_product=create_product(db=db,product=product)
    return db_product

@router.post('/list')
def create_new_product_by_list(products:List[ProductCreateSchema],db: Session = Depends(get_db)):
    create_products_with_list(db,products)
    return {"detail":"Products created!"}

@router.delete('/{product_id}',response_model=dict)
def delete_product_endpoint(product_id:int,db:Session=Depends(get_db)):
    return delete_product(db,product_id)

@router.put('/{product_id}',response_model=ProductDetailSchema)
def update_product_endpoint(product_id:int,product:ProductUpdateSchema,db:Session=Depends(get_db)):
    return update_product(db,product_id,product)