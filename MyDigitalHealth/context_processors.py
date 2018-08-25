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


def get_admin_own_packages(request):
    owner = request.user
    own_packages = Package.get_packages_by_owner(owner)
    return own_packages
