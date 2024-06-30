from sqlalchemy import  Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class CartModel(Base):
    __tablename__='carts'


    id= Column(Integer,primary_key=True)
    user_id= Column(Integer,ForeignKey('users.id'),nullable=False)
    total_price= Column(Float(precision=2),default=0.00)
    status = Column(String(50), default='active')
    discount_code = Column(String(50))
    discount_amount = Column(Float(precision=2), default=0.00)
    item_count = Column(Integer, default=0)

    users=relationship('UserModel',back_populates='carts')
    cart_items=relationship('CartItemModel',back_populates='carts',cascade='all,delete-orphan')