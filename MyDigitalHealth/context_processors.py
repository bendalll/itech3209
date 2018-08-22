from .models import Package, Card


def card_packages(request):
    return {
        'card_packages': Package.objects.all()
    }


# def cardGroups(request):
#     return {
#         'cardGroups': Card_Groups.objects.all()
#     }


def card_list(request):
    return {
        'card_list': Card.objects.all()
    }
