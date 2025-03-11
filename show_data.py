#!/usr/bin/env python3
from culinary_compass.models import Session, Recipe, Ingredient, Category, RecipeIngredient

def show_all_data():
    """Display all data from the database."""
    session = Session()

    print("\n=== RECIPES ===")
    recipes = session.query(Recipe).all()
    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}, Prep: {recipe.prep_time}min, Cook: {recipe.cook_time}min")

    print("\n=== INGREDIENTS ===")
    ingredients = session.query(Ingredient).all()
    for ingredient in ingredients:
        print(f"ID: {ingredient.id}, Name: {ingredient.name}")

    print("\n=== CATEGORIES ===")
    categories = session.query(Category).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")

    print("\n=== RECIPE INGREDIENTS ===")
    recipe_ingredients = session.query(RecipeIngredient).all()
    for ri in recipe_ingredients:
        print(f"Recipe ID: {ri.recipe_id}, Ingredient ID: {ri.ingredient_id}, Quantity: {ri.quantity} {ri.unit}")

    session.close()

if __name__ == "__main__":
    show_all_data()