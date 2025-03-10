import unittest
from culinary_compass.models import Session, Recipe, Ingredient, RecipeIngredient, Category, create_tables

class TestRecipeModel(unittest.TestCase):
    def setUp(self):
        # Create a test database in memory
        create_tables()
        self.session = Session()

    def tearDown(self):
        # Clean up after each test
        self.session.close()

    def test_recipe_creation(self):
        # Test that we can create a recipe
        category = Category.create(self.session, name="Test Category")
        recipe = Recipe.create(
            self.session,
            name="Test Recipe",
            description="A test recipe",
            prep_time=10,
            cook_time=20,
            serving_size=2,
            category_id=category.id,
            instructions="Test instructions"
        )

        # Verify the recipe was created with correct attributes
        self.assertEqual(recipe.name, "Test Recipe")
        self.assertEqual(recipe.description, "A test recipe")
        self.assertEqual(recipe.prep_time, 10)
        self.assertEqual(recipe.cook_time, 20)
        self.assertEqual(recipe.serving_size, 2)
        self.assertEqual(recipe.category_id, category.id)
        self.assertEqual(recipe.instructions, "Test instructions")

    def test_recipe_ingredient_association(self):
        # Test that we can associate ingredients with recipes
        ingredient = Ingredient.create(self.session, name="Test Ingredient")
        recipe = Recipe.create(
            self.session,
            name="Test Recipe",
            description="A test recipe",
            prep_time=10,
            cook_time=20,
            serving_size=2,
            instructions="Test instructions"
        )

        # Associate ingredient with recipe
        recipe_ingredient = RecipeIngredient.create(
            self.session,
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=2.5,
            unit="cups"
        )

        # Verify the association
        self.assertEqual(len(recipe.ingredients), 1)
        self.assertEqual(recipe.ingredients[0].ingredient_id, ingredient.id)
        self.assertEqual(recipe.ingredients[0].quantity, 2.5)
        self.assertEqual(recipe.ingredients[0].unit, "cups")

if __name__ == "__main__":
    unittest.main()