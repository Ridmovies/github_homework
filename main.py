from contextlib import asynccontextmanager
from typing import List, Sequence

from fastapi import FastAPI, HTTPException
from sqlalchemy import column, select, update
from sqlalchemy.exc import NoResultFound

from database import Base, async_engine, session
from models import Recipe
from schemas import RecipeIn, RecipeOutDetail, RecipeOutShort


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan start")
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("lifespan end")
    await session.close()
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="fastapi homework")


@app.get(
    "/recipes", response_model=List[RecipeOutShort], description="get_all_short_recipes"
)
async def get_all_short_recipes() -> Sequence[Recipe]:
    """get_all_short_recipes"""
    async with session:
        res = await session.execute(
            select(Recipe).order_by(Recipe.number_of_views.desc(), Recipe.cooking_time)
        )
        return res.scalars().all()


@app.get("/recipes/detail_list", response_model=List[RecipeOutDetail])
async def get_all_detail_recipes() -> Sequence[Recipe]:
    """get_all_detail_recipes"""
    async with session:
        res = await session.execute(select(Recipe))
        return res.scalars().all()


@app.get("/recipes/{id}", response_model=RecipeOutDetail)
async def get_detail_recipe(id: int) -> RecipeOutDetail:
    """get_detail_recipe"""
    async with session.begin():
        try:
            res = await session.execute(select(Recipe).where(column("id") == id))
            recipe = res.scalars().one()
            number_of_views = int(recipe.number_of_views)
            number_of_views += 1
            await session.execute(
                update(Recipe)
                .where(column("id") == id)
                .values(number_of_views=number_of_views)
            )
            return recipe

        except NoResultFound:
            raise HTTPException(status_code=404, detail="Recipe not found")


@app.post("/recipes", response_model=RecipeOutDetail)
async def add_recipe(recipe: RecipeIn) -> Recipe:
    """add_recipe"""
    new_recipe = Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
        return new_recipe


# uvicorn main:app --host 0.0.0.0 --port 8000
# isort --check --diff --profile black main.py
