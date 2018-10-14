from .models import Card_Packages


def cardPackages(request):
    return {'cardPackages': Card_Packages.objects.all()}
