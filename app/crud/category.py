from sqlalchemy.orm import Session

from app.db.models.category import CategoryModel
from app.db.models.product import ProductModel


def get_category_info_by_id(db:Session,category_id):
    return db.query(CategoryModel).filter(CategoryModel.id==category_id).first()


def get_all_products_by_category_id(db:Session,category_id:int):
    return db.query(ProductModel).filter(ProductModel.category_id==category_id).all()