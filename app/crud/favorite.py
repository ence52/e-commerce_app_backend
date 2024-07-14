from app.db.models.favorite import FavoriteModel
from app.db.models.product import ProductModel
from app.db.models.user import UserModel
from sqlalchemy.orm import Session


def get_all(db:Session,current_user:UserModel):
    items = db.query(ProductModel)\
              .join(FavoriteModel, ProductModel.id == FavoriteModel.product_id)\
              .filter(FavoriteModel.user_id == current_user.id)\
              .all()
    return items

def get_favorite_by_id(db:Session,user_id:int,product_id:int):
   return db.query(FavoriteModel).filter(FavoriteModel.product_id==product_id,FavoriteModel.user_id==user_id).first()

def toggle_favorite(db:Session,current_user:UserModel,product_id:int):
    db_favorite = get_favorite_by_id(db,current_user.id,product_id)
    if  db_favorite is None:
        new_favorite= FavoriteModel(user_id=current_user.id,product_id=product_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)
        return {"detail":"Favorite added!"}
    else:
        db.delete(db_favorite)
        db.commit()
        return {"detail":"Favorite deleted!"}
    
    