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

def add_ingredient():
    """Add a new ingredient to the database."""
    session = Session()

    # Show existing ingredients
    print("\n=== EXISTING INGREDIENTS ===")
    ingredients = session.query(Ingredient).all()
    for ingredient in ingredients:
        print(f"ID: {ingredient.id}, Name: {ingredient.name}")

    # Get new ingredient name
    name = input("\nEnter new ingredient name: ")

    # Check if ingredient already exists
    existing = session.query(Ingredient).filter(Ingredient.name.ilike(name)).first()
    if existing:
        print(f"Ingredient '{name}' already exists with ID: {existing.id}")
        session.close()
        return

    # Create new ingredient
    try:
        ingredient = Ingredient.create(session, name=name)
        print(f"Ingredient '{name}' added successfully with ID: {ingredient.id}")
    except Exception as e:
        print(f"Error adding ingredient: {e}")
        session.rollback()
    finally:
        session.close()

def update_recipe():
    """Update an existing recipe."""
    session = Session()

    # Show available recipes
    print("\n=== AVAILABLE RECIPES ===")
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes available to update.")
        session.close()
        return

    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}")

    # Get recipe ID to update
    try:
        recipe_id = int(input("\nEnter ID of recipe to update: "))
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()

        if not recipe:
            print(f"Recipe with ID {recipe_id} not found.")
            session.close()
            return

        print("\n=== CURRENT RECIPE DETAILS ===")
        print(f"Name: {recipe.name}")
        print(f"Description: {recipe.description}")
        print(f"Prep time: {recipe.prep_time} minutes")
        print(f"Cook time: {recipe.cook_time} minutes")
        print(f"Serving size: {recipe.serving_size}")
        print(f"Instructions: {recipe.instructions}")

        # Get updated details
        print("\nEnter new details (leave blank to keep current value):")
        name = input("Name: ") or recipe.name
        description = input("Description: ") or recipe.description

        try:
            prep_time_input = input("Prep time (minutes): ")
            prep_time = int(prep_time_input) if prep_time_input else recipe.prep_time

            cook_time_input = input("Cook time (minutes): ")
            cook_time = int(cook_time_input) if cook_time_input else recipe.cook_time

            serving_size_input = input("Serving size: ")
            serving_size = int(serving_size_input) if serving_size_input else recipe.serving_size
        except ValueError:
            print("Invalid input for numeric fields. Using existing values.")
            prep_time = recipe.prep_time
            cook_time = recipe.cook_time
            serving_size = recipe.serving_size

        instructions = input("Instructions: ") or recipe.instructions

        # Display available categories
        print("\n=== AVAILABLE CATEGORIES ===")
        categories = session.query(Category).all()
        for category in categories:
            print(f"ID: {category.id}, Name: {category.name}")

        category_id_input = input(f"Category ID (current: {recipe.category_id}): ")
        category_id = int(category_id_input) if category_id_input else recipe.category_id

        # Update recipe
        recipe.name = name
        recipe.description = description
        recipe.prep_time = prep_time
        recipe.cook_time = cook_time
        recipe.serving_size = serving_size
        recipe.category_id = category_id
        recipe.instructions = instructions

        # Ask if user wants to update ingredients
        update_ingredients = input("\nDo you want to update ingredients? (y/n): ").lower() == 'y'

        if update_ingredients:
            # Show current ingredients
            print("\n=== CURRENT INGREDIENTS ===")
            recipe_ingredients = session.query(RecipeIngredient).filter_by(recipe_id=recipe.id).all()
            for ri in recipe_ingredients:
                ingredient = session.query(Ingredient).filter_by(id=ri.ingredient_id).first()
                if ingredient:
                    print(f"ID: {ri.id}, {ri.quantity} {ri.unit} {ingredient.name}")

            # Ask if user wants to remove ingredients
            remove_ingredients = input("\nDo you want to remove any ingredients? (y/n): ").lower() == 'y'
            if remove_ingredients:
                while True:
                    ri_id = input("Enter RecipeIngredient ID to remove (or blank to finish): ")
                    if not ri_id:
                        break
                    try:
                        ri_id = int(ri_id)
                        ri = session.query(RecipeIngredient).filter_by(id=ri_id, recipe_id=recipe.id).first()
                        if ri:
                            session.delete(ri)
                            print("Ingredient removed.")
                        else:
                            print("Ingredient not found.")
                    except ValueError:
                        print("Invalid ID.")

            # Ask if user wants to add ingredients
            add_ingredients = input("\nDo you want to add new ingredients? (y/n): ").lower() == 'y'
            if add_ingredients:
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

        session.commit()
        print(f"\nRecipe '{name}' updated successfully!")

    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")
    except Exception as e:
        print(f"Error updating recipe: {e}")
        session.rollback()
    finally:
        session.close()

def search_recipes():
    """Search for recipes by name, ingredient, or category."""
    session = Session()

    print("\n=== SEARCH RECIPES ===")
    print("1. Search by name")
    print("2. Search by ingredient")
    print("3. Search by category")

    choice = input("\nEnter your choice (1-3): ")

    if choice == "1":
        name = input("Enter recipe name to search: ")
        recipes = session.query(Recipe).filter(Recipe.name.ilike(f"%{name}%")).all()
    elif choice == "2":
        ingredient_name = input("Enter ingredient name to search: ")
        # Find ingredients matching the search term
        ingredients = session.query(Ingredient).filter(Ingredient.name.ilike(f"%{ingredient_name}%")).all()
        if not ingredients:
            print(f"No ingredients found matching '{ingredient_name}'")
            session.close()
            return

        # Get recipe IDs that use these ingredients
        recipe_ids = set()
        for ingredient in ingredients:
            ris = session.query(RecipeIngredient).filter_by(ingredient_id=ingredient.id).all()
            for ri in ris:
                recipe_ids.add(ri.recipe_id)

        # Get the recipes
        recipes = session.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()
    elif choice == "3":
        category_name = input("Enter category name to search: ")
        # Find categories matching the search term
        categories = session.query(Category).filter(Category.name.ilike(f"%{category_name}%")).all()
        if not categories:
            print(f"No categories found matching '{category_name}'")
            session.close()
            return

        # Get recipe IDs in these categories
        category_ids = [category.id for category in categories]
        recipes = session.query(Recipe).filter(Recipe.category_id.in_(category_ids)).all()
    else:
        print("Invalid choice.")
        session.close()
        return

    if not recipes:
        print("No recipes found matching your search criteria.")
    else:
        print(f"\nFound {len(recipes)} recipes:")
        for recipe in recipes:
            category = session.query(Category).filter_by(id=recipe.category_id).first()
            category_name = category.name if category else "No Category"
            print(f"ID: {recipe.id}, Name: {recipe.name}, Category: {category_name}")

    session.close()

def view_recipe_details():
    """View complete details of a single recipe."""
    session = Session()

    # Show available recipes
    print("\n=== AVAILABLE RECIPES ===")
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes available to view.")
        session.close()
        return

    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}")

    # Get recipe ID to view
    try:
        recipe_id = int(input("\nEnter ID of recipe to view: "))
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()

        if not recipe:
            print(f"Recipe with ID {recipe_id} not found.")
            session.close()
            return

        # Get category name
        category = session.query(Category).filter_by(id=recipe.category_id).first()
        category_name = category.name if category else "No Category"

        # Display recipe details
        print("\n" + "=" * 50)
        print(f"RECIPE: {recipe.name}")
        print("=" * 50)
        print(f"Category: {category_name}")
        print(f"Preparation Time: {recipe.prep_time} minutes")
        print(f"Cooking Time: {recipe.cook_time} minutes")
        print(f"Serving Size: {recipe.serving_size}")
        print("\nDescription:")
        print(recipe.description)

        # Get ingredients
        print("\nIngredients:")
        recipe_ingredients = session.query(RecipeIngredient).filter_by(recipe_id=recipe.id).all()
        if recipe_ingredients:
            for ri in recipe_ingredients:
                ingredient = session.query(Ingredient).filter_by(id=ri.ingredient_id).first()
                if ingredient:
                    print(f"- {ri.quantity} {ri.unit} {ingredient.name}")
        else:
            print("No ingredients listed.")

        print("\nInstructions:")
        print(recipe.instructions)
        print("=" * 50)

    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")
    finally:
        session.close()

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
        print("7. Add a new ingredient")
        print("8. Update a recipe")
        print("9. Search recipes")
        print("10. View recipe details")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ")

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
            add_ingredient()
        elif choice == "8":
            update_recipe()
        elif choice == "9":
            search_recipes()
        elif choice == "10":
            view_recipe_details()
        elif choice == "11":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()