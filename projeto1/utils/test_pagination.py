from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_start_page(self):
        # Current Page = 1 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        # Current Page = 2 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=2
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_middle_page(self):
        # Current Page = 7 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=7
        )
        self.assertEqual([6, 7, 8, 9], pagination['pagination'])

        # Current Page = 2 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=10
        )
        self.assertEqual([9, 10, 11, 12], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_last_page(self):
        # Current Page = 17 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=17
        )
        self.assertEqual([16, 17, 18, 19], pagination['pagination'])

        # Current Page = 18 - Qt Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qt_page=4,
            current_page=19
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
