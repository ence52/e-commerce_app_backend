from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base


class FavoriteModel (Base):
    __tablename__ = "favorites"
    id= Column(Integer,primary_key=True,index=True)
    user_id= Column(Integer,ForeignKey('users.id'),nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    users = relationship('UserModel',back_populates='favorites')
    