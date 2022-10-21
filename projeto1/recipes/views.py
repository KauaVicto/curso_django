from django.http import Http404
from django.shortcuts import render
from utils.recipes.factory import make_recipe

from recipes.models import Category, Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True  # Apenas as receitas que foram publicadas
    ).order_by('-id')
    return render(request, "recipes/pages/home.html", context={
        'recipes': recipes,
    })


def recipe(request, id):
    return render(request, "recipes/pages/recipe-view.html", context={
        'recipe': make_recipe(),
        'is_detail_page': True
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,  # Todas as receitas de uma categoria
        is_published=True  # Apenas as receitas que foram publicadas
    ).order_by('-id')

    category = Category.objects.filter(
        id=category_id
    ).first()

    if category is None:
        raise Http404('Not found 😊')
    else:
        return render(request, "recipes/pages/category.html", context={
            'recipes': recipes,
            'title': f'{category.name} | Category'
        })
