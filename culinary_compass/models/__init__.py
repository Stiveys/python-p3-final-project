from .base import Base, Session, engine
from .recipe import Recipe
from .ingredient import Ingredient
from .recipe_ingredient import RecipeIngredient
from .category import Category

def create_tables():
    Base.metadata.create_all(engine)