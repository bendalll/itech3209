from cardsort.models import Package


def card_packages(request):
    return {
        'card_packages': Package.objects.all()
    }
