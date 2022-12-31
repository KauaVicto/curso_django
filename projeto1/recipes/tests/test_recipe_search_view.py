from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_user_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?search=teste'
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertIn('Pesquisa por &quot;teste&quot;', content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?search={title1}')
        response2 = self.client.get(f'{search_url}?search={title2}')
        response_both = self.client.get(f'{search_url}?search=this')

        # Response 1
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        # Response 2
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        # Response both
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'This is recipe one'
        description2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            description=description1,
            author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two',
            description=description2,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?search={description1}')
        response2 = self.client.get(f'{search_url}?search={description2}')
        response_both = self.client.get(f'{search_url}?search=this')

        # Response 1
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        # Response 2
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        # Response both
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    @patch('recipes.views.PER_PAGE', new=10)
    def test_recipe_search_is_paginated(self):
        for i in range(19):
            self.make_recipe(
                title='receita',
                slug=f'slug-{i}',
                author_data={'username': f'usuario{i}'}
            )

        response = self.client.get(
            reverse('recipes:search') + '?search=receita')
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 10)
        self.assertEqual(len(paginator.get_page(2)), 9)
