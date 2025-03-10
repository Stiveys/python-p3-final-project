from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50))

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")

    def __repr__(self):
        return f"<RecipeIngredient(recipe_id={self.recipe_id}, ingredient_id={self.ingredient_id}, quantity={self.quantity})>"

    @classmethod
    def create(cls, session, **kwargs):
        recipe_ingredient = cls(**kwargs)
        session.add(recipe_ingredient)
        session.commit()
        return recipe_ingredient

    @classmethod
    def get_by_recipe_id(cls, session, recipe_id):
        return session.query(cls).filter_by(recipe_id=recipe_id).all()

    @classmethod
    def delete(cls, session, id):
        recipe_ingredient = session.query(cls).filter_by(id=id).first()
        if recipe_ingredient:
            session.delete(recipe_ingredient)
            session.commit()
            return True
        return False