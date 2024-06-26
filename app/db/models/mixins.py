import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr

class TimeStampMixin():
    @declared_attr
    def created_at(cls):
        # UTC+3 saat dilimi
        UTC_PLUS_3 = datetime.timezone(datetime.timedelta(hours=3))
        return Column(DateTime, default=lambda: datetime.datetime.now(UTC_PLUS_3), nullable=False)
    @declared_attr
    def updated_at(cls):
        UTC_PLUS_3 = datetime.timezone(datetime.timedelta(hours=3))
        if cls.created_at is not None:
            return Column(DateTime, default=lambda: datetime.datetime.now(UTC_PLUS_3), nullable=False)
        else:
            Column(DateTime, default=lambda: cls.created_at, nullable=False)