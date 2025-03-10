from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationship with Recipe
    recipes = relationship("Recipe", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

    @classmethod
    def create(cls, session, **kwargs):
        category = cls(**kwargs)
        session.add(category)
        session.commit()
        return category

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
        category = cls.get_by_id(session, id)
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            session.commit()
        return category

    @classmethod
    def delete(cls, session, id):
        category = cls.get_by_id(session, id)
        if category:
            session.delete(category)
            session.commit()
            return True
        return False