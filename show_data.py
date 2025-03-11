#!/usr/bin/env python3
from culinary_compass.models import Session, Recipe, Ingredient, Category, RecipeIngredient

def show_all_data():
    """Display essential data from the database with key relationships."""
    session = Session()

    print("\n=== CATEGORIES ===")
    categories = session.query(Category).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")

    print("\n=== INGREDIENTS ===")
    ingredients = session.query(Ingredient).all()
    for ingredient in ingredients:
        print(f"ID: {ingredient.id}, Name: {ingredient.name}")

    print("\n=== RECIPES ===")
    recipes = session.query(Recipe).all()
    for recipe in recipes:
        # Get category name
        category = session.query(Category).filter_by(id=recipe.category_id).first()
        category_name = category.name if category else "No Category"

        print(f"ID: {recipe.id}, Name: {recipe.name}, Category: {category_name}")
        print(f"Prep: {recipe.prep_time}min, Cook: {recipe.cook_time}min, Serves: {recipe.serving_size}")

        # Get ingredients for this recipe - simplified display
        recipe_ingredients = session.query(RecipeIngredient).filter_by(recipe_id=recipe.id).all()
        if recipe_ingredients:
            ingredients_list = []
            for ri in recipe_ingredients:
                ingredient = session.query(Ingredient).filter_by(id=ri.ingredient_id).first()
                if ingredient:
                    ingredients_list.append(f"{ri.quantity} {ri.unit} {ingredient.name}")
            print(f"Ingredients: {', '.join(ingredients_list)}")
        print("-" * 40)

    session.close()

def add_recipe():
    """Add a new recipe to the database with ingredients."""
    session = Session()

    # Display available categories
    print("\n=== AVAILABLE CATEGORIES ===")
    categories = session.query(Category).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")

    # Get recipe details
    name = input("\nEnter recipe name: ")
    description = input("Enter recipe description: ")
    prep_time = int(input("Enter prep time (minutes): "))
    cook_time = int(input("Enter cook time (minutes): "))
    serving_size = int(input("Enter serving size: "))
    category_id = int(input("Enter category ID: "))
    instructions = input("Enter cooking instructions: ")

    # Create the recipe
    recipe = Recipe.create(
        session,
        name=name,
        description=description,
        prep_time=prep_time,
        cook_time=cook_time,
        serving_size=serving_size,
        category_id=category_id,
        instructions=instructions
    )

    # Add ingredients
    print("\n=== AVAILABLE INGREDIENTS ===")
    ingredients = session.query(Ingredient).all()
    for ingredient in ingredients:
        print(f"ID: {ingredient.id}, Name: {ingredient.name}")

    while True:
        add_more = input("\nAdd an ingredient? (y/n): ").lower()
        if add_more != 'y':
            break

        ingredient_id = int(input("Enter ingredient ID: "))
        quantity = float(input("Enter quantity: "))
        unit = input("Enter unit (e.g., cups, tbsp): ")

        RecipeIngredient.create(
            session,
            recipe_id=recipe.id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )

    session.close()
    print(f"\nRecipe '{name}' added successfully!")

def delete_recipe():
    """Delete a recipe from the database."""
    session = Session()

    # Show available recipes
    print("\n=== AVAILABLE RECIPES ===")
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes available to delete.")
        session.close()
        return

    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}")

    # Get recipe ID to delete
    try:
        recipe_id = int(input("\nEnter ID of recipe to delete: "))
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()

        if not recipe:
            print(f"Recipe with ID {recipe_id} not found.")
            session.close()
            return

        # Delete associated recipe ingredients first
        session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()

        # Delete the recipe
        recipe_name = recipe.name
        session.delete(recipe)
        session.commit()
        print(f"Recipe '{recipe_name}' deleted successfully!")

    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")
    except Exception as e:
        print(f"Error deleting recipe: {e}")
        session.rollback()
    finally:
        session.close()

def show_categories():
    """Display only the categories from the database."""
    session = Session()

    print("\n=== CATEGORIES ===")
    categories = session.query(Category).all()
    if not categories:
        print("No categories found in the database.")
    else:
        for category in categories:
            print(f"ID: {category.id}, Name: {category.name}")

            # Optionally show recipes in this category
            recipes = session.query(Recipe).filter_by(category_id=category.id).all()
            if recipes:
                print(f"  Recipes in this category:")
                for recipe in recipes:
                    print(f"  - {recipe.name}")
            print()

    session.close()

def show_ingredients():
    """Display only the ingredients from the database."""
    session = Session()

    print("\n=== INGREDIENTS ===")
    ingredients = session.query(Ingredient).all()
    if not ingredients:
        print("No ingredients found in the database.")
    else:
        for ingredient in ingredients:
            print(f"ID: {ingredient.id}, Name: {ingredient.name}")

            # Show recipes that use this ingredient
            recipe_ingredients = session.query(RecipeIngredient).filter_by(ingredient_id=ingredient.id).all()
            if recipe_ingredients:
                print(f"  Used in recipes:")
                for ri in recipe_ingredients:
                    recipe = session.query(Recipe).filter_by(id=ri.recipe_id).first()
                    if recipe:
                        print(f"  - {recipe.name} ({ri.quantity} {ri.unit})")
            print()

    session.close()

def add_category():
    """Add a new category to the database."""
    session = Session()

    # Show existing categories
    print("\n=== EXISTING CATEGORIES ===")
    categories = session.query(Category).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")

    # Get new category name
    name = input("\nEnter new category name: ")

    # Check if category already exists
    existing = session.query(Category).filter(Category.name.ilike(name)).first()
    if existing:
        print(f"Category '{name}' already exists with ID: {existing.id}")
        session.close()
        return

    # Create new category
    try:
        category = Category.create(session, name=name)
        print(f"Category '{name}' added successfully with ID: {category.id}")
    except Exception as e:
        print(f"Error adding category: {e}")
        session.rollback()
    finally:
        session.close()

# Update main_menu function to include the new option
def main_menu():
    """Display a menu to choose between viewing data and adding a recipe."""
    while True:
        print("\n=== CULINARY COMPASS MENU ===")
        print("1. View all data")
        print("2. Add a new recipe")
        print("3. Delete a recipe")
        print("4. View categories only")
        print("5. View ingredients only")
        print("6. Add a new category")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":
            show_all_data()
        elif choice == "2":
            add_recipe()
        elif choice == "3":
            delete_recipe()
        elif choice == "4":
            show_categories()
        elif choice == "5":
            show_ingredients()
        elif choice == "6":
            add_category()
        elif choice == "7":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()