from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib import messages

from .forms import RegistrationForm


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
        else:
            messages.error("Form validation error")
            form = RegistrationForm()
            context = {'form': form}
            return render(
                request,
                'register.html',
                context
            )
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(
            request,
            'register.html',
            context
        )
