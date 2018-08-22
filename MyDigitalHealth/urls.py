from django.urls import path, reverse
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView, {'template_name': 'login.html'}, name='login'),
	path('logout', LogoutView, name='logout'),
	path('create', views.create, name='create'),
	path('register', views.register, name='register'),
	path('cards', views.cards, name='cards'),
	path('view', views.view, name='view'),
	path('package', views.package, name='package'),
	path('packageList/<packagePK>/', views.packageList, name='packageList'),
]