#!/usr/bin/env python3
from culinary_compass.models import Session, Recipe, Ingredient, RecipeIngredient, Category, create_tables

def seed_database():
    """
    Seed the database with initial data.

    This function creates sample categories, ingredients, and recipes
    to provide users with example data when they first start using
    the application.
    """
    session = Session()

    # Create sample categories for recipe organization
    categories = {
        "Breakfast": Category.create(session, name="Breakfast"),
        "Lunch": Category.create(session, name="Lunch"),
        "Dinner": Category.create(session, name="Dinner"),
        "Dessert": Category.create(session, name="Dessert"),
        "Appetizer": Category.create(session, name="Appetizer"),
        "Vegetarian": Category.create(session, name="Vegetarian"),
        "Vegan": Category.create(session, name="Vegan")
    }

    # Create common ingredients that can be used in recipes
    ingredients = {
        "Flour": Ingredient.create(session, name="Flour"),
        "Sugar": Ingredient.create(session, name="Sugar"),
        # ... other ingredients ...
    }

    # Create sample recipes with detailed information
    pancakes = Recipe.create(
        session,
        name="Classic Pancakes",
        description="Fluffy and delicious pancakes for a perfect breakfast.",
        prep_time=10,
        cook_time=15,
        serving_size=4,
        category_id=categories["Breakfast"].id,
        instructions="""
1. In a large bowl, sift together the flour, baking powder, salt, and sugar.
2. Make a well in the center and pour in the milk, egg, and melted butter; mix until smooth.
3. Heat a lightly oiled griddle or frying pan over medium-high heat.
4. Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.
5. Cook until bubbles form and the edges are dry, then flip and cook until browned on the other side.
6. Serve hot with maple syrup, butter, or your favorite toppings.
"""
    )

    # Associate ingredients with recipes, including quantities and units
    RecipeIngredient.create(session, recipe_id=pancakes.id, ingredient_id=ingredients["Flour"].id, quantity=1.5, unit="cups")
    RecipeIngredient.create(session, recipe_id=pancakes.id, ingredient_id=ingredients["Sugar"].id, quantity=3, unit="tbsp")
    # ... other recipe ingredients ...

    session.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    # Create database tables before seeding
    create_tables()
    # Populate the database with sample data
    seed_database()