from cardsort.models import Package


def card_packages(request):
    """ Will return only the base packages not user assigned ones """
    return {
        'card_packages': Package.objects.filter(assignedpackage__isnull=True)
    }
