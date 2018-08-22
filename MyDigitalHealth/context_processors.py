from .models import Package, Card


def get_card_packages(request):
    return {
        'cardPackages': Package.objects.all()
    }


# def cardGroups(request):
#     return {
#         'cardGroups': Card_Groups.objects.all()
#     }


def get_card_list(request):
    return {
        'cardList': Card.objects.all()
    }
