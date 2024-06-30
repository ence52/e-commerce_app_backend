from datetime import datetime
import bcrypt
from sqlalchemy import Column, DateTime, Integer, String
from app.core.security import check_password
from app.db.models.mixins import TimeStampMixin
from app.db.session import Base
from sqlalchemy.orm import relationship

class UserModel(Base,TimeStampMixin):
    __tablename__ = "users"

    id= Column(Integer,primary_key=True,index=True)
    name = Column(String(50))
    email = Column(String(60),unique=True,index=True)
    hashed_password = Column(String(64))

    carts = relationship('CartModel', back_populates='users')
    

    def set_password(self,password: str):
        self.hashed_password= hash_password(password)

    def check_password(self,password :str)->bool:
        return check_password(password,self.hashed_password)

def hash_password(password:str)->str:
    password_bytes=password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes,salt)
    return hashed_password.decode('utf-8')

