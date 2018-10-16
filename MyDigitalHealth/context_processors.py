from .models import Package


def cardPackages(request):
    return {'cardPackages': Package.objects.all()}
