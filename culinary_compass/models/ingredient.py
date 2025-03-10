from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationship with RecipeIngredient
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"

    @classmethod
    def create(cls, session, **kwargs):
        ingredient = cls(**kwargs)
        session.add(ingredient)
        session.commit()
        return ingredient

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def update(cls, session, id, **kwargs):
        ingredient = cls.get_by_id(session, id)
        if ingredient:
            for key, value in kwargs.items():
                setattr(ingredient, key, value)
            session.commit()
        return ingredient

    @classmethod
    def delete(cls, session, id):
        ingredient = cls.get_by_id(session, id)
        if ingredient:
            session.delete(ingredient)
            session.commit()
            return True
        return False