from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from cardsort.forms import NewPackageForm, EditPackageForm, SubmittedForm
from .forms import RegistrationForm
from cardsort.models import Package, UserCardsort


def index(request):
    """ View function for home page of site. """
    return render(
        request,
        'index.html',
    )


def register(request):
    """
    View to create a new user with data provided
    **Fails if the password does not meet the requirements, without advising the user of the reason**
    If successful, creates the user, logs them in and sends to home page;
    If fails, currently refreshes the page with no additional information
    """
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
        else:  # TODO return error
            form = RegistrationForm()
            args = {'form': form}
            return render(
                request,
                'register.html',
                {'form': form}
            )
    else:  # TODO return error
        form = RegistrationForm()
        args = {'form': form}
        return render(
            request,
            'register.html',
            {'form': form}
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def create_package(request):
    """ Administrator functionality to create new Packages with related Cards and Categories """
    if request.method == 'POST':
        form = SubmittedForm(request)
        if form.is_valid():
            form.save()
        # new_package = validate_and_save_package(request)
        return HttpResponseRedirect('administration')

    else:
        form = NewPackageForm(2, 3).to_dict()

        return render(
            request,
            'create_edit.html',
            context=form
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def edit_package(request, package_id):
    """ Display the editing page with pre-filled data; if POST, save the edited package and redirect to admin page """
    if request.method == 'POST':
        print("Package ID is: ", request.POST['package_id'])
        form = SubmittedForm(request)
        if form.is_valid():
            form.save()
            messages.info(request, 'Changes saved.')
        else:
            messages.error(request, "An error occurred when saving")
        return redirect('administration')
    else:
        filled_form = EditPackageForm(package_id).to_dict()
        return render(
            request,
            'create_edit.html',
            context=filled_form
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def package_administration(request):
    """ Generate and display the Administration page with a list of the packages the admin has created """
    own_packages = Package.objects.filter(owner=request.user)
    context = {'own_packages': own_packages}
    return render(
        request,
        'package_administration.html',
        context
    )


def package_open(request, package_id):
    """ Display the package as a cardsort activity for the user to complete """
    context = Package.objects.get(pk=package_id).to_dict()
    return render(
        request,
        'active.html',
        context
    )


def activity_save(request, package_id):
    # TODO: this should create a UserCardsort object with the positions of cards in categories from request.POST
    if request.method == "POST":
        data = request.POST
        package = Package.objects.get(pk=package_id)
        cards_unassigned = data['card_ids_unassigned'].split(',')
        sortlist = {}

        # Check if save thing exists
        if UserCardsort.objects.filter(package=package, user=request.user).exists():
            UserCardsort.objects.get(package=package, user=request.user).delete()

        for category in package.get_categories():
            new_sortlist = data['card_ids_for_' + str(category.pk)].split(',')
            for card in new_sortlist:
                sortlist[card] = category.pk

    return redirect('home')


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_choose_user(request, package_id):
    active_package = Package.objects.get(pk=package_id)
    user_list = User.objects.all()
    context = {'active_package': active_package,
               'user_list': user_list
               }
    return render(
        request,
        'assign_package.html',
        context
    )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_package_to_user(request, package_id, user_id):
    """ Function to assign the active package to the provided user - # TODO? creates instance of UserCardsort """
    # get the package by id
    active_package = Package.objects.get(pk=package_id)
    # get the user by id
    assigned_user = User.objects.get(pk=user_id)
    # check if UserCardsort already exists
    all_pack_assignments = UserCardsort.objects.all()
    for cardsort in all_pack_assignments:
        # if exists, return and say already assigned
        # TODO: change this so that you can tell it's already assigned on the page, and don't have to make this call
        if cardsort.package == active_package and cardsort.user == assigned_user:
            context = {'message': "This package is already assigned to this user"}
            return render(
                request,
                'assign_package.html',
                context
            )
        # if not exist, create it and provide success message
        else:
            assignment = UserCardsort(package=active_package, user=assigned_user)
            assignment.save()
            context = {'assignment': assignment}
            return render(
                request,
                'assign_package.html',
                context
            )
    # Nothing exists there yet so have to make the first item and then this code won't be used
    else:
        assignment = UserCardsort(package=active_package, user=assigned_user)
        assignment.save()
        context = {'assignment': assignment}
        return render(
            request,
            'assign_package.html',
            context
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def delete_package(request, package_id):
        instance = Package.objects.get(pk=package_id)
        # TODO: try/catch delete errors here
        instance.delete()
        own_packages = Package.objects.filter(owner=request.user)
        context = {'own_packages': own_packages, 'message': 'Delete successful'}
        return render(
            request,
            'package_administration.html',
            context
        )
