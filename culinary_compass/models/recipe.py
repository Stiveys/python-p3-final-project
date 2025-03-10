from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Recipe(Base):
    """
    Recipe model representing a cooking recipe in the database.

    This model stores all recipe information including name, description,
    preparation and cooking times, serving size, and cooking instructions.
    It also maintains relationships with ingredients and categories.
    """
    __tablename__ = 'recipes'

    # Primary key and basic recipe information
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    prep_time = Column(Integer)  # in minutes
    cook_time = Column(Integer)  # in minutes
    serving_size = Column(Integer)
    instructions = Column(Text)

    # One-to-many relationship with RecipeIngredient
    # This allows a recipe to have multiple ingredients with specific quantities
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")

    # Many-to-one relationship with Category
    # Each recipe can belong to one category
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="recipes")

    def __repr__(self):
        """String representation of the Recipe object"""
        return f"<Recipe(id={self.id}, name='{self.name}')>"

    @classmethod
    def create(cls, session, **kwargs):
        """Create a new recipe in the database"""
        recipe = cls(**kwargs)
        session.add(recipe)
        session.commit()
        return recipe

    @classmethod
    def get_all(cls, session):
        """Retrieve all recipes from the database"""
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, id):
        """Retrieve a specific recipe by its ID"""
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def update(cls, session, id, **kwargs):
        """Update an existing recipe with new values"""
        recipe = cls.get_by_id(session, id)
        if recipe:
            for key, value in kwargs.items():
                setattr(recipe, key, value)
            session.commit()
        return recipe

    @classmethod
    def delete(cls, session, id):
        """Delete a recipe from the database"""
        recipe = cls.get_by_id(session, id)
        if recipe:
            session.delete(recipe)
            session.commit()
            return True
        return False