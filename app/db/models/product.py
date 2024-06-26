from sqlalchemy import  Column,  Float, ForeignKey, Integer, String, Text
from app.db.models.mixins import TimeStampMixin
from app.db.session import Base
from sqlalchemy.orm import relationship

class ProductModel(Base,TimeStampMixin):
    __tablename__ ="products"

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False)
    brand = Column(String(255),nullable=False)
    model = Column(String(255),nullable=False)
    description = Column(Text)
    price = Column(Float(precision=2), nullable=False)
    images = relationship("Image", order_by="Image.id", back_populates="product")
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("CategoryModel", back_populates="products")
    stock= Column(Integer,nullable=False)
    
class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("ProductModel", back_populates="images")