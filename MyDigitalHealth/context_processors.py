from .models import Card_Packages, Card_Groups, Cards

def cardPackages(request):
    return {
        'cardPackages': Card_Packages.objects.all()
    }
def cardGroups(request):
    return {
        'cardGroups': Card_Groups.objects.all()
    }
	
def cardList(request):
    return {
        'cardList': Cards.objects.all()
    }