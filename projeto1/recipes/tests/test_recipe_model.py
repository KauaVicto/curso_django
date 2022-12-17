from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):

        setattr(self.recipe, field, 'A' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('is_published', False),
        ('preparation_steps_is_html', False)
    ])
    def test_recipe_defaults_fields(self, field, campo_default):
        recipe = Recipe(
            title='recipe title',
            description='description',
            slug=f'slug{field}',
            preparation_time=2,
            preparation_time_unit='Minutos',
            servings=3,
            servings_unit='Pessoas',
            preparation_steps='preparation_steps',
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='new user')
        )
        recipe.full_clean()
        recipe.save()
        self.assertEqual(getattr(recipe, field), campo_default)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Teste de Representação'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Teste de Representação')
