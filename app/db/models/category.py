from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class CategoryModel(Base):
    __tablename__ ="categories"

    id= Column(Integer,primary_key=True)
    name= Column(String(255))
    products = relationship("ProductModel", back_populates="category")
    