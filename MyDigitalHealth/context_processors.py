from .models import Package, Category, Card


def card_packages(request):
    return {
        'cardPackages': Package.objects.all()
    }


def card_categories(request):
    return {
        'cardGroups': Category.objects.all()
    }


def all_cards(request):
    return {
        'cardList': Card.objects.all()
    }
