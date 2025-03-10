import click
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

from ..models import Session, Recipe, Ingredient, RecipeIngredient, Category

# Create a Rich console for prettier output
console = Console()

@click.group()
def cli():
    """Culinary Compass: A Comprehensive Recipe Management System"""
    pass

# Recipe Commands Group
# This creates a subcommand group for all recipe-related operations
@cli.group()
def recipe():
    """Manage recipes"""
    pass

@recipe.command("list")
def list_recipes():
    """
    List all recipes in the database.

    This command displays a table with basic information about each recipe,
    including ID, name, category, preparation time, cooking time, and servings.
    """
    session = Session()
    recipes = Recipe.get_all(session)

    if not recipes:
        console.print("[bold red]No recipes found![/bold red]")
        return

    # Create a Rich table for better visual presentation
    table = Table(title="Recipes")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Category", style="blue")
    table.add_column("Prep Time (min)", style="yellow")
    table.add_column("Cook Time (min)", style="yellow")
    table.add_column("Servings", style="cyan")

    for recipe in recipes:
        category_name = recipe.category.name if recipe.category else "Uncategorized"
        table.add_row(
            str(recipe.id),
            recipe.name,
            category_name,
            str(recipe.prep_time) if recipe.prep_time else "-",
            str(recipe.cook_time) if recipe.cook_time else "-",
            str(recipe.serving_size) if recipe.serving_size else "-"
        )

    console.print(table)
    session.close()

@recipe.command("view")
@click.argument("recipe_id", type=int)
def view_recipe(recipe_id):
    """View a recipe by ID"""
    session = Session()
    recipe = Recipe.get_by_id(session, recipe_id)

    if not recipe:
        console.print(f"[bold red]Recipe with ID {recipe_id} not found![/bold red]")
        session.close()
        return

    console.print(f"[bold green]Recipe: {recipe.name}[/bold green]")
    console.print(f"[bold blue]Category: {recipe.category.name if recipe.category else 'Uncategorized'}[/bold blue]")
    console.print(f"Preparation Time: {recipe.prep_time} minutes")
    console.print(f"Cooking Time: {recipe.cook_time} minutes")
    console.print(f"Servings: {recipe.serving_size}")

    if recipe.description:
        console.print("\n[bold]Description:[/bold]")
        console.print(recipe.description)

    console.print("\n[bold]Ingredients:[/bold]")
    recipe_ingredients = RecipeIngredient.get_by_recipe_id(session, recipe.id)

    if not recipe_ingredients:
        console.print("[italic]No ingredients listed[/italic]")
    else:
        ingredients_table = Table()
        ingredients_table.add_column("Ingredient", style="green")
        ingredients_table.add_column("Quantity", style="yellow")
        ingredients_table.add_column("Unit", style="blue")

        for ri in recipe_ingredients:
            ingredient = Ingredient.get_by_id(session, ri.ingredient_id)
            ingredients_table.add_row(
                ingredient.name,
                str(ri.quantity),
                ri.unit or "-"
            )

        console.print(ingredients_table)

    if recipe.instructions:
        console.print("\n[bold]Instructions:[/bold]")
        console.print(recipe.instructions)

    session.close()

@recipe.command("add")
@click.option("--name", prompt="Recipe name", help="Name of the recipe")
@click.option("--description", prompt="Description (optional)", default="", help="Description of the recipe")
@click.option("--prep-time", prompt="Preparation time (minutes)", type=int, help="Preparation time in minutes")
@click.option("--cook-time", prompt="Cooking time (minutes)", type=int, help="Cooking time in minutes")
@click.option("--servings", prompt="Number of servings", type=int, help="Number of servings")
@click.option("--category", prompt="Category (optional)", default=None, help="Recipe category")
@click.option("--instructions", prompt="Instructions", help="Cooking instructions")
def add_recipe(name, description, prep_time, cook_time, servings, category, instructions):
    """Add a new recipe"""
    session = Session()

    # Handle category
    category_id = None
    if category:
        category_obj = Category.get_by_name(session, category)
        if not category_obj:
            category_obj = Category.create(session, name=category)
        category_id = category_obj.id

    # Create recipe
    recipe = Recipe.create(
        session,
        name=name,
        description=description,
        prep_time=prep_time,
        cook_time=cook_time,
        serving_size=servings,
        instructions=instructions,
        category_id=category_id
    )

    console.print(f"[bold green]Recipe '{name}' added successfully with ID {recipe.id}![/bold green]")
    console.print("[yellow]Now you can add ingredients to this recipe using:[/yellow]")
    console.print(f"[yellow]  ingredient add-to-recipe {recipe.id}[/yellow]")

    session.close()

@recipe.command("update")
@click.argument("recipe_id", type=int)
@click.option("--name", help="Name of the recipe")
@click.option("--description", help="Description of the recipe")
@click.option("--prep-time", type=int, help="Preparation time in minutes")
@click.option("--cook-time", type=int, help="Cooking time in minutes")
@click.option("--servings", type=int, help="Number of servings")
@click.option("--category", help="Recipe category")
@click.option("--instructions", help="Cooking instructions")
def update_recipe(recipe_id, name, description, prep_time, cook_time, servings, category, instructions):
    """Update a recipe"""
    session = Session()
    recipe = Recipe.get_by_id(session, recipe_id)

    # Continuing from the update_recipe function
    if not recipe:
        console.print(f"[bold red]Recipe with ID {recipe_id} not found![/bold red]")
        session.close()
        return

    update_data = {}
    if name:
        update_data['name'] = name
    if description is not None:
        update_data['description'] = description
    if prep_time is not None:
        update_data['prep_time'] = prep_time
    if cook_time is not None:
        update_data['cook_time'] = cook_time
    if servings is not None:
        update_data['serving_size'] = servings
    if instructions is not None:
        update_data['instructions'] = instructions

    # Handle category update
    if category:
        category_obj = Category.get_by_name(session, category)
        if not category_obj:
            category_obj = Category.create(session, name=category)
        update_data['category_id'] = category_obj.id

    if not update_data:
        console.print("[yellow]No changes specified for update.[/yellow]")
        session.close()
        return

    Recipe.update(session, recipe_id, **update_data)
    console.print(f"[bold green]Recipe with ID {recipe_id} updated successfully![/bold green]")
    session.close()

@recipe.command("delete")
@click.argument("recipe_id", type=int)
@click.option("--confirm", is_flag=True, help="Confirm deletion without prompt")
def delete_recipe(recipe_id, confirm):
    """Delete a recipe"""
    session = Session()
    recipe = Recipe.get_by_id(session, recipe_id)

    if not recipe:
        console.print(f"[bold red]Recipe with ID {recipe_id} not found![/bold red]")
        session.close()
        return

    if not confirm:
        if not click.confirm(f"Are you sure you want to delete recipe '{recipe.name}'?"):
            console.print("[yellow]Deletion cancelled.[/yellow]")
            session.close()
            return

    Recipe.delete(session, recipe_id)
    console.print(f"[bold green]Recipe '{recipe.name}' deleted successfully![/bold green]")
    session.close()

@recipe.command("search")
@click.option("--name", help="Search by recipe name")
@click.option("--category", help="Search by category name")
@click.option("--ingredient", help="Search by ingredient name")
def search_recipes(name, category, ingredient):
    """Search for recipes by name, category, or ingredient"""
    session = Session()
    query = session.query(Recipe)

    if name:
        query = query.filter(Recipe.name.like(f"%{name}%"))

    if category:
        query = query.join(Category).filter(Category.name.like(f"%{category}%"))

    if ingredient:
        query = query.join(RecipeIngredient).join(Ingredient).filter(Ingredient.name.like(f"%{ingredient}%"))

    recipes = query.all()

    if not recipes:
        console.print("[bold yellow]No recipes found matching your search criteria.[/bold yellow]")
        session.close()
        return

    table = Table(title="Search Results")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Category", style="blue")
    table.add_column("Prep Time (min)", style="yellow")
    table.add_column("Cook Time (min)", style="yellow")

    for recipe in recipes:
        category_name = recipe.category.name if recipe.category else "Uncategorized"
        table.add_row(
            str(recipe.id),
            recipe.name,
            category_name,
            str(recipe.prep_time) if recipe.prep_time else "-",
            str(recipe.cook_time) if recipe.cook_time else "-"
        )

    console.print(table)
    session.close()

# Ingredient Commands
@cli.group()
def ingredient():
    """Manage ingredients"""
    pass

@ingredient.command("list")
def list_ingredients():
    """List all ingredients"""
    session = Session()
    ingredients = Ingredient.get_all(session)

    if not ingredients:
        console.print("[bold red]No ingredients found![/bold red]")
        session.close()
        return

    table = Table(title="Ingredients")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")

    for ingredient in ingredients:
        table.add_row(str(ingredient.id), ingredient.name)

    console.print(table)
    session.close()

@ingredient.command("add")
@click.option("--name", prompt="Ingredient name", help="Name of the ingredient")
def add_ingredient(name):
    """Add a new ingredient"""
    session = Session()

    # Check if ingredient already exists
    existing = Ingredient.get_by_name(session, name)
    if existing:
        console.print(f"[bold yellow]Ingredient '{name}' already exists with ID {existing.id}![/bold yellow]")
        session.close()
        return

    ingredient = Ingredient.create(session, name=name)
    console.print(f"[bold green]Ingredient '{name}' added successfully with ID {ingredient.id}![/bold green]")
    session.close()

@ingredient.command("add-to-recipe")
@click.argument("recipe_id", type=int)
def add_ingredient_to_recipe(recipe_id):
    """Add ingredients to a recipe"""
    session = Session()
    recipe = Recipe.get_by_id(session, recipe_id)

    if not recipe:
        console.print(f"[bold red]Recipe with ID {recipe_id} not found![/bold red]")
        session.close()
        return

    console.print(f"[bold green]Adding ingredients to recipe: {recipe.name}[/bold green]")

    while True:
        ingredient_name = click.prompt("Ingredient name (or 'done' to finish)")

        if ingredient_name.lower() == 'done':
            break

        # Check if ingredient exists, create if not
        ingredient = Ingredient.get_by_name(session, ingredient_name)
        if not ingredient:
            ingredient = Ingredient.create(session, name=ingredient_name)
            console.print(f"[green]Created new ingredient: {ingredient_name}[/green]")

        quantity = click.prompt("Quantity", type=float)
        unit = click.prompt("Unit (e.g., g, ml, tbsp)", default="")

        # Add to recipe
        RecipeIngredient.create(
            session,
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=quantity,
            unit=unit
        )

        console.print(f"[green]Added {quantity} {unit} {ingredient_name} to the recipe[/green]")

    console.print(f"[bold green]Finished adding ingredients to {recipe.name}![/bold green]")
    session.close()

@ingredient.command("update")
@click.argument("ingredient_id", type=int)
@click.option("--name", prompt="New name", help="New name for the ingredient")
def update_ingredient(ingredient_id, name):
    """Update an ingredient"""
    session = Session()
    ingredient = Ingredient.get_by_id(session, ingredient_id)

    if not ingredient:
        console.print(f"[bold red]Ingredient with ID {ingredient_id} not found![/bold red]")
        session.close()
        return

    old_name = ingredient.name
    Ingredient.update(session, ingredient_id, name=name)
    console.print(f"[bold green]Ingredient updated from '{old_name}' to '{name}'![/bold green]")
    session.close()

@ingredient.command("delete")
@click.argument("ingredient_id", type=int)
@click.option("--confirm", is_flag=True, help="Confirm deletion without prompt")
def delete_ingredient(ingredient_id, confirm):
    """Delete an ingredient"""
    session = Session()
    ingredient = Ingredient.get_by_id(session, ingredient_id)

    if not ingredient:
        console.print(f"[bold red]Ingredient with ID {ingredient_id} not found![/bold red]")
        session.close()
        return

    # Check if ingredient is used in any recipes
    recipe_ingredients = session.query(RecipeIngredient).filter_by(ingredient_id=ingredient_id).all()
    if recipe_ingredients and not confirm:
        console.print(f"[bold yellow]Warning: This ingredient is used in {len(recipe_ingredients)} recipes.[/bold yellow]")
        if not click.confirm("Deleting this ingredient will remove it from all recipes. Continue?"):
            console.print("[yellow]Deletion cancelled.[/yellow]")
            session.close()
            return

    Ingredient.delete(session, ingredient_id)
    console.print(f"[bold green]Ingredient '{ingredient.name}' deleted successfully![/bold green]")
    session.close()

# Category Commands
@cli.group()
def category():
    """Manage recipe categories"""
    pass

@category.command("list")
def list_categories():
    """List all categories"""
    session = Session()
    categories = Category.get_all(session)

    if not categories:
        console.print("[bold red]No categories found![/bold red]")
        session.close()
        return

    table = Table(title="Categories")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Recipe Count", style="blue")

    for category in categories:
        recipe_count = len(category.recipes)
        table.add_row(str(category.id), category.name, str(recipe_count))

    console.print(table)
    session.close()

@category.command("add")
@click.option("--name", prompt="Category name", help="Name of the category")
def add_category(name):
    """Add a new category"""
    session = Session()

    # Check if category already exists
    existing = Category.get_by_name(session, name)
    if existing:
        console.print(f"[bold yellow]Category '{name}' already exists with ID {existing.id}![/bold yellow]")
        session.close()
        return

    category = Category.create(session, name=name)
    console.print(f"[bold green]Category '{name}' added successfully with ID {category.id}![/bold green]")
    session.close()

@category.command("update")
@click.argument("category_id", type=int)
@click.option("--name", prompt="New name", help="New name for the category")
def update_category(category_id, name):
    """Update a category"""
    session = Session()
    category = Category.get_by_id(session, category_id)

    if not category:
        console.print(f"[bold red]Category with ID {category_id} not found![/bold red]")
        session.close()
        return

    old_name = category.name
    Category.update(session, category_id, name=name)
    console.print(f"[bold green]Category updated from '{old_name}' to '{name}'![/bold green]")
    session.close()

@category.command("delete")
@click.argument("category_id", type=int)
@click.option("--confirm", is_flag=True, help="Confirm deletion without prompt")
def delete_category(category_id, confirm):
    """Delete a category"""
    session = Session()
    category = Category.get_by_id(session, category_id)

    if not category:
        console.print(f"[bold red]Category with ID {category_id} not found![/bold red]")
        session.close()
        return

    # Check if category is used in any recipes
    if category.recipes and not confirm:
        console.print(f"[bold yellow]Warning: This category is used in {len(category.recipes)} recipes.[/bold yellow]")
        if not click.confirm("Recipes in this category will become uncategorized. Continue?"):
            console.print("[yellow]Deletion cancelled.[/yellow]")
            session.close()
            return

    Category.delete(session, category_id)
    console.print(f"[bold green]Category '{category.name}' deleted successfully![/bold green]")
    session.close()