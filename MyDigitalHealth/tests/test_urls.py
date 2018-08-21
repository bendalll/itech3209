from django.urls import resolve
from django.test import TestCase
from MyDigitalHealth.views import cards


class ViewTest(TestCase):

    def test_cards_url_resolves_to_cards_view(self):
        found = resolve('/MyDigitalHealth/cards')
        self.assertEqual(found.func, cards)
