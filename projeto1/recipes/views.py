from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from recipes.models import Category, Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True  # Apenas as receitas que foram publicadas
    ).order_by('-id')
    return render(request, "recipes/pages/home.html", context={
        'recipes': recipes,
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(
        id=id,
        is_published=True
    ).first()

    if recipe is None:
        raise Http404('Receita não encontrada')
        return

    return render(request, "recipes/pages/recipe-view.html", context={
        'recipe': recipe,
        'is_detail_page': True
    })


def category(request, category_id):
    category_query = Category.objects.filter(id=category_id)
    category = get_object_or_404(category_query)

    recipes = Recipe.objects.filter(
        category__id=category_id,  # Todas as receitas de uma categoria
        is_published=True  # Apenas as receitas que foram publicadas
    ).order_by('-id')

    return render(request, "recipes/pages/category.html", context={
        'recipes': recipes,
        'title': f'{category.name} | Category'
    })


def search(request):
    search = request.GET.get('search', '').strip()

    # caso o usuário não insira nada na busca
    if len(search) == 0:
        return redirect('/')

    recipes = Recipe.objects.filter(
        title__contains=search
    )

    return render(request, 'recipes/pages/search.html', context={
        'search': search,
        'page_title': f'Pesquisa por {search}',
        'recipes': recipes,
    })
