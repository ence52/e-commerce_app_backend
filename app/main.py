from typing import Union
from app.api.v1 import category, product, user
from app.db.models.category import CategoryModel
from app.db.models.product import ProductModel
from app.db.models.user import UserModel

from .db.session import  engine
from fastapi import FastAPI

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
ProductModel.metadata.create_all(bind=engine)
UserModel.metadata.create_all(bind=engine)
CategoryModel.metadata.create_all(bind=engine)


app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])

