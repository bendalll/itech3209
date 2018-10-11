from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import RegistrationForm, CreateCardPackage, CreateComments
from .models import Card_Packages, Card_Groups, Cards, Comments, Sorted_Package


def index(request):
    """
    View function for home page of site.
    """
    return render(
        request,
        'index.html',
    )


def cards(request):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Card_Packages())
        if form.is_valid():
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            names = request.POST.getlist('name')
            main_color = request.POST['main_color']
            if 'comments_allowed' in request.POST and request.POST['comments_allowed'] is not False:
                comments_allowed = True
            else:
                comments_allowed = False
            user = request.user
            for name in names:
                cardPackage = Card_Packages(name=name, user=user, main_color=main_color,
                                            comments_allowed=comments_allowed)
                cardPackage.save()
            for title in titles:
                group = Card_Groups(card_package=cardPackage, title=title)
                group.save()
            for text in texts:
                card = Cards(card_package=cardPackage, text=text)
                card.save()
            return render(
                request,
                'index.html',
            )
        else:
            print("Form failed validation: ", form.errors)
            form = CreateCardPackage(instance=Card_Packages())
            args = {'form': form}
            return render(
                request,
                'create_package.html',
                args
            )
    else:
        form = CreateCardPackage(instance=Card_Packages())
        args = {'form': form}
        return render(
            request,
            'create_package.html',
            args
        )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(
                request,
                'index.html',
            )
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(
            request,
            'register.html',
            args
        )
#
#
# def view(request):
#     cardPackages = Card_Packages.objects.all()
#     return render(
#         request,
#         'view.html',
#
#     )
#
#
# def package(request):
#     cardPackages = Card_Packages.objects.all()
#     context = {'cardPackages': cardPackages}
#     return render(
#         request,
#         'package.html',
#         context
#     )


def packageList(request, package):
    package = Card_Packages.objects.get(id__exact=package)
    user = request.user
    sortcardList = Cards.objects.all()
    sortGroups = Card_Groups.objects.filter(card_package=package).values_list('id', flat=True)
    sortCards = Cards.objects.filter(card_package=package).values_list('id', flat=True)
    filteredCardsList = None
    filteredGroupsList = None
    if request.user.is_anonymous:
        comments = Comments.objects.filter(card_package__exact= package)
        sortPackageUser = Sorted_Package.objects.filter(card_package=package)
        sortPackageGroups = Sorted_Package.objects.filter(card_package=package).values_list('card_group', flat=True)
        sortPackageCards = Sorted_Package.objects.filter(card_package=package).values_list('cards', flat=True)
        sortPackage = Sorted_Package.objects.filter(card_package=package)
    else:
        comments = Comments.objects.filter(card_package__exact= package).filter(user__exact= user)
        sortPackageUser = Sorted_Package.objects.filter(card_package=package).filter(user__exact = user).exists()
        sortPackageGroups = Sorted_Package.objects.filter(card_package=package).filter(user__exact = user).values_list('card_group', flat=True)
        sortPackageCards = Sorted_Package.objects.filter(card_package=package).filter(user__exact = user).values_list('cards', flat=True)
        sortPackage = Sorted_Package.objects.filter(card_package=package).filter(user__exact = user)

        filteredGroups = [x for x in sortGroups if x not in sortPackageGroups]
        filteredCards = [x for x in sortCards if x not in sortPackageCards]

        for filteredGroups in filteredGroups:
            filteredGroupsList = Card_Groups.objects.filter(card_package=package).filter(id=filteredGroups)
        for filteredCards in filteredCards:
            filteredCardsList = Cards.objects.filter(card_package=package).filter(id=filteredCards)
    context = {'package': package, 'user': user, 'comments': comments, 'sortcardList': sortcardList,
               'sortPackage': sortPackage, 'sortPackageUser': sortPackageUser, 'filteredGroupsList': filteredGroupsList,
               'filteredCardsList': filteredCardsList}
    return render(
        request,
        'packageList.html',
        context
    )


def admin(request):
    cardPackages = Card_Packages.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'admin.html',
        context
    )


def edit(request, package):
    package = Card_Packages.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'edit.html',
        context
    )


def comments(request, package):
    if request.method =='POST':
        commentID = request.POST.get('commentID')
        user = request.user
        text = request.POST.get('comment')
        cardPackage = Card_Packages.objects.get(id__exact=package)
        cardsList = request.POST.getlist('cardsList')
        sortPackages = request.POST.getlist('sortPackages')
        sortedCardsInts = list(filter(None, request.POST.getlist('sortedCards')))
        cardGroupIDs = request.POST.getlist('cardGroupID')
        sortCardGroupIDs = request.POST.getlist('sortCardGroupID')
        sortedCardLists = list(filter(None, request.POST.getlist('sortedCardList')))
        sorted = Sorted_Package()
        for sortPackage, sortedCardList in zip(sortPackages,sortedCardLists):
            sortedSplitCardPackage = sortedCardList.split(",")
            sortedGroup = sortedSplitCardPackage[0]
            sortedCard = sortedSplitCardPackage[1:]
            sorted = Sorted_Package.objects.get(id__exact=sortPackage)
            sorted.card_group = Card_Groups.objects.get(id__exact=sortedGroup)
            sorted.user = user
            sorted.cards.clear()
            sorted.save()
            for sortedCard in sortedCard:
                sorted.cards.add(Cards.objects.get(id__exact=sortedCard))

        for sortedCardsInt in sortedCardsInts:
            sort = Sorted_Package()
            sort.card_package = cardPackage
            sort.user = user
            splitCardPackage = sortedCardsInt.split(",")
            sortGroup = splitCardPackage[0]
            sortCard = splitCardPackage[1:]
            print(sortGroup)
            sort.card_group = Card_Groups.objects.get(id__exact=sortGroup)
            sort.save()
            for sortCard in sortCard:
                sort.cards.add(Cards.objects.get(id__exact=sortCard))

        comment = Comments()
        comment.card_package = cardPackage
        comment.user = user
        comment.comment = text
        comment.id = commentID
        comment.save()
        return render(
            request,
            'index.html',
        )
    else:
        form = CreateComments(instance=Comments())
        args = {'form': form}
        return render(
            request,
            'packageList.html',
            args
        )


def editPackage(request, package):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Card_Packages())
        if form.is_valid():
            cardPackage = Card_Packages.objects.get(id__exact=package)
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            cardGroupIDs = request.POST.getlist('cardGroupID')
            cardListIDs = request.POST.getlist('cardListID')
            newGroups = request.POST.getlist('newGroup')
            newCards = request.POST.getlist('newCard')
            deleteGroups = request.POST.getlist('deleteGroup')
            deleteCards = request.POST.getlist('deleteCard')
            test = Card_Groups()
            card = Cards()

            for newGroup in newGroups:
                group = Card_Groups(card_package = cardPackage, title = newGroup)
                group.save()
            for newCard in newCards:
                card = Cards(card_package = cardPackage, text = newCard)
                card.save()
            for cardGroupID, title in zip(cardGroupIDs, titles):
                group.id = cardGroupID
                group.card_package = cardPackage
                group.title = title
                group.save()
            for cardListID, text in zip(cardListIDs, texts):
                card.id = cardListID
                card.card_package = cardPackage
                card.text = text
                card.save()
            for deleteCard in deleteCards:
                test = Cards.objects.get(id__exact= deleteCard)
                test.delete()

            for deleteGroup in deleteGroups:
                test1 = Card_Groups.objects.filter(card_package = cardPackage).filter(id__exact= deleteGroup)
                test1.delete()
            return render(
                request,
                'admin.html',
            )
    else:
        form = CreateCardPackage(instance=Card_Packages())
        args = {'form': form}
        return render(
            request,
            'admin.html',
            args
        )


def deletePackage(request, package_id):
    """ Remove the package (as provided by package id) from the database """
    # TODO: put this in a try/catch for db errors
    package = Card_Packages.objects.get(pk=package_id)
    package.delete()
    # TODO: return some indicator of success or failure
    cardPackages = Card_Packages.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'admin.html',
        context
    )


def get_css(request, package_id):
    package = Card_Packages.objects.get(pk=package_id)
    main_color = package.main_color
    return render(
        request,
        'heading_colors.css',
        {'main_color': main_color},
        content_type='text/css'
    )
