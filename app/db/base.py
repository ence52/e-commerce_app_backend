from app.db.models.user import UserModel
from app.db.models.product import ProductModel
from app.db.models import user, product, order, order_detail, review, payment, category

# Bu dosya, tüm modelleri içe aktararak metadata oluşturulmasını sağlar.
Base = declarative_base()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()