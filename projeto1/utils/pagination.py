import math

from django.core.paginator import Paginator


def make_pagination_range(page_range, qt_page, current_page):

    current_page_index = page_range.index(current_page)
    middle_range = math.ceil(qt_page/2)

    # Caso tenha menos página que a quantidade de elementos por página
    if len(page_range) <= qt_page:

        start_range = 0
        stop_range = page_range[-1]

        pagination = page_range

    else:
        # pega o valor inicial
        start_range = current_page_index - (middle_range - 1)

        # caso o valor inicial seja menor que 0 o valor inicial fica igual a 0
        if start_range < 0:
            start_range = 0

        # pega o valor final, valor_inicial + qt_page
        stop_range = start_range + qt_page

        # caso o valor final seja maior que o total de páginas o valor
        # final passa a ser a última página da lista e o valor inicial
        # -------- passa a ser a última página menos o qt_page -------
        if stop_range >= page_range[-1]:
            stop_range = page_range[-1]
            start_range = stop_range - qt_page

        pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'current_page': current_page,
        'qt_page': qt_page,
        'total_pages': len(page_range),
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': start_range == 0,
        'last_page_out_of_range': stop_range == len(page_range)
    }


def make_pagination(request, queryset, per_page, qt_page=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        page_obj.paginator.page_range, qt_page, current_page)

    return page_obj, pagination_range
