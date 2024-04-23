from sqlalchemy import Column, Integer, String

from database import Base


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String, index=True)
    number_of_views = Column(Integer, index=True)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String, nullable=True)
    description = Column(String, nullable=True)
