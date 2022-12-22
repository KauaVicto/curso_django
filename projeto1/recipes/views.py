from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from recipes.models import Category, Recipe
from utils.pagination import make_pagination_range


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True  # Apenas as receitas que foram publicadas
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        page_obj.paginator.page_range, 6, current_page)

    return render(request, "recipes/pages/home.html", context={
        'recipes': page_obj,
        'pagination_range': pagination_range
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

    # realiza a busca no banco de dados
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        ),
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', context={
        'search': search,
        'page_title': f'Pesquisa por "{search}"',
        'recipes': recipes,
    })
