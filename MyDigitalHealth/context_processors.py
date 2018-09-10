from .models import Card_Packages, Card_Groups, Cards, Comments, Sorted_Package

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

def commentList(request):
    return {
        'commentList': Comments.objects.all()
    }	
	
def sortedPackageList(request):
    return {
        'sortedPackageList': Sorted_Package.objects.all()
    }		