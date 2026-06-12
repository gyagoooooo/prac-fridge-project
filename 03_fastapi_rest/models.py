from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    storage_type = Column(String)
    quantity = Column(Integer)
    unit = Column(String)
    expire_date = Column(String)
    memo = Column(String)
    created_at = Column(String)