from typing import Optional

from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    title: str = Field(description="some title description", max_length=30)
    number_of_views: int = Field(description="number_of_views description", default=0)
    cooking_time: int = Field(description="some description cooking_time", gt=0, lt=120)
    ingredients: Optional[str]
    description: Optional[str]


class RecipeIn(BaseRecipe): ...


class RecipeOutShort(BaseModel):
    title: str
    number_of_views: int
    cooking_time: int


class RecipeOutDetail(BaseModel):
    title: str
    cooking_time: int
    ingredients: Optional[str]
    description: Optional[str]
