from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )
        content = response.content.decode('utf-8')

        # Checa se possui 1 recipe
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={
                'category_id': recipe.category.id
            }))

        # Checa se possui 1 recipe
        self.assertIn("não possui receitas nesta categoria",
                      response.content.decode('utf-8'))

    @patch('recipes.views.PER_PAGE', new=10)
    def test_recipe_category_is_paginated(self):
        category = self.make_category(name='categoria teste')
        for i in range(19):
            self.make_recipe(
                slug=f'slug-{i}',
                author_data={'username': f'usuario{i}'},
                category_data=category,
                make_category=False
            )

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': category.id}))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 10)
        self.assertEqual(len(paginator.get_page(2)), 9)
