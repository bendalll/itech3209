from .models import Permission, Package


def card_packages(request):
    user = request.user

    if user.is_authenticated:
        packages = []
        permissions = Permission.objects.filter(user=user)
        for permission in permissions:
            packages.append(permission.package)

        if user.is_staff:
            own_packages = Package.objects.filter(owner=user)
            for package in own_packages:
                packages.append(package)
        return {'card_packages': packages}
    return {'': ''}

