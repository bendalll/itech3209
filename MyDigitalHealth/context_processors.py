from .models import Package, Category, Card

def cardPackages(request):
    return {
        'cardPackages': Package.objects.all()
    }
def cardGroups(request):
    return {
        'cardGroups': Category.objects.all()
    }
	
def cardList(request):
    return {
        'cardList': Card.objects.all()
    }