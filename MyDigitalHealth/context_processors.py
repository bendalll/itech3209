from .models import Package, Category, Card


def card_packages(request):
    return {
        'all_packages': Package.objects.all()
    }


def card_categories(request):
    return {
        'card_categories': Category.objects.all()
    }


def all_cards(request):
    return {
        'card_list': Card.objects.all()
    }
