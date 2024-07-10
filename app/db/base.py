from app.db.models.user import UserModel
from app.db.models.product import ProductModel
from app.db.models import user, product, order, order_detail, review, payment, category



from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()