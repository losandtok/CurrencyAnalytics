from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from user_database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Timeseries", back_populates="owner")


class Timeseries(Base):
    __tablename__ = "timeseries"

    id = Column(Integer, primary_key=True, index=True)
    query_date = Column(DateTime(timezone=True), server_default=func.now())
    start_to_end_time = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

